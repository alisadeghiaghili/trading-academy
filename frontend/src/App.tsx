import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import { useEffect } from "react";
import { useAppStore } from "@/store";
import { useLocale, useTheme } from "@/hooks/useApp";
import { MainLayout } from "@/components/layout/MainLayout";
import { LoginPage } from "@/pages/LoginPage";
import { RegisterPage } from "@/pages/RegisterPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { ModulesPage } from "@/pages/ModulesPage";
import { ModuleDetailPage } from "@/pages/ModuleDetailPage";
import { LessonPage } from "@/pages/LessonPage";
import { TradingPage } from "@/pages/TradingPage";
import { PortfolioPage } from "@/pages/PortfolioPage";
import { AnalyticsPage } from "@/pages/AnalyticsPage";
import { CoachingPage } from "@/pages/CoachingPage";
import { SettingsPage } from "@/pages/SettingsPage";
import { GamificationPage } from "@/pages/GamificationPage";
import { PrivateRoute } from "@/components/auth/PrivateRoute";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";

// Trailing slash from Vite BASE_URL; react-router basename has none
const routerBasename = import.meta.env.BASE_URL.replace(/\/$/, "") || "/";

export default function App() {
  const { fetchProfile, isAuthenticated } = useAppStore();
  useTheme();
  useLocale();

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  return (
    <BrowserRouter basename={routerBasename}>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: { fontSize: "14px" },
        }}
      />
      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />
          }
        />
        <Route
          path="/register"
          element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />
          }
        />

        {/* Private routes */}
        <Route element={<PrivateRoute />}>
          <Route element={<MainLayout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/modules" element={<ModulesPage />} />
            <Route path="/modules/:moduleId" element={<ModuleDetailPage />} />
            <Route path="/lessons/:lessonId" element={<LessonPage />} />
            <Route path="/trading" element={<TradingPage />} />
            <Route path="/portfolio" element={<PortfolioPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/coaching" element={<CoachingPage />} />
            <Route path="/gamification" element={<GamificationPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}

function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-surface-50 dark:bg-surface-900">
      <h1 className="text-6xl font-bold text-primary-600">404</h1>
      <p className="text-xl text-surface-600 dark:text-surface-400 mt-4">
        Page not found
      </p>
      <Link to="/dashboard" className="btn-primary mt-6">
        Go to Dashboard
      </Link>
    </div>
  );
}