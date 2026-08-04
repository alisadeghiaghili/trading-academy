"""WebSocket manager for real-time market data streaming."""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SubscriptionType(str, Enum):
    """WebSocket subscription types."""

    TICKER = "ticker"
    OHLCV = "ohlcv"
    ORDER_BOOK = "order_book"
    TRADES = "trades"
    MARKET_SUMMARY = "market_summary"


@dataclass
class Subscription:
    """Client subscription."""

    client_id: str
    subscription_type: SubscriptionType
    symbols: List[str]
    timeframe: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ConnectionManager:
    """Manages WebSocket connections and subscriptions."""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.subscriptions: Dict[str, List[Subscription]] = {}
        self.symbol_subscribers: Dict[str, Set[str]] = {}  # symbol -> set of client_ids
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """Accept new WebSocket connection."""
        await websocket.accept()
        async with self._lock:
            self.active_connections[client_id] = websocket
            self.subscriptions[client_id] = []
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

    async def disconnect(self, client_id: str) -> None:
        """Remove WebSocket connection."""
        async with self._lock:
            # Remove from symbol subscribers
            for symbol, subscribers in self.symbol_subscribers.items():
                subscribers.discard(client_id)

            self.active_connections.pop(client_id, None)
            self.subscriptions.pop(client_id, None)
        logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def subscribe(
        self,
        client_id: str,
        subscription_type: SubscriptionType,
        symbols: List[str],
        timeframe: Optional[str] = None,
    ) -> bool:
        """Subscribe client to market data."""
        if client_id not in self.active_connections:
            return False

        async with self._lock:
            subscription = Subscription(
                client_id=client_id,
                subscription_type=subscription_type,
                symbols=symbols,
                timeframe=timeframe,
            )
            self.subscriptions[client_id].append(subscription)

            for symbol in symbols:
                if symbol not in self.symbol_subscribers:
                    self.symbol_subscribers[symbol] = set()
                self.symbol_subscribers[symbol].add(client_id)

        logger.info(f"Client {client_id} subscribed to {subscription_type.value} for {symbols}")
        return True

    async def unsubscribe(
        self,
        client_id: str,
        subscription_type: SubscriptionType,
        symbols: List[str],
    ) -> bool:
        """Unsubscribe client from market data."""
        if client_id not in self.subscriptions:
            return False

        async with self._lock:
            # Remove matching subscriptions
            self.subscriptions[client_id] = [
                s for s in self.subscriptions[client_id]
                if not (s.subscription_type == subscription_type and set(s.symbols) & set(symbols))
            ]

            # Update symbol subscribers
            for symbol in symbols:
                if symbol in self.symbol_subscribers:
                    self.symbol_subscribers[symbol].discard(client_id)

        return True

    async def get_subscribers(self, symbol: str) -> Set[str]:
        """Get all client IDs subscribed to a symbol."""
        async with self._lock:
            return self.symbol_subscribers.get(symbol, set()).copy()

    async def broadcast_to_symbol(
        self,
        symbol: str,
        message: dict,
        subscription_type: Optional[SubscriptionType] = None,
    ) -> int:
        """Broadcast message to all subscribers of a symbol."""
        subscribers = await self.get_subscribers(symbol)
        sent = 0

        for client_id in subscribers:
            # Check if client has matching subscription type
            if subscription_type:
                client_subs = self.subscriptions.get(client_id, [])
                has_sub = any(
                    s.subscription_type == subscription_type and symbol in s.symbols
                    for s in client_subs
                )
                if not has_sub:
                    continue

            await self.send_personal_message(client_id, message)
            sent += 1

        return sent

    async def send_personal_message(self, client_id: str, message: dict) -> bool:
        """Send message to specific client."""
        websocket = self.active_connections.get(client_id)
        if not websocket:
            return False

        try:
            await websocket.send_json(message)
            return True
        except Exception as e:
            logger.error(f"Error sending to {client_id}: {e}")
            await self.disconnect(client_id)
            return False

    async def broadcast(self, message: dict) -> int:
        """Broadcast message to all connected clients."""
        sent = 0
        for client_id in list(self.active_connections.keys()):
            if await self.send_personal_message(client_id, message):
                sent += 1
        return sent

    def get_connection_count(self) -> int:
        """Get total active connections."""
        return len(self.active_connections)

    def get_subscription_count(self) -> int:
        """Get total active subscriptions."""
        return sum(len(subs) for subs in self.subscriptions.values())


# Message models
class WSMessage(BaseModel):
    """Base WebSocket message."""

    type: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    data: dict


class TickerMessage(WSMessage):
    """Real-time ticker update."""

    type: str = "ticker"
    data: dict  # {symbol, price, change_24h, change_24h_pct, volume_24h, high_24h, low_24h}


class OHLCVMessage(WSMessage):
    """Real-time OHLCV update."""

    type: str = "ohlcv"
    data: dict  # {symbol, timeframe, timestamp, open, high, low, close, volume, is_final}


class OrderBookMessage(WSMessage):
    """Order book update."""

    type: str = "order_book"
    data: dict  # {symbol, bids: [[price, qty]], asks: [[price, qty]], timestamp}


class TradeMessage(WSMessage):
    """Recent trade update."""

    type: str = "trade"
    data: dict  # {symbol, price, quantity, side, timestamp, trade_id}


class SubscriptionMessage(WSMessage):
    """Subscription confirmation."""

    type: str = "subscription"
    data: dict  # {action: "subscribed"/"unsubscribed", subscription_type, symbols, timeframe}


class ErrorMessage(WSMessage):
    """Error message."""

    type: str = "error"
    data: dict  # {code, message}


class HeartbeatMessage(WSMessage):
    """Heartbeat/ping message."""

    type: str = "heartbeat"
    data: dict = field(default_factory=dict)


# Global connection manager
_connection_manager: Optional[ConnectionManager] = None


def get_connection_manager() -> ConnectionManager:
    """Get global connection manager instance."""
    global _connection_manager
    if _connection_manager is None:
        _connection_manager = ConnectionManager()
    return _connection_manager