"""WebSocket API endpoints for real-time market data."""

import asyncio
import json
from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends, HTTPException, status
from pydantic import BaseModel, ValidationError

from app.core.config import settings
from app.core.websocket import (
    ConnectionManager,
    SubscriptionType,
    get_connection_manager,
    WSMessage,
    TickerMessage,
    OHLCVMessage,
    OrderBookMessage,
    TradeMessage,
    SubscriptionMessage,
    ErrorMessage,
    HeartbeatMessage,
)
from app.api.v1.auth import get_current_user_dependency
from app.db.models import User

router = APIRouter(prefix="/ws", tags=["websocket"])


class SubscriptionRequest(BaseModel):
    """WebSocket subscription request."""

    action: str  # "subscribe" or "unsubscribe"
    type: str  # ticker, ohlcv, order_book, trades, market_summary
    symbols: List[str]
    timeframe: Optional[str] = None


class WSAuthMessage(BaseModel):
    """Authentication message for WebSocket."""

    type: str = "auth"
    token: str


@router.websocket("/market-data")
async def websocket_market_data(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    """WebSocket endpoint for real-time market data."""
    client_id = str(uuid4())
    manager = get_connection_manager()
    user = None

    # Try to authenticate if token provided
    if token:
        try:
            from app.core.security import decode_token
            from app.db.session import get_db_context
            from app.db.models import User
            from sqlalchemy import select

            payload = decode_token(token)
            user_id = payload.sub

            async with get_db_context() as db:
                result = await db.execute(select(User).where(User.id == user_id))
                user = result.scalar_one_or_none()
        except Exception:
            pass  # Continue as anonymous

    await manager.connect(websocket, client_id)

    # Send welcome message
    await manager.send_personal_message(client_id, {
        "type": "welcome",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "client_id": client_id,
            "authenticated": user is not None,
            "user_tier": user.role.value if user else "anonymous",
            "server_time": datetime.now(timezone.utc).isoformat(),
        },
    })

    # Start heartbeat task
    heartbeat_task = asyncio.create_task(_heartbeat(manager, client_id))

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                msg_type = message.get("type")

                if msg_type == "auth":
                    # Re-authenticate
                    token = message.get("token")
                    if token:
                        try:
                            from app.core.security import decode_token
                            from app.db.session import get_db_context
                            from app.db.models import User
                            from sqlalchemy import select

                            payload = decode_token(token)
                            user_id = payload.sub

                            async with get_db_context() as db:
                                result = await db.execute(select(User).where(User.id == user_id))
                                user = result.scalar_one_or_none()

                            await manager.send_personal_message(client_id, {
                                "type": "auth_result",
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "data": {"success": user is not None, "user_tier": user.role.value if user else "anonymous"},
                            })
                        except Exception as e:
                            await manager.send_personal_message(client_id, {
                                "type": "error",
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "data": {"code": "AUTH_FAILED", "message": str(e)},
                            })

                elif msg_type in ["subscribe", "unsubscribe"]:
                    await _handle_subscription(manager, client_id, message, user)

                elif msg_type == "ping":
                    await manager.send_personal_message(client_id, {
                        "type": "pong",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "data": {},
                    })

                elif msg_type == "get_subscriptions":
                    subs = manager.subscriptions.get(client_id, [])
                    await manager.send_personal_message(client_id, {
                        "type": "subscriptions",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "data": {
                            "subscriptions": [
                                {
                                    "type": s.subscription_type.value,
                                    "symbols": s.symbols,
                                    "timeframe": s.timeframe,
                                }
                                for s in subs
                            ]
                        },
                    })

                else:
                    await manager.send_personal_message(client_id, {
                        "type": "error",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "data": {"code": "UNKNOWN_MESSAGE_TYPE", "message": f"Unknown message type: {msg_type}"},
                    })

            except json.JSONDecodeError:
                await manager.send_personal_message(client_id, {
                    "type": "error",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "data": {"code": "INVALID_JSON", "message": "Invalid JSON message"},
                })
            except ValidationError as e:
                await manager.send_personal_message(client_id, {
                    "type": "error",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "data": {"code": "VALIDATION_ERROR", "message": str(e)},
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
    finally:
        heartbeat_task.cancel()
        await manager.disconnect(client_id)


async def _handle_subscription(
    manager: ConnectionManager,
    client_id: str,
    message: dict,
    user: Optional[User],
) -> None:
    """Handle subscription/unsubscription request."""
    action = message.get("action")
    sub_type_str = message.get("type")
    symbols = message.get("symbols", [])
    timeframe = message.get("timeframe")

    # Validate subscription type
    try:
        sub_type = SubscriptionType(sub_type_str)
    except ValueError:
        await manager.send_personal_message(client_id, {
            "type": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"code": "INVALID_SUBSCRIPTION_TYPE", "message": f"Invalid subscription type: {sub_type_str}"},
        })
        return

    # Validate symbols
    if not symbols:
        await manager.send_personal_message(client_id, {
            "type": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"code": "NO_SYMBOLS", "message": "At least one symbol required"},
        })
        return

    # Check tier limits
    if user and not _check_tier_limits(user, sub_type, len(symbols)):
        await manager.send_personal_message(client_id, {
            "type": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"code": "TIER_LIMIT_EXCEEDED", "message": "Subscription limit exceeded for your tier"},
        })
        return

    if action == "subscribe":
        success = await manager.subscribe(client_id, sub_type, symbols, timeframe)
        await manager.send_personal_message(client_id, {
            "type": "subscription",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "action": "subscribed" if success else "failed",
                "subscription_type": sub_type.value,
                "symbols": symbols,
                "timeframe": timeframe,
            },
        })
    elif action == "unsubscribe":
        success = await manager.unsubscribe(client_id, sub_type, symbols)
        await manager.send_personal_message(client_id, {
            "type": "subscription",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {
                "action": "unsubscribed" if success else "failed",
                "subscription_type": sub_type.value,
                "symbols": symbols,
            },
        })
    else:
        await manager.send_personal_message(client_id, {
            "type": "error",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": {"code": "INVALID_ACTION", "message": f"Invalid action: {action}"},
        })


def _check_tier_limits(user: User, sub_type: SubscriptionType, symbol_count: int) -> bool:
    """Check if user's tier allows the subscription."""
    from app.core.licensing import get_license_manager, has_feature

    license_manager = get_license_manager()
    user_tier = "free"
    for license_obj in user.licenses:
        valid, _ = license_manager.validate_license(license_obj)
        if valid:
            user_tier = license_obj.tier.value
            break

    # Define limits per tier
    limits = {
        "free": {"max_symbols": 5, "allowed_types": ["ticker", "ohlcv"]},
        "pro": {"max_symbols": 50, "allowed_types": ["ticker", "ohlcv", "order_book", "trades", "market_summary"]},
        "institutional": {"max_symbols": 500, "allowed_types": ["ticker", "ohlcv", "order_book", "trades", "market_summary"]},
    }

    tier_limits = limits.get(user_tier, limits["free"])

    if sub_type.value not in tier_limits["allowed_types"]:
        return False

    # Could also check total active subscriptions
    return symbol_count <= tier_limits["max_symbols"]


async def _heartbeat(manager: ConnectionManager, client_id: str, interval: int = 30) -> None:
    """Send periodic heartbeat to client."""
    try:
        while True:
            await asyncio.sleep(interval)
            success = await manager.send_personal_message(client_id, {
                "type": "heartbeat",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {"server_time": datetime.now(timezone.utc).isoformat()},
            })
            if not success:
                break
    except asyncio.CancelledError:
        pass
    except Exception:
        pass


# REST endpoint to get WebSocket stats
@router.get("/stats")
async def get_ws_stats(
    current_user: User = Depends(get_current_user_dependency),
) -> dict:
    """Get WebSocket connection statistics (admin only)."""
    from app.db.models import UserRole

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    manager = get_connection_manager()
    return {
        "active_connections": manager.get_connection_count(),
        "total_subscriptions": manager.get_subscription_count(),
        "symbols_tracked": len(manager.symbol_subscribers),
    }


# Import logger
import logging
logger = logging.getLogger(__name__)