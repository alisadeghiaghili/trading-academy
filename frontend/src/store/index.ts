import { create } from "zustand";
import { persist } from "zustand/middleware";
import { api } from "@/services/api";
import {
  UserWithLicense,
  AuthTokens,
  Module,
  Lesson,
  TradeStats,
  ProgressSummary,
  CoachingAnalysis,
} from "@/types";

interface AppState {
  // Auth
  user: UserWithLicense | null;
  isAuthenticated: boolean;

  // Data
  modules: Module[];
  currentModule: Module | null;
  currentLesson: Lesson | null;
  tradeStats: TradeStats | null;
  progressSummary: ProgressSummary | null;
  coachingAnalysis: CoachingAnalysis | null;

  // UI
  sidebarOpen: boolean;
  theme: "light" | "dark" | "system";
  locale: string;

  // WebSocket
  wsConnected: boolean;

  // Loading
  isLoading: boolean;
  error: string | null;

  // Actions
  setUser: (user: UserWithLicense | null) => void;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; password: string; fullName?: string; locale?: string }) => Promise<void>;
  logout: () => Promise<void>;
  fetchProfile: () => Promise<void>;
  fetchModules: () => Promise<void>;
  setCurrentModule: (module: Module | null) => void;
  setCurrentLesson: (lesson: Lesson | null) => void;
  fetchTradeStats: () => Promise<void>;
  fetchProgressSummary: () => Promise<void>;
  fetchCoachingAnalysis: () => Promise<void>;
  setTheme: (theme: "light" | "dark" | "system") => void;
  setLocale: (locale: string) => void;
  toggleSidebar: () => void;
  setWsConnected: (connected: boolean) => void;
  clearError: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      modules: [],
      currentModule: null,
      currentLesson: null,
      tradeStats: null,
      progressSummary: null,
      coachingAnalysis: null,
      sidebarOpen: true,
      theme: "system",
      locale: "en",
      wsConnected: false,
      isLoading: false,
      error: null,

      // Auth actions
      setUser: (user) => set({ user, isAuthenticated: !!user }),

      login: async (email, password) => {
        set({ isLoading: true, error: null });
        try {
          const tokens = await api.login(email, password);
          const user = await api.getProfile();
          set({ user, isAuthenticated: true, isLoading: false, locale: user.locale || "en" });
        } catch (err: any) {
          const message = err.response?.data?.detail || "Login failed";
          set({ isLoading: false, error: message });
          throw new Error(message);
        }
      },

      register: async (data) => {
        set({ isLoading: true, error: null });
        try {
          await api.register(data);
          set({ isLoading: false });
        } catch (err: any) {
          const message = err.response?.data?.detail || "Registration failed";
          set({ isLoading: false, error: message });
          throw new Error(message);
        }
      },

      logout: async () => {
        try {
          await api.logout();
        } catch {
          // Clear local state regardless
        }
        set({
          user: null,
          isAuthenticated: false,
          modules: [],
          currentModule: null,
          currentLesson: null,
          tradeStats: null,
          progressSummary: null,
          coachingAnalysis: null,
        });
      },

      fetchProfile: async () => {
        try {
          const user = await api.getProfile();
          set({ user, isAuthenticated: true, locale: user.locale || "en" });
        } catch {
          set({ user: null, isAuthenticated: false });
        }
      },

      // Data actions
      fetchModules: async () => {
        set({ isLoading: true });
        try {
          const response = await api.getModules();
          set({ modules: response.items || [], isLoading: false });
        } catch (err: any) {
          set({ isLoading: false, error: err.message });
        }
      },

      setCurrentModule: (module) => set({ currentModule: module, currentLesson: null }),
      setCurrentLesson: (lesson) => set({ currentLesson: lesson }),

      fetchTradeStats: async () => {
        try {
          const stats = await api.getTradeStats();
          set({ tradeStats: stats });
        } catch {
          // Silent fail
        }
      },

      fetchProgressSummary: async () => {
        try {
          const summary = await api.getProgressSummary();
          set({ progressSummary: summary });
        } catch {
          // Silent fail
        }
      },

      fetchCoachingAnalysis: async () => {
        try {
          const analysis = await api.getCoachingAnalysis();
          set({ coachingAnalysis: analysis });
        } catch {
          // Silent fail
        }
      },

      // UI actions
      setTheme: (theme) => set({ theme }),
      setLocale: (locale) => set({ locale }),
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setWsConnected: (connected) => set({ wsConnected: connected }),
      clearError: () => set({ error: null }),
    }),
    {
      name: "trading-academy-storage",
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        theme: state.theme,
        locale: state.locale,
      }),
    }
  )
);