import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import {
  BookOpen,
  LineChart,
  Briefcase,
  TrendingUp,
  Target,
  Award,
  Clock,
  BarChart3,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { formatCurrency, formatPercent, formatTimeAgo, cn } from "@/utils";

export function DashboardPage() {
  const { t } = useTranslation();
  const { fetchModules, fetchTradeStats, fetchProgressSummary, fetchCoachingAnalysis, modules, tradeStats, progressSummary, coachingAnalysis } = useAppStore();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      try {
        await Promise.all([
          fetchModules(),
          fetchTradeStats(),
          fetchProgressSummary(),
          fetchCoachingAnalysis(),
        ]);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [fetchModules, fetchTradeStats, fetchProgressSummary, fetchCoachingAnalysis]);

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  const stats = [
    {
      label: t("modules.lessons"),
      value: progressSummary?.totalLessons || 0,
      icon: <BookOpen className="h-6 w-6" />,
      color: "text-blue-600 bg-blue-100",
    },
    {
      label: t("portfolio.value"),
      value: formatCurrency((tradeStats?.totalPnl || 0) + 10000),
      icon: <Briefcase className="h-6 w-6" />,
      color: "text-green-600 bg-green-100",
    },
    {
      label: t("portfolio.total_return"),
      value: formatPercent(tradeStats?.totalPnl || 0, 2),
      icon: <TrendingUp className="h-6 w-6" />,
      color: "text-purple-600 bg-purple-100",
    },
    {
      label: t("portfolio.win_rate"),
      value: formatPercent(tradeStats?.winRate || 0),
      icon: <Target className="h-6 w-6" />,
      color: "text-orange-600 bg-orange-100",
    },
  ];

  const recentModules = modules.slice(0, 4).map((module) => {
    const moduleProgress = progressSummary;
    return (
      <Link
        key={module.id}
        to={`/modules/${module.id}`}
        className="card-hover p-4 flex items-center gap-4"
      >
        <div className="w-12 h-12 rounded-xl bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center">
          <BookOpen className="h-6 w-6 text-primary-600" />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-surface-900 dark:text-surface-50 truncate">{module.title}</h4>
          <p className="text-sm text-surface-500 dark:text-surface-400">
            {module.lessonsCount} {t("modules.lessons")} · {module.order}
          </p>
        </div>
        <BarChart3 className="h-5 w-5 text-surface-400" />
      </Link>
    );
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("nav.dashboard")}</h1>
          <p className="text-surface-600 dark:text-surface-400">{t("app.tagline")}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => (
          <div key={i} className="card p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-surface-500 dark:text-surface-400">{stat.label}</p>
                <p className="text-2xl font-bold text-surface-900 dark:text-surface-50 mt-1">{stat.value}</p>
              </div>
              <div className={cn("p-3 rounded-xl", stat.color, "dark:bg-opacity-20")}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("modules.title")}</h2>
            <Link to="/modules" className="text-sm text-primary-600 hover:underline">{t("app.view_all")}</Link>
          </div>
          <div className="space-y-3">
            {recentModules.length > 0 ? (
              recentModules
            ) : (
              <p className="text-center text-surface-500 dark:text-surface-400 py-8">{t("app.no_data")}</p>
            )}
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("trading.title")}</h2>
            <Link to="/trading" className="text-sm text-primary-600 hover:underline">{t("app.view_all")}</Link>
          </div>
          <div className="space-y-4">
            <div className="grid grid-cols-4 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{tradeStats?.totalTrades || 0}</p>
                <p className="text-sm text-surface-500">{t("trading.trade_history")}</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-600">{tradeStats?.winningTrades || 0}</p>
                <p className="text-sm text-surface-500">{t("trading.trade_history")}</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-600">{tradeStats?.losingTrades || 0}</p>
                <p className="text-sm text-surface-500">{t("trading.trade_history")}</p>
              </div>
              <div>
                <p className="text-2xl font-bold {tradeStats?.totalPnl >= 0 ? 'text-green-600' : 'text-red-600'}">
                  {formatCurrency(tradeStats?.totalPnl || 0)}
                </p>
                <p className="text-sm text-surface-500">{t("trading.pnl")}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}