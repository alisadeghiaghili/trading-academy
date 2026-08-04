import { NavLink } from "react-router-dom";
import { useTranslation } from "react-i18next";
import {
  LayoutDashboard,
  BookOpen,
  LineChart,
  Briefcase,
  PieChart,
  MessageSquare,
  Settings,
  ChevronLeft,
  ChevronRight,
  TrendingUp,
} from "lucide-react";
import { useAppStore } from "@/store";
import { cn } from "@/utils";

const navItems = [
  { key: "dashboard", icon: LayoutDashboard, path: "/dashboard" },
  { key: "modules", icon: BookOpen, path: "/modules" },
  { key: "trading", icon: LineChart, path: "/trading" },
  { key: "portfolio", icon: Briefcase, path: "/portfolio" },
  { key: "analytics", icon: PieChart, path: "/analytics" },
  { key: "coaching", icon: MessageSquare, path: "/coaching" },
  { key: "settings", icon: Settings, path: "/settings" },
] as const;

export function Sidebar() {
  const { t } = useTranslation();
  const { sidebarOpen, toggleSidebar } = useAppStore();

  return (
    <aside
      className={cn(
        "fixed inset-y-0 z-40 flex flex-col bg-white dark:bg-surface-800 border-surface-200 dark:border-surface-700 transition-all duration-300",
        "ltr:left-0 ltr:border-r rtl:right-0 rtl:border-l",
        sidebarOpen ? "w-64" : "w-16"
      )}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-surface-200 dark:border-surface-700">
        <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
          <TrendingUp className="h-6 w-6 text-white" />
        </div>
        {sidebarOpen && (
          <div className="overflow-hidden">
            <h1 className="font-bold text-surface-900 dark:text-surface-50 truncate">
              {t("app.name")}
            </h1>
            <p className="text-xs text-surface-500 dark:text-surface-400 truncate">
              {t("app.tagline")}
            </p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto scrollbar-thin px-2 py-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.key}>
                <NavLink
                  to={item.path}
                  className={({ isActive }) =>
                    cn(
                      "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                      isActive
                        ? "bg-primary-50 text-primary-700 dark:bg-primary-900/20 dark:text-primary-300"
                        : "text-surface-700 dark:text-surface-300 hover:bg-surface-100 dark:hover:bg-surface-700"
                    )
                  }
                  title={sidebarOpen ? undefined : t(`nav.${item.key}`)}
                >
                  <Icon className="h-5 w-5 flex-shrink-0" />
                  {sidebarOpen && <span>{t(`nav.${item.key}`)}</span>}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Toggle button */}
      <button
        onClick={toggleSidebar}
        className="flex items-center justify-center h-10 border-t border-surface-200 dark:border-surface-700 text-surface-500 hover:text-surface-900 dark:hover:text-surface-50 hover:bg-surface-100 dark:hover:bg-surface-700"
      >
        {sidebarOpen ? (
          <ChevronLeft className="h-5 w-5 rtl:hidden" />
        ) : (
          <ChevronRight className="h-5 w-5 rtl:hidden" />
        )}
        {sidebarOpen ? (
          <ChevronRight className="h-5 w-5 hidden rtl:block" />
        ) : (
          <ChevronLeft className="h-5 w-5 hidden rtl:block" />
        )}
      </button>
    </aside>
  );
}