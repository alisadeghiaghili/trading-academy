import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  TrendingUp,
  ArrowUpDown,
  DollarSign,
  PieChart,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { formatCurrency, formatPercent, cn } from "@/utils";

const MAJOR_SYMBOLS = [
  { symbol: "BTC/USDT", name: "Bitcoin" },
  { symbol: "ETH/USDT", name: "Ethereum" },
  { symbol: "SOL/USDT", name: "Solana" },
  { symbol: "BNB/USDT", name: "BNB" },
  { symbol: "ADA/USDT", name: "Cardano" },
  { symbol: "XRP/USDT", name: "Ripple" },
  { symbol: "DOT/USDT", name: "Polkadot" },
  { symbol: "DOGE/USDT", name: "Dogecoin" },
  { symbol: "LINK/USDT", name: "Chainlink" },
  { symbol: "AVAX/USDT", name: "Avalanche" },
];

export function TradingPage() {
  const { t } = useTranslation();
  const { user } = useAppStore();
  const [trades, setTrades] = useState<any[]>([]);
  const [tradeStats, setTradeStats] = useState<any>(null);
  const [selectedSymbol, setSelectedSymbol] = useState("BTC/USDT");
  const [orderSide, setOrderSide] = useState<"buy" | "sell">("buy");
  const [orderType, setOrderType] = useState<"market" | "limit" | "stop">("market");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");
  const [stopPrice, setStopPrice] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadTrades = async () => {
      setIsLoading(true);
      try {
        const [tradesData, statsData] = await Promise.all([
          api.getTrades({ pageSize: 20 }),
          api.getTradeStats(),
        ]);
        setTrades(tradesData.items || []);
        setTradeStats(statsData);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadTrades();
  }, []);

  const handlePlaceOrder = async () => {
    setIsSubmitting(true);
    try {
      const orderData: any = {
        symbol: selectedSymbol,
        side: orderSide,
        order_type: orderType,
        quantity: parseFloat(quantity),
      };
      if (orderType !== "market") {
        orderData.price = parseFloat(price);
      }
      if (orderType === "stop") {
        orderData.stop_price = parseFloat(stopPrice);
      }
      await api.createTrade(orderData);
      // Refresh trades
      const [tradesData, statsData] = await Promise.all([
        api.getTrades({ pageSize: 20 }),
        api.getTradeStats(),
      ]);
      setTrades(tradesData.items || []);
      setTradeStats(statsData);
      setQuantity("");
      setPrice("");
      setStopPrice("");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("trading.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400">{t("app.tagline")}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Order Entry Panel */}
        <div className="card p-6 space-y-6 lg:col-span-1">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("trading.title")}</h2>
            <div className="flex items-center gap-2 text-sm text-surface-500">
              <DollarSign className="h-4 w-4" />
              <span>{formatCurrency(tradeStats?.totalPnl || 0)}</span>
            </div>
          </div>

          {/* Symbol Selector */}
          <div>
            <label className="label">{t("trading.symbol")}</label>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="input"
            >
              {MAJOR_SYMBOLS.map((s) => (
                <option key={s.symbol} value={s.symbol}>{s.symbol} - {s.name}</option>
              ))}
            </select>
          </div>

          {/* Side Toggle */}
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => setOrderSide("buy")}
              className={cn(
                "py-3 rounded-lg font-semibold transition-colors",
                orderSide === "buy"
                  ? "bg-green-600 text-white"
                  : "bg-surface-100 dark:bg-surface-700 text-surface-600 dark:text-surface-300"
              )}
            >
              {t("trading.buy")}
            </button>
            <button
              onClick={() => setOrderSide("sell")}
              className={cn(
                "py-3 rounded-lg font-semibold transition-colors",
                orderSide === "sell"
                  ? "bg-red-600 text-white"
                  : "bg-surface-100 dark:bg-surface-700 text-surface-600 dark:text-surface-300"
              )}
            >
              {t("trading.sell")}
            </button>
          </div>

          {/* Order Type */}
          <div>
            <label className="label">{t("trading.order_type")}</label>
            <select
              value={orderType}
              onChange={(e) => setOrderType(e.target.value as any)}
              className="input"
            >
              <option value="market">{t("trading.market")}</option>
              <option value="limit">{t("trading.limit")}</option>
              <option value="stop">{t("trading.stop")}</option>
            </select>
          </div>

          {/* Quantity */}
          <div>
            <label className="label">{t("trading.qty")}</label>
            <input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              className="input"
              placeholder="0.001"
              step="0.001"
              min="0"
            />
          </div>

          {/* Price (for limit/stop) */}
          {orderType !== "market" && (
            <div>
              <label className="label">{t("trading.price")}</label>
              <input
                type="number"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                className="input"
                placeholder="50000"
                min="0"
              />
            </div>
          )}

          {/* Stop Price */}
          {orderType === "stop" && (
            <div>
              <label className="label">{t("trading.stop_price")}</label>
              <input
                type="number"
                value={stopPrice}
                onChange={(e) => setStopPrice(e.target.value)}
                className="input"
                placeholder="49000"
                min="0"
              />
            </div>
          )}

          {/* Place Order Button */}
          <button
            onClick={handlePlaceOrder}
            disabled={isSubmitting || !quantity}
            className={cn(
              "w-full py-3 rounded-lg font-bold text-white transition-colors",
              orderSide === "buy"
                ? "bg-green-600 hover:bg-green-700"
                : "bg-red-600 hover:bg-red-700",
              (isSubmitting || !quantity) && "opacity-50 cursor-not-allowed"
            )}
          >
            {isSubmitting ? (
              <span className="spinner spinner-sm" />
            ) : (
              `${orderSide === "buy" ? t("trading.buy") : t("trading.sell")} ${selectedSymbol}`
            )}
          </button>
        </div>

        {/* Trade History + Stats */}
        <div className="lg:col-span-2 space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="card p-4 text-center">
              <p className="text-sm text-surface-500">{t("trading.pnl")}</p>
              <p className={cn("text-xl font-bold", (tradeStats?.totalPnl || 0) >= 0 ? "text-green-600" : "text-red-600")}>
                {formatCurrency(tradeStats?.totalPnl || 0)}
              </p>
            </div>
            <div className="card p-4 text-center">
              <p className="text-sm text-surface-500">{t("portfolio.win_rate")}</p>
              <p className="text-xl font-bold text-surface-900 dark:text-surface-50">{formatPercent(tradeStats?.winRate || 0)}</p>
            </div>
            <div className="card p-4 text-center">
              <p className="text-sm text-surface-500">{t("trades")}</p>
              <p className="text-xl font-bold text-surface-900 dark:text-surface-50">{tradeStats?.totalTrades || 0}</p>
            </div>
            <div className="card p-4 text-center">
              <p className="text-sm text-surface-500">{t("open")}</p>
              <p className="text-xl font-bold text-surface-900 dark:text-surface-50">{tradeStats?.openTrades || 0}</p>
            </div>
          </div>

          {/* Trade History Table */}
          <div className="card overflow-hidden">
            <div className="p-4 border-b border-surface-200 dark:border-surface-700">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("trading.trade_history")}</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-surface-50 dark:bg-surface-800/50">
                  <tr>
                    <th className="text-left p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.time")}</th>
                    <th className="text-left p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.symbol")}</th>
                    <th className="text-left p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.side")}</th>
                    <th className="text-right p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.qty")}</th>
                    <th className="text-right p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.price")}</th>
                    <th className="text-right p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.pnl")}</th>
                    <th className="text-center p-3 font-medium text-surface-600 dark:text-surface-400">{t("trading.status")}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-surface-200 dark:divide-surface-700">
                  {trades.map((trade: any) => (
                    <tr key={trade.id} className="hover:bg-surface-50 dark:hover:bg-surface-700/50">
                      <td className="p-3 text-surface-600 dark:text-surface-400">
                        {new Date(trade.createdAt || trade.created_at).toLocaleDateString()}
                      </td>
                      <td className="p-3 font-medium text-surface-900 dark:text-surface-50">{trade.symbol}</td>
                      <td className="p-3">
                        <span className={cn(
                          "badge",
                          trade.side === "buy" ? "badge-green" : "badge-red"
                        )}>
                          {trade.side}
                        </span>
                      </td>
                      <td className="p-3 text-right text-surface-900 dark:text-surface-50">{trade.quantity}</td>
                      <td className="p-3 text-right text-surface-900 dark:text-surface-50">
                        {trade.filledPrice ? formatCurrency(trade.filledPrice) : "-"}
                      </td>
                      <td className={cn("p-3 text-right font-medium", trade.pnl >= 0 ? "text-green-600" : "text-red-600")}>
                        {formatCurrency(trade.pnl)}
                      </td>
                      <td className="p-3 text-center">
                        <span className={cn(
                          "badge",
                          trade.status === "filled" ? "badge-green" :
                          trade.status === "pending" ? "badge-yellow" :
                          trade.status === "cancelled" ? "badge-gray" : "badge-blue"
                        )}>
                          {trade.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {trades.length === 0 && (
                <div className="p-8 text-center text-surface-500 dark:text-surface-400">
                  <ArrowUpDown className="h-12 w-12 mx-auto mb-3 text-surface-300 dark:text-surface-600" />
                  <p>{t("trading.no_trades")}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}