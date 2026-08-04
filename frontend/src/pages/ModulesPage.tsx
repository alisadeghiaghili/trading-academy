import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { BookOpen, Lock, CheckCircle, Clock, ArrowRight } from "lucide-react";
import { useAppStore } from "@/store";
import { LoadingSpinner, ErrorMessage } from "@/components/common";
import { cn } from "@/utils";

export function ModulesPage() {
  const { t } = useTranslation();
  const { modules, fetchModules } = useAppStore();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadModules = async () => {
      setIsLoading(true);
      try {
        await fetchModules();
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    loadModules();
  }, [fetchModules]);

  if (isLoading) return <LoadingSpinner size="lg" label={t("app.loading")} />;
  if (error) return <ErrorMessage message={error} onRetry={() => window.location.reload()} />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("modules.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400 mt-1">{t("app.tagline")}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules.map((module) => (
          <Link
            key={module.id}
            to={`/modules/${module.id}`}
            className={cn(
              "card-hover p-6 flex flex-col h-full transition-all duration-200",
              !module.isPublished && "opacity-50"
            )}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
                <BookOpen className="h-7 w-7 text-white" />
              </div>
              {!module.isPublished && (
                <Lock className="h-5 w-5 text-surface-400" />
              )}
            </div>

            <div className="flex-1">
              <h3 className="text-lg font-semibold text-surface-900 dark:text-surface-50 mb-2">{module.title}</h3>
              <p className="text-surface-600 dark:text-surface-400 text-sm mb-4 line-clamp-2">{module.description}</p>
            </div>

            <div className="space-y-3 pt-4 border-t border-surface-200 dark:border-surface-700">
              <div className="flex items-center gap-2 text-sm text-surface-500">
                <Clock className="h-4 w-4" />
                <span>{module.lessonsCount} {t("modules.lessons")}</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-surface-500">
                <BookOpen className="h-4 w-4" />
                <span>{t("modules.required_tier", { tier: t(`license.${module.requiredTier}`) })}</span>
              </div>
            </div>
          </Link>
        ))}

        {modules.length === 0 && (
          <div className="col-span-full text-center py-16">
            <BookOpen className="h-12 w-12 text-surface-300 dark:text-surface-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-surface-900 dark:text-surface-50">{t("app.no_data")}</h3>
            <p className="text-surface-500 dark:text-surface-400 mt-1">{t("modules.title")} {t("app.coming_soon")}</p>
          </div>
        )}
      </div>
    </div>
  );
}