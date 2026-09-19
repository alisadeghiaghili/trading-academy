import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Trophy,
  Flame,
  Star,
  Zap,
  Target,
  Award,
  Crown,
  Gift,
  TrendingUp,
  BookOpen,
  Brain,
} from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { cn } from "@/utils";

export function GamificationPage() {
  const { t } = useTranslation();
  const { user } = useAppStore();
  const [profile, setProfile] = useState<any>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);
  const [challenges, setChallenges] = useState<any[]>([]);
  const [badges, setBadges] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "challenges" | "badges" | "leaderboard">("overview");

  useEffect(() => {
    const loadGamification = async () => {
      setIsLoading(true);
      try {
        const profileData = await api.getGamificationProfile();
        setProfile(profileData);

        const lbData = await api.getLeaderboard("xp", "weekly");
        setLeaderboard(lbData.entries || []);

        setChallenges(profileData.challenges || []);
        setBadges(profileData.badges || []);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadGamification();
  }, []);

  const claimDailyReward = async () => {
    try {
      const result = await api.trackDailyLogin();
      if (result.is_new_login) {
        const profileData = await api.getGamificationProfile();
        setProfile(profileData);
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  const xp = profile?.xp || { total_xp: 0, current_level: 1, level_title: "beginner", xp_to_next_level: 100, progress_pct: 0 };
  const streaks = profile?.streaks || { login_streak: 0, longest_login_streak: 0 };
  const stats = profile?.stats || { lessons_completed: 0, quizzes_passed: 0, trades_completed: 0 };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("gamification.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400">{t("gamification.subtitle")}</p>
      </div>

      {/* XP & Level Card */}
      <div className="card p-6 bg-gradient-to-br from-primary-600 to-primary-800 text-white">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-white/20 flex items-center justify-center text-3xl">
              {xp.current_level >= 15 ? "👑" : xp.current_level >= 10 ? "🌟" : xp.current_level >= 5 ? "⭐" : "🎯"}
            </div>
            <div>
              <h2 className="text-2xl font-bold">{t(`gamification.levels.${xp.level_title}`)}</h2>
              <p className="text-primary-100">{t("gamification.level")} {xp.current_level}</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold">{xp.total_xp.toLocaleString()}</p>
            <p className="text-primary-200 text-sm">XP</p>
          </div>
        </div>

        {/* XP Progress Bar */}
        <div className="mb-2">
          <div className="flex justify-between text-sm mb-1">
            <span>{t("gamification.progress")}</span>
            <span>{xp.xp_to_next_level} XP {t("gamification.to_next_level")}</span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-3">
            <div
              className="bg-white rounded-full h-3 transition-all duration-500"
              style={{ width: `${xp.progress_pct}%` }}
            />
          </div>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="card p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <Flame className="h-6 w-6 text-orange-500" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{streaks.login_streak}</p>
          <p className="text-sm text-surface-500">{t("gamification.day_streak")}</p>
        </div>
        <div className="card p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <BookOpen className="h-6 w-6 text-blue-500" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{stats.lessons_completed}</p>
          <p className="text-sm text-surface-500">{t("gamification.lessons_done")}</p>
        </div>
        <div className="card p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <Brain className="h-6 w-6 text-purple-500" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{stats.quizzes_passed}</p>
          <p className="text-sm text-surface-500">{t("gamification.quizzes_passed")}</p>
        </div>
        <div className="card p-4 text-center">
          <div className="flex items-center justify-center mb-2">
            <TrendingUp className="h-6 w-6 text-green-500" />
          </div>
          <p className="text-2xl font-bold text-surface-900 dark:text-surface-50">{stats.trades_completed}</p>
          <p className="text-sm text-surface-500">{t("gamification.trades_done")}</p>
        </div>
      </div>

      {/* Daily Reward */}
      {!profile?.daily_reward_claimed && (
        <div className="card p-4 border-2 border-yellow-400 bg-yellow-50 dark:bg-yellow-900/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Gift className="h-8 w-8 text-yellow-500" />
              <div>
                <p className="font-semibold text-surface-900 dark:text-surface-50">{t("gamification.daily_reward")}</p>
                <p className="text-sm text-surface-600 dark:text-surface-400">{t("gamification.claim_daily")}</p>
              </div>
            </div>
            <button onClick={claimDailyReward} className="btn-primary">
              {t("gamification.claim")}
            </button>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="card p-1">
        <div className="flex">
          {(["overview", "challenges", "badges", "leaderboard"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={cn(
                "flex-1 py-2.5 px-4 rounded-lg text-sm font-medium transition-colors",
                activeTab === tab
                  ? "bg-primary-600 text-white"
                  : "text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700"
              )}
            >
              {t(`gamification.tabs.${tab}`)}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === "overview" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Active Challenges Preview */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Target className="h-5 w-5 text-primary-600" />
              {t("gamification.daily_challenges")}
            </h3>
            <div className="space-y-3">
              {challenges.slice(0, 3).map((challenge: any) => (
                <ChallengeCard key={challenge.id} challenge={challenge} />
              ))}
              {challenges.length === 0 && (
                <p className="text-surface-500 text-center py-4">{t("app.coming_soon")}</p>
              )}
            </div>
          </div>

          {/* Recent Badges Preview */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-4 flex items-center gap-2">
              <Award className="h-5 w-5 text-yellow-500" />
              {t("gamification.your_badges")}
            </h3>
            <div className="flex flex-wrap gap-3">
              {badges.filter((b: any) => b.earned).slice(0, 8).map((badge: any) => (
                <div
                  key={badge.id}
                  className="w-14 h-14 rounded-xl bg-surface-100 dark:bg-surface-700 flex items-center justify-center text-2xl"
                  title={badge.name?.en || badge.code}
                >
                  {badge.icon_emoji || "🏅"}
                </div>
              ))}
              {badges.filter((b: any) => b.earned).length === 0 && (
                <p className="text-surface-500 w-full text-center py-4">{t("gamification.no_badges_yet")}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === "challenges" && (
        <div className="space-y-4">
          {challenges.map((challenge: any) => (
            <ChallengeCard key={challenge.id} challenge={challenge} full />
          ))}
          {challenges.length === 0 && (
            <div className="card p-8 text-center">
              <Target className="h-12 w-12 text-surface-300 mx-auto mb-3" />
              <p className="text-surface-500">{t("app.coming_soon")}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === "badges" && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {badges.map((badge: any) => (
            <div
              key={badge.id}
              className={cn(
                "card p-4 text-center",
                !badge.earned && "opacity-40 grayscale"
              )}
            >
              <div className="text-4xl mb-2">{badge.icon_emoji || "🏅"}</div>
              <p className="text-sm font-medium text-surface-900 dark:text-surface-50 mb-1">
                {badge.name?.en || badge.code}
              </p>
              <span className={cn(
                "badge text-xs",
                badge.tier === "diamond" ? "bg-cyan-100 text-cyan-700" :
                badge.tier === "platinum" ? "bg-purple-100 text-purple-700" :
                badge.tier === "gold" ? "bg-yellow-100 text-yellow-700" :
                badge.tier === "silver" ? "bg-gray-100 text-gray-700" :
                "bg-orange-100 text-orange-700"
              )}>
                {badge.tier}
              </span>
            </div>
          ))}
        </div>
      )}

      {activeTab === "leaderboard" && (
        <div className="card overflow-hidden">
          <div className="p-4 border-b border-surface-200 dark:border-surface-700">
            <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-50 flex items-center gap-2">
              <Crown className="h-5 w-5 text-yellow-500" />
              {t("gamification.leaderboard")} - {t("gamification.this_week")}
            </h3>
          </div>
          <div className="divide-y divide-surface-200 dark:divide-surface-700">
            {leaderboard.map((entry: any) => (
              <div
                key={entry.user_id}
                className={cn(
                  "flex items-center gap-4 p-4",
                  entry.user_id === user?.id && "bg-primary-50 dark:bg-primary-900/20"
                )}
              >
                <div className={cn(
                  "w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm",
                  entry.rank === 1 ? "bg-yellow-400 text-white" :
                  entry.rank === 2 ? "bg-gray-300 text-gray-700" :
                  entry.rank === 3 ? "bg-orange-400 text-white" :
                  "bg-surface-200 dark:bg-surface-700 text-surface-600 dark:text-surface-400"
                )}>
                  {entry.rank}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium text-surface-900 dark:text-surface-50 truncate">
                    {entry.display_name}
                    {entry.user_id === user?.id && (
                      <span className="text-primary-600 text-sm ml-2">({t("gamification.you")})</span>
                    )}
                  </p>
                  <p className="text-sm text-surface-500">
                    {t(`gamification.levels.${entry.level_title}`)} · Level {entry.level}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-surface-900 dark:text-surface-50">{entry.score.toLocaleString()}</p>
                  <p className="text-sm text-surface-500">XP</p>
                </div>
              </div>
            ))}
            {leaderboard.length === 0 && (
              <div className="p-8 text-center text-surface-500">
                <Trophy className="h-12 w-12 mx-auto mb-3 text-surface-300" />
                <p>{t("app.coming_soon")}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function ChallengeCard({ challenge, full }: { challenge: any; full?: boolean }) {
  const { t } = useTranslation();
  const progressPct = challenge.target > 0 ? Math.round((challenge.progress / challenge.target) * 100) : 0;

  return (
    <div className={cn(
      "card p-4",
      challenge.is_completed && "border-green-300 bg-green-50 dark:bg-green-900/20"
    )}>
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          {challenge.is_completed ? (
            <span className="text-green-500 text-xl">✅</span>
          ) : (
            <Target className="h-5 w-5 text-primary-600" />
          )}
          <div>
            <p className="font-medium text-surface-900 dark:text-surface-50">
              {challenge.title?.en || challenge.type}
            </p>
            <p className="text-sm text-surface-500">
              {challenge.description?.en}
            </p>
          </div>
        </div>
        <div className="text-right flex-shrink-0">
          <p className="text-sm font-bold text-primary-600">+{challenge.xp_reward} XP</p>
        </div>
      </div>
      <div className="mt-3">
        <div className="flex justify-between text-sm mb-1">
          <span className="text-surface-500">{challenge.progress}/{challenge.target}</span>
          <span className="text-surface-500">{progressPct}%</span>
        </div>
        <div className="w-full bg-surface-200 dark:bg-surface-700 rounded-full h-2">
          <div
            className={cn(
              "rounded-full h-2 transition-all duration-500",
              challenge.is_completed ? "bg-green-500" : "bg-primary-600"
            )}
            style={{ width: `${Math.min(progressPct, 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
}