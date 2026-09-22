import { useState } from "react";
import { useTranslation } from "react-i18next";
import { Bell, Sun, Moon, Monitor, Globe, LogOut, User as UserIcon } from "lucide-react";
import { useAppStore } from "@/store";
import { useTheme } from "@/hooks/useApp";
import { Link } from "react-router-dom";
import { cn } from "@/utils";

export function Header() {
  const { t, i18n } = useTranslation();
  const { user, logout } = useAppStore();
  const { theme, setTheme } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const [themeOpen, setThemeOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);

  const locales = [
    { code: "en", name: "English", flag: "🇬🇧" },
    { code: "fa", name: "فارسی", flag: "🇮🇷" },
    { code: "de", name: "Deutsch", flag: "🇩🇪" },
  ];

  const changeLocale = (locale: string) => {
    i18n.changeLanguage(locale);
    useAppStore.getState().setLocale(locale);
    setLangOpen(false);
  };

  return (
    <header className="flex items-center justify-between h-16 px-6 border-b border-surface-200 dark:border-surface-700 bg-white dark:bg-surface-800">
      <div>
        <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-50">
          {t("nav.dashboard")}
        </h2>
      </div>

      <div className="flex items-center gap-2">
        {/* Language Selector */}
        <div className="relative">
          <button
            onClick={() => setLangOpen(!langOpen)}
            className="btn-ghost p-2"
            aria-label="Language"
          >
            <Globe className="h-5 w-5" />
          </button>
          {langOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-surface-800 rounded-lg shadow-lg border border-surface-200 dark:border-surface-700 py-1 z-50">
              {locales.map((loc) => (
                <button
                  key={loc.code}
                  onClick={() => changeLocale(loc.code)}
                  className={cn(
                    "w-full px-4 py-2 text-sm flex items-center gap-2 hover:bg-surface-100 dark:hover:bg-surface-700",
                    i18n.language === loc.code && "bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300"
                  )}
                >
                  <span>{loc.flag}</span>
                  <span>{loc.name}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Theme Selector */}
        <div className="relative">
          <button
            onClick={() => setThemeOpen(!themeOpen)}
            className="btn-ghost p-2"
            aria-label="Theme"
          >
            {theme === "light" && <Sun className="h-5 w-5" />}
            {theme === "dark" && <Moon className="h-5 w-5" />}
            {theme === "system" && <Monitor className="h-5 w-5" />}
          </button>
          {themeOpen && (
            <div className="absolute right-0 mt-2 w-40 bg-white dark:bg-surface-800 rounded-lg shadow-lg border border-surface-200 dark:border-surface-700 py-1 z-50">
              {(["light", "dark", "system"] as const).map((th) => (
                <button
                  key={th}
                  onClick={() => {
                    setTheme(th);
                    setThemeOpen(false);
                  }}
                  className={cn(
                    "w-full px-4 py-2 text-sm flex items-center gap-2 hover:bg-surface-100 dark:hover:bg-surface-700",
                    theme === th && "bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300"
                  )}
                >
                  {th === "light" && <Sun className="h-4 w-4" />}
                  {th === "dark" && <Moon className="h-4 w-4" />}
                  {th === "system" && <Monitor className="h-4 w-4" />}
                  <span>{t(`settings.${th}`)}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Notifications */}
        <button className="btn-ghost p-2 relative" aria-label="Notifications">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1.5 right-1.5 h-2 w-2 bg-red-500 rounded-full" />
        </button>

        {/* User Menu */}
        <div className="relative">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-surface-100 dark:hover:bg-surface-700"
          >
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center text-white font-medium text-sm">
              {user?.fullName?.charAt(0)?.toUpperCase() || user?.email?.charAt(0)?.toUpperCase() || "U"}
            </div>
            <div className="hidden md:block text-left">
              <p className="text-sm font-medium text-surface-900 dark:text-surface-50">
                {user?.fullName || user?.email?.split("@")[0]}
              </p>
              <p className="text-xs text-surface-500 dark:text-surface-400 capitalize">
                {user?.licenseTier || "free"}
              </p>
            </div>
          </button>
          {menuOpen && (
            <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-surface-800 rounded-lg shadow-lg border border-surface-200 dark:border-surface-700 py-1 z-50">
              <Link
                to="/settings"
                className="flex items-center gap-2 px-4 py-2 text-sm hover:bg-surface-100 dark:hover:bg-surface-700"
              >
                <UserIcon className="h-4 w-4" />
                {t("nav.profile")}
              </Link>
              <button
                onClick={() => logout()}
                className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-surface-100 dark:hover:bg-surface-700"
              >
                <LogOut className="h-4 w-4" />
                {t("nav.logout")}
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}