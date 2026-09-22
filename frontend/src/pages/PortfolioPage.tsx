import { useEffect, useState, useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  PieChart as PieChartIcon,
  TrendingUp,
  TrendingDown,
  BarChart3,
  Target,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { formatCurrency, formatPercent, cn } from "@/utils";
import { TradingChart } from "@/components/charts/TradingChart";
import { useWebSocket } from "@/hooks/useWebSocket";

const API_WS_URL = import.meta.env.VITE_WS_URL || `ws://${window.location.host}/api/v1/ws/market-data`;

export function PortfolioPage() {
  const { t } = useTranslation();
  const { user } = useAppStore();
  const [trades, setTrades] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPortfolio = async () => {
      setIsLoading(true);
      try {
        const [tradesData, statsData] = await Promise.all([
          api.getTrades({ pageSize: 100 }),
          api.getTradeStats(),
        ]);
        setTrades(tradesData.items || []);
        setStats(statsData);

        // Get chart data
        const ohlcvData = await api.getOHLCV({
          symbol: "BTC/USDT",
          timeframe: "1d",
          limit: 100,
        });
        setChartData(ohlcvData.items || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadPortfolio();
  }, []);

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  const winningTrades = trades.filter(t => t.pnl > 0);
  const losingTrades = trades.filter(t => t.pnl < 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("portfolio.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400">{t("app.tagline")}</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-surface-500">{t("portfolio.value")}</p>
            <PieChartIcon className="h-5 w-5 text-primary-600" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">
            {formatCurrency(10000 + (stats?.totalPnl || 0))}
          </p>
          <p className={cn("text-sm mt-1", (stats?.totalPnl || 0) >= 0 ? "text-green-600" : "text-red-600")}>
            {formatPercent(stats?.totalPnl || 0, 2)}
          </p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-surface-500">{t("portfolio.sharpe")}</p>
            <TrendingUp className="h-5 w-5 text-green-600" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">
            {stats?.sharpeRatio?.toFixed(2) || "N/A"}
          </p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-surface-500">{t("portfolio.max_drawdown")}</p>
            <TrendingDown className="h-5 w-5 text-red-600" />
          </div>
          <p className="text-2xl font-bold text-red-600">
            {stats?.maxDrawdown ? formatPercent(stats.maxDrawdown) : "N/A"}
          </p>
        </div>

        <div className="card p-5">
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm text-surface-500">{t("portfolio.profit_factor")}</p>
            <Target className="h-5 w-5 text-blue-600" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">
            {stats?.profitFactor?.toFixed(2) || "N/A"}
          </p>
        </div>
      </div>

      {/* Chart + Stats Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart */}
        <div className="card p-6 lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">BTC/USDT</h2>
            <div className="flex items-center gap-2">
              <span className="text-sm text-surface-500">1D</span>
            </div>
          </div>
          <TradingChart data={chartData} height={400} showVolume />
        </div>

        {/* Stats */}
        <div className="space-y-6">
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4">{t("analytics.risk_metrics")}</h2>
            <div className="space-y-3">
              <RiskRow label={t("portfolio.win_rate")} value={formatPercent(stats?.winRate || 0)} color={stats?.winRate >= 50 ? "text-green-600" : "text-red-600"} />
              <RiskRow label={t("best_trade")} value={formatCurrency(stats?.bestTrade || 0)} color="text-green-600" />
              <RiskRow label={t("worst_trade")} value={formatCurrency(stats?.worstTrade || 0)} color="text-red-600" />
              <RiskRow label={t("winning_trades")} value={String(stats?.winningTrades || 0)} />
              <RiskRow label={t("losing_trades")} value={String(stats?.losingTrades || 0)} />
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4">{t("analytics.entry")}</h2>
            <div className="space-y-3">
              <RiskRow label={t("total_trades")} value={String(stats?.totalTrades || 0)} />
              <RiskRow label={t("open_trades")} value={String(stats?.openTrades || 0)} />
              <RiskRow label={t("closed_trades")} value={String(stats?.closedTrades || 0)} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function RiskRow({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm text-surface-500">{label}</span>
      <span className={cn("text-sm font-medium text-surface-900 dark:text-surface-50", color)}>{value}</span>
    </div>
  );
}