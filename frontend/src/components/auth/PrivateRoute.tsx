import { Outlet, Navigate } from "react-router-dom";
import { useAppStore } from "@/store";
import { LoadingSpinner } from "@/components/common/LoadingSpinner";

export function PrivateRoute() {
  const { isAuthenticated, user } = useAppStore();

  // Still loading initial profile check
  if (!user && localStorage.getItem("access_token")) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}