import { useEffect, useRef, useCallback, useState } from "react";

type MessageHandler = (data: any) => void;
type ConnectionStatus = "disconnected" | "connecting" | "connected";

interface UseWebSocketOptions {
  url: string;
  autoConnect?: boolean;
  reconnectInterval?: number;
  maxReconnects?: number;
  authToken?: string;
  heartbeatInterval?: number;
}

export function useWebSocket({
  url,
  autoConnect = true,
  reconnectInterval = 5000,
  maxReconnects = 10,
  authToken,
  heartbeatInterval = 30000,
}: UseWebSocketOptions) {
  const [status, setStatus] = useState<ConnectionStatus>("disconnected");
  const [lastMessage, setLastMessage] = useState<any>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const handlersRef = useRef<Map<string, Set<MessageHandler>>>(new Map());
  const reconnectCountRef = useRef(0);
  const heartbeatRef = useRef<ReturnType<typeof setInterval>>();
  const mountedRef = useRef(true);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    setStatus("connecting");
    const wsUrl = authToken ? `${url}?token=${authToken}` : url;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      setStatus("connected");
      reconnectCountRef.current = 0;

      // Start heartbeat
      heartbeatRef.current = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "ping" }));
        }
      }, heartbeatInterval);
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        setLastMessage(message);

        // Dispatch to handlers
        const typeHandlers = handlersRef.current.get(message.type);
        if (typeHandlers) {
          typeHandlers.forEach((handler) => handler(message.data));
        }

        // Dispatch to wildcard handlers
        const wildcardHandlers = handlersRef.current.get("*");
        if (wildcardHandlers) {
          wildcardHandlers.forEach((handler) => handler(message));
        }
      } catch (e) {
        console.error("WebSocket message parse error:", e);
      }
    };

    ws.onerror = () => {
      setStatus("disconnected");
    };

    ws.onclose = () => {
      setStatus("disconnected");
      if (heartbeatRef.current) {
        clearInterval(heartbeatRef.current);
      }

      // Reconnect
      if (mountedRef.current && reconnectCountRef.current < maxReconnects) {
        reconnectCountRef.current++;
        setTimeout(connect, reconnectInterval);
      }
    };

    wsRef.current = ws;
  }, [url, authToken, reconnectInterval, maxReconnects, heartbeatInterval]);

  const disconnect = useCallback(() => {
    mountedRef.current = false;
    if (heartbeatRef.current) {
      clearInterval(heartbeatRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setStatus("disconnected");
  }, []);

  const subscribe = useCallback(
    (type: string, handler: MessageHandler) => {
      if (!handlersRef.current.has(type)) {
        handlersRef.current.set(type, new Set());
      }
      handlersRef.current.get(type)!.add(handler);

      return () => {
        handlersRef.current.get(type)?.delete(handler);
      };
    },
    []
  );

  const send = useCallback((message: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  const subscribeToSymbol = useCallback(
    (symbols: string[], type: string = "ticker", timeframe?: string) => {
      send({
        action: "subscribe",
        type,
        symbols: Array.isArray(symbols) ? symbols : [symbols],
        timeframe,
      });
    },
    [send]
  );

  const unsubscribeFromSymbol = useCallback(
    (symbols: string[], type: string = "ticker") => {
      send({
        action: "unsubscribe",
        type,
        symbols: Array.isArray(symbols) ? symbols : [symbols],
      });
    },
    [send]
  );

  useEffect(() => {
    mountedRef.current = true;
    if (autoConnect) {
      connect();
    }
    return () => {
      mountedRef.current = false;
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    status,
    lastMessage,
    connect,
    disconnect,
    subscribe,
    send,
    subscribeToSymbol,
    unsubscribeFromSymbol,
  };
}