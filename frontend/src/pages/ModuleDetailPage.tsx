import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { BookOpen, Clock, CheckCircle, PlayCircle, Lock, ChevronRight, Award, TrendingUp } from "lucide-react";
import { useAppStore } from "@/store";
import { api } from "@/services/api";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { cn, formatTimeAgo } from "@/utils";

export function ModuleDetailPage() {
  const { t } = useTranslation();
  const { moduleId } = useParams();
  const { modules, setCurrentModule, fetchModules } = useAppStore();
  const [module, setModule] = useState<any>(null);
  const [lessons, setLessons] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadModule = async () => {
      setIsLoading(true);
      try {
        // Find module in store or fetch
        let mod = modules.find(m => m.id === moduleId);
        if (!mod) {
          await fetchModules();
          mod = modules.find(m => m.id === moduleId);
        }
        if (!mod) throw new Error("Module not found");
        setModule(mod);
        setCurrentModule(mod);

        // Fetch lessons with progress
        const lessonsData = await api.getModuleLessons(moduleId);
        setLessons(lessonsData);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadModule();
  }, [moduleId, modules, fetchModules, setCurrentModule]);

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;
  if (!module) return <ErrorMessage message={t("app.not_found")} />;

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="card p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium mb-3">
              {t(`license.${module.requiredTier}`)}
            </div>
            <h1 className="text-3xl font-bold text-surface-900 dark:text-surface-50 mb-2">{module.title}</h1>
            <p className="text-surface-600 dark:text-surface-400 max-w-2xl">{module.description}</p>
          </div>
          <div className="flex items-center gap-6 text-surface-600 dark:text-surface-400">
            <div className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              <span>{module.lessonsCount} {t("modules.lessons")}</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              <span>{module.lessonsCount * 30} {t("modules.minutes")}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Lessons List */}
      <div className="card overflow-hidden">
        <div className="p-4 border-b border-surface-200 dark:border-surface-700">
          <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("lessons.title")}</h2>
        </div>
        <div className="divide-y divide-surface-200 dark:divide-surface-700">
          {lessons.map((lesson, index) => (
            <Link
              key={lesson.id}
              to={`/lessons/${lesson.id}`}
              className="flex items-center justify-between p-4 hover:bg-surface-50 dark:hover:bg-surface-700/50 transition-colors"
            >
              <div className="flex items-center gap-4 flex-1 min-w-0">
                <div className={cn(
                  "w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0",
                  lesson.progress?.status === "completed" ? "bg-green-100 dark:bg-green-900/30 text-green-600" :
                  lesson.progress?.status === "in_progress" ? "bg-blue-100 dark:bg-blue-900/30 text-blue-600" :
                  "bg-surface-100 dark:bg-surface-800 text-surface-400"
                )}>
                  {lesson.progress?.status === "completed" ? (
                    <CheckCircle className="h-5 w-5" />
                  ) : lesson.lessonType === "quiz" ? (
                    <Award className="h-5 w-5" />
                  ) : lesson.lessonType === "simulation" ? (
                    <TrendingUp className="h-5 w-5" />
                  ) : (
                    <BookOpen className="h-5 w-5" />
                  )}
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium text-surface-900 dark:text-surface-50 truncate">
                      {index + 1}. {lesson.title}
                    </span>
                    {lesson.progress?.status === "completed" && (
                      <span className="badge badge-green text-xs">{t("modules.completed")}</span>
                    )}
                    {lesson.progress?.status === "in_progress" && (
                      <span className="badge badge-blue text-xs">{t("modules.in_progress")}</span>
                    )}
                    {!lesson.isPublished && (
                      <span className="badge badge-gray text-xs">{t("modules.locked")}</span>
                    )}
                  </div>
                  <p className="text-sm text-surface-500 dark:text-surface-400 truncate">{lesson.description}</p>
                  <div className="flex items-center gap-4 mt-1 text-xs text-surface-400">
                    <span className="flex items-center gap-1 capitalize">{lesson.lessonType}</span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {lesson.estimatedMinutes} {t("modules.minutes")}
                    </span>
                  </div>
                </div>
              </div>
              <ChevronRight className="h-5 w-5 text-surface-400 rtl:rotate-180" />
            </Link>
          ))}
        </div>
        {lessons.length === 0 && (
          <div className="p-8 text-center">
            <BookOpen className="h-12 w-12 text-surface-300 dark:text-surface-600 mx-auto mb-4" />
            <p className="text-surface-500 dark:text-surface-400">{t("app.coming_soon")}</p>
          </div>
        )}
      </div>
    </div>
  );
}