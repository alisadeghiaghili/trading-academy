import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  MessageSquare,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Brain,
  Lightbulb,
  BookOpen,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { cn, formatCurrency, formatPercent } from "@/utils";

export function CoachingPage() {
  const { t } = useTranslation();
  const { user } = useAppStore();
  const [analysis, setAnalysis] = useState<any>(null);
  const [feedback, setFeedback] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [trades, setTrades] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCoachingData = async () => {
      setIsLoading(true);
      try {
        const [tradesData, statsData] = await Promise.all([
          api.getTrades({ pageSize: 50 }),
          api.getTradeStats(),
        ]);
        setTrades(tradesData.items || []);

        // Build analysis from stats
        const stats = statsData;
        if (stats) {
          setAnalysis({
            summary: {
              totalTrades: stats.totalTrades || 0,
              winRate: (stats.winRate || 0) / 100,
              avgWin: stats.bestTrade || 0,
              avgLoss: Math.abs(stats.worstTrade || 0),
              profitFactor: stats.profitFactor || 1,
              maxWinStreak: 0,
              maxLossStreak: 0,
            },
          });

          // Generate feedback
          const feedbackList = [];
          if (stats.winRate < 40) {
            feedbackList.push({
              type: "strategy_adherence",
              severity: "warning",
              message: "Win rate is below 40%. Consider reviewing your entry strategy.",
            });
          }
          if (stats.totalPnl < 0) {
            feedbackList.push({
              type: "risk_management",
              severity: "critical",
              message: "Overall P&L is negative. Review your risk management rules.",
            });
          }
          setFeedback(feedbackList);

          // Recommendations
          setRecommendations([
            {
              lesson_topic: "Risk Management",
              reason: "Improve position sizing and stop-loss discipline",
              priority: "high",
            },
            {
              lesson_topic: "Technical Analysis",
              reason: "Strengthen entry signal identification",
              priority: "high",
            },
            {
              lesson_topic: "Trading Psychology",
              reason: "Build emotional discipline and reduce overtrading",
              priority: "medium",
            },
          ]);
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadCoachingData();
  }, []);

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("coaching.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400">{t("app.tagline")}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Analysis Panel */}
        <div className="card p-6 lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 flex items-center gap-2">
              <Brain className="h-5 w-5 text-primary-600" />
              {t("coaching.pattern")}
            </h2>
            <button className="btn-primary btn-sm">
              {t("coaching.analyze")}
            </button>
          </div>

          {analysis && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="card p-4 text-center">
                <p className="text-sm text-surface-500">{t("portfolio.win_rate")}</p>
                <p className={cn("text-2xl font-bold", (analysis.summary.winRate || 0) >= 0.4 ? "text-green-600" : "text-red-600")}>
                  {formatPercent((analysis.summary.winRate || 0) * 100)}
                </p>
              </div>
              <div className="card p-4 text-center">
                <p className="text-sm text-surface-500">{t("portfolio.profit_factor")}</p>
                <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">
                  {(analysis.summary.profitFactor || 1).toFixed(2)}
                </p>
              </div>
              <div className="card p-4 text-center">
                <p className="text-sm text-surface-500">{t("portfolio.avg_win")}</p>
                <p className="text-2xl font-bold text-green-600">{formatCurrency(analysis.summary.avgWin || 0)}</p>
              </div>
              <div className="card p-4 text-center">
                <p className="text-sm text-surface-500">{t("portfolio.avg_loss")}</p>
                <p className="text-2xl font-bold text-red-600">{formatCurrency(analysis.summary.avgLoss || 0)}</p>
              </div>
            </div>
          )}

          {/* Feedback */}
          {feedback.length > 0 && (
            <div>
              <h3 className="font-medium text-surface-900 dark:text-surface-50 mb-3">{t("coaching.feedback")}</h3>
              <div className="space-y-3">
                {feedback.map((fb, i) => (
                  <div
                    key={i}
                    className={cn(
                      "flex items-start gap-3 p-4 rounded-lg",
                      fb.severity === "critical"
                        ? "bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800"
                        : "bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800"
                    )}
                  >
                    <AlertTriangle className={cn(
                      "h-5 w-5 flex-shrink-0 mt-0.5",
                      fb.severity === "critical" ? "text-red-600" : "text-yellow-600"
                    )} />
                    <p className={cn(
                      "text-sm",
                      fb.severity === "critical"
                        ? "text-red-700 dark:text-red-300"
                        : "text-yellow-700 dark:text-yellow-300"
                    )}>
                      {fb.message}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Recommendations Panel */}
        <div className="space-y-6">
          <div className="card p-6">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Lightbulb className="h-5 w-5 text-yellow-500" />
              {t("coaching.strengths")}
            </h2>
            <div className="flex items-center gap-2 mb-4">
              <div className="text-3xl font-bold text-green-600">B</div>
              <div className="text-sm text-surface-600 dark:text-surface-400">
                <p className="font-medium text-green-600">{t("coaching.discipline")}</p>
                <p>75% - {t("progressing")}</p>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-blue-500" />
              {t("coaching.recommendations")}
            </h2>
            <div className="space-y-3">
              {recommendations.map((rec, i) => (
                <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-surface-50 dark:bg-surface-700/50">
                  <div className="w-8 h-8 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center flex-shrink-0">
                    <BookOpen className="h-4 w-4 text-primary-600" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-surface-900 dark:text-surface-50">{rec.lesson_topic}</p>
                    <p className="text-xs text-surface-500 mt-0.5">{rec.reason}</p>
                    <span className={cn(
                      "text-xs mt-1 inline-block px-2 py-0.5 rounded-full",
                      rec.priority === "high" ? "bg-red-100 dark:bg-red-900/30 text-red-600" : "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600"
                    )}>
                      {rec.priority}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}