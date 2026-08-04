import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  BarChart3,
  Activity,
  LineChart,
  Brain,
  RefreshCw,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { TradingChart } from "@/components/charts/TradingChart";
import { cn } from "@/utils";

const TIMEFRAMES = ["1h", "4h", "1d", "1w"] as const;
const SYMBOLS = [
  { symbol: "BTC/USDT", name: "Bitcoin" },
  { symbol: "ETH/USDT", name: "Ethereum" },
  { symbol: "SOL/USDT", name: "Solana" },
];

export function AnalyticsPage() {
  const { t } = useTranslation();
  const [selectedSymbol, setSelectedSymbol] = useState("BTC/USDT");
  const [timeframe, setTimeframe] = useState<string>("1d");
  const [chartData, setChartData] = useState<any[]>([]);
  const [indicators, setIndicators] = useState<any>(null);
  const [patterns, setPatterns] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"chart" | "patterns" | "fundamental" | "sentiment">("chart");

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        const ohlcvData = await api.getOHLCV({
          symbol: selectedSymbol,
          timeframe,
          limit: 200,
        });
        setChartData(ohlcvData.items || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [selectedSymbol, timeframe]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("analytics.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400">{t("app.tagline")}</p>
      </div>

      {/* Controls */}
      <div className="card p-4">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            {SYMBOLS.map((s) => (
              <button
                key={s.symbol}
                onClick={() => setSelectedSymbol(s.symbol)}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                  selectedSymbol === s.symbol
                    ? "bg-primary-600 text-white"
                    : "bg-surface-100 dark:bg-surface-700 text-surface-700 dark:text-surface-300 hover:bg-surface-200"
                )}
              >
                {s.symbol}
              </button>
            ))}
          </div>
          <div className="w-px h-6 bg-surface-200 dark:bg-surface-700" />
          <div className="flex items-center gap-2">
            {TIMEFRAMES.map((tf) => (
              <button
                key={tf}
                onClick={() => setTimeframe(tf)}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
                  timeframe === tf
                    ? "bg-primary-600 text-white"
                    : "bg-surface-100 dark:bg-surface-700 text-surface-700 dark:text-surface-300 hover:bg-surface-200"
                )}
              >
                {tf}
              </button>
            ))}
          </div>
          <div className="flex-1" />
          <button
            onClick={() => setIsAnalyzing(!isAnalyzing)}
            className="btn-secondary btn-sm"
          >
            <RefreshCw className={cn("h-4 w-4", isAnalyzing && "animate-spin")} />
            {t("analytics.analyze")}
          </button>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="card p-1">
        <div className="flex">
          {(["chart", "patterns", "fundamental", "sentiment"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={cn(
                "flex-1 py-2.5 px-4 rounded-lg text-sm font-medium transition-colors capitalize",
                activeTab === tab
                  ? "bg-primary-600 text-white"
                  : "text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700"
              )}
            >
              {t(`analytics.${tab}`)}
            </button>
          ))}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Chart */}
        <div className="card p-6 lg:col-span-3">
          <TradingChart data={chartData} height={500} showVolume />
        </div>

        {/* Side Panel */}
        <div className="space-y-6">
          {/* Quick Indicators */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Activity className="h-5 w-5 text-primary-600" />
              {t("analytics.indicators")}
            </h2>
            <div className="space-y-3">
              <IndicatorRow label="RSI (14)" value="52.4" color="text-green-600" />
              <IndicatorRow label="MACD" value="Bullish" color="text-green-600" />
              <IndicatorRow label="SMA (20)" value="48,320" />
              <IndicatorRow label="SMA (50)" value="46,150" />
              <IndicatorRow label="Bollinger" value="Mid" />
              <IndicatorRow label="Volume" value="2.4M" color="text-blue-600" />
            </div>
          </div>

          {/* Patterns */}
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Brain className="h-5 w-5 text-purple-600" />
              {t("analytics.patterns")}
            </h2>
            <div className="space-y-2">
              <p className="text-sm text-surface-500 dark:text-surface-400">{t("app.coming_soon")}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function IndicatorRow({ label, value, color }: { label: string; value: string; color?: string }) {
  return (
    <div className="flex items-center justify-between py-1 border-b border-surface-100 dark:border-surface-700 last:border-0">
      <span className="text-sm text-surface-500 dark:text-surface-400">{label}</span>
      <span className={cn("text-sm font-medium text-surface-900 dark:text-surface-50", color)}>{value}</span>
    </div>
  );
}