import { useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Settings as SettingsIcon,
  Globe,
  Sun,
  Moon,
  Monitor,
  User,
  Bell,
  Shield,
  CreditCard,
  Key,
  CheckCircle,
} from "lucide-react";
import { useAppStore } from "@/store";
import { useTheme } from "@/hooks/useApp";
import { cn } from "@/utils";

export function SettingsPage() {
  const { t, i18n } = useTranslation();
  const { user, locale } = useAppStore();
  const { theme, setTheme } = useTheme();
  const [activeSection, setActiveSection] = useState<string>("preferences");

  const locales = [
    { code: "en", name: "English", native: "English", dir: "ltr" },
    { code: "fa", name: "Persian", native: "فارسی", dir: "rtl" },
    { code: "de", name: "German", native: "Deutsch", dir: "ltr" },
  ];

  const sections = [
    { id: "preferences", icon: Sun, label: t("settings.preferences") },
    { id: "language", icon: Globe, label: t("settings.language") },
    { id: "notifications", icon: Bell, label: t("settings.notifications") },
    { id: "security", icon: Shield, label: t("settings.security") },
    { id: "subscription", icon: CreditCard, label: t("settings.subscription") },
    { id: "api_keys", icon: Key, label: t("settings.api_keys") },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-surface-900 dark:text-surface-50">{t("settings.title")}</h1>
        <p className="text-surface-600 dark:text-surface-400">{t("app.tagline")}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar Navigation */}
        <div className="card p-2 space-y-1 h-fit">
          {sections.map((section) => {
            const Icon = section.icon;
            return (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={cn(
                  "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                  activeSection === section.id
                    ? "bg-primary-50 text-primary-700 dark:bg-primary-900/20 dark:text-primary-300"
                    : "text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700"
                )}
              >
                <Icon className="h-5 w-5" />
                {section.label}
              </button>
            );
          })}
        </div>

        {/* Content Panel */}
        <div className="card p-6 lg:col-span-3">
          {activeSection === "preferences" && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("settings.preferences")}</h2>

              <div>
                <label className="label">{t("settings.theme")}</label>
                <div className="flex gap-3 mt-2">
                  {(["light", "dark", "system"] as const).map((th) => (
                    <button
                      key={th}
                      onClick={() => setTheme(th)}
                      className={cn(
                        "flex items-center gap-2 px-4 py-2.5 rounded-lg border transition-colors",
                        theme === th
                          ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300"
                          : "border-surface-200 dark:border-surface-700 text-surface-700 dark:text-surface-300"
                      )}
                    >
                      {th === "light" && <Sun className="h-4 w-4" />}
                      {th === "dark" && <Moon className="h-4 w-4" />}
                      {th === "system" && <Monitor className="h-4 w-4" />}
                      {t(`settings.${th}`)}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeSection === "language" && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("settings.language")}</h2>
              <div className="space-y-3">
                {locales.map((loc) => (
                  <button
                    key={loc.code}
                    onClick={() => i18n.changeLanguage(loc.code)}
                    className={cn(
                      "w-full flex items-center justify-between p-4 rounded-lg border transition-colors",
                      i18n.language === loc.code
                        ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                        : "border-surface-200 dark:border-surface-700 hover:border-surface-300"
                    )}
                  >
                    <div>
                      <p className="font-medium text-surface-900 dark:text-surface-50">{loc.native}</p>
                      <p className="text-sm text-surface-500">{loc.name} ({loc.dir})</p>
                    </div>
                    {i18n.language === loc.code && (
                      <CheckCircle className="h-5 w-5 text-primary-600" />
                    )}
                  </button>
                ))}
              </div>
            </div>
          )}

          {activeSection === "subscription" && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("settings.subscription")}</h2>
              <div className="card p-6 bg-gradient-to-br from-primary-500 to-primary-700 text-white">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-sm opacity-80">{t("license.current_plan")}</p>
                    <h3 className="text-2xl font-bold capitalize">{user?.licenseTier || t("license.free")}</h3>
                  </div>
                  <CreditCard className="h-10 w-10 opacity-80" />
                </div>
                {user?.licenseTier === "free" && (
                  <button className="mt-4 px-4 py-2 bg-white text-primary-700 rounded-lg font-medium hover:bg-opacity-90">
                    {t("license.upgrade")}
                  </button>
                )}
              </div>
            </div>
          )}

          {activeSection === "security" && (
            <div className="space-y-6">
              <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">{t("settings.security")}</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-lg bg-surface-50 dark:bg-surface-700/50">
                  <div>
                    <p className="font-medium text-surface-900 dark:text-surface-50">{t("auth.password")}</p>
                    <p className="text-sm text-surface-500">••••••••</p>
                  </div>
                  <button className="btn-secondary btn-sm">{t("edit")}</button>
                </div>
              </div>
            </div>
          )}

          {(activeSection === "notifications" || activeSection === "api_keys") && (
            <div className="text-center py-12">
              <SettingsIcon className="h-12 w-12 text-surface-300 dark:text-surface-600 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-surface-900 dark:text-surface-50">{t("app.coming_soon")}</h3>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}