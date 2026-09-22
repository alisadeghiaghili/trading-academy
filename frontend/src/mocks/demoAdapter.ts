/**
 * Axios adapter that serves in-browser mock responses when VITE_DEMO=true.
 * Enables GitHub Pages login and UI navigation without a backend.
 */
import type { AxiosAdapter, AxiosRequestConfig, AxiosResponse } from "axios";
import {
  DEMO_EMAIL,
  DEMO_PASSWORD,
  demoBadges,
  demoChallenges,
  demoCoachingAnalysis,
  demoGamification,
  demoLeaderboard,
  demoLessonContent,
  demoLessons,
  demoModules,
  demoOhlcv,
  demoProgressSummary,
  demoQuizQuestions,
  demoSymbols,
  demoTradeStats,
  demoTrades,
  demoUser,
  defaultLessonContent,
} from "./demoData";

type Handler = (ctx: {
  method: string;
  path: string;
  params: Record<string, unknown>;
  body: unknown;
  form: URLSearchParams | null;
}) => { status?: number; data: unknown };

interface DemoAccount {
  email: string;
  password: string;
  fullName?: string;
  locale?: string;
}

const TOKEN_KEY = "demo_access_token";
const ACCOUNTS_KEY = "demo_accounts";

function loadAccounts(): DemoAccount[] {
  try {
    const raw = localStorage.getItem(ACCOUNTS_KEY);
    const parsed = raw ? (JSON.parse(raw) as DemoAccount[]) : [];
    return parsed;
  } catch {
    return [];
  }
}

function saveAccounts(accounts: DemoAccount[]): void {
  localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(accounts));
}

function issueTokens() {
  localStorage.setItem(TOKEN_KEY, "demo-access-token");
  return {
    accessToken: "demo-access-token",
    refreshToken: "demo-refresh-token",
    tokenType: "bearer",
    expiresIn: 3600,
  };
}

function isAuthed(): boolean {
  return Boolean(localStorage.getItem(TOKEN_KEY));
}

function profileFor(account: DemoAccount | typeof demoUser) {
  return {
    ...demoUser,
    email: account.email,
    fullName: account.fullName || demoUser.fullName,
    locale: account.locale || demoUser.locale,
  };
}

function unauthorized() {
  return { status: 401, data: { detail: "Not authenticated" } };
}

const handlers: Array<{ test: RegExp; methods: string[]; handle: Handler }> = [
  {
    test: /^\/health$/,
    methods: ["get"],
    handle: () => ({
      data: {
        status: "ok",
        version: "demo",
        environment: "github-pages-demo",
        database: "n/a",
        redis: "n/a",
      },
    }),
  },
  {
    test: /^\/auth\/login$/,
    methods: ["post"],
    handle: ({ form, body }) => {
      const email = form?.get("username") || (body as { email?: string } | undefined)?.email || "";
      const password = form?.get("password") || (body as { password?: string } | undefined)?.password || "";
      const accounts = loadAccounts();
      const seeded = { email: DEMO_EMAIL, password: DEMO_PASSWORD, fullName: "Demo Trader", locale: "en" };
      const all = [seeded, ...accounts];
      const account = all.find((a) => a.email === email && a.password === password);
      if (!account) {
        return { status: 401, data: { detail: "Incorrect email or password" } };
      }
      return { data: issueTokens() };
    },
  },
  {
    test: /^\/auth\/register$/,
    methods: ["post"],
    handle: ({ body }) => {
      const data = body as { email?: string; password?: string; fullName?: string; locale?: string };
      if (!data?.email || !data?.password) {
        return { status: 400, data: { detail: "Email and password required" } };
      }
      const accounts = loadAccounts();
      if (data.email === DEMO_EMAIL || accounts.some((a) => a.email === data.email)) {
        return { status: 400, data: { detail: "Email already registered" } };
      }
      accounts.push({
        email: data.email,
        password: data.password,
        fullName: data.fullName,
        locale: data.locale,
      });
      saveAccounts(accounts);
      return {
        status: 201,
        data: {
          ...demoUser,
          email: data.email,
          fullName: data.fullName || data.email.split("@")[0],
          locale: data.locale || "en",
        },
      };
    },
  },
  {
    test: /^\/auth\/logout$/,
    methods: ["post"],
    handle: () => {
      localStorage.removeItem(TOKEN_KEY);
      return { data: { ok: true } };
    },
  },
  {
    test: /^\/auth\/refresh$/,
    methods: ["post"],
    handle: () => {
      if (!isAuthed()) return unauthorized();
      return { data: issueTokens() };
    },
  },
  {
    test: /^\/users\/me$/,
    methods: ["get"],
    handle: () => {
      if (!isAuthed()) return unauthorized();
      const accounts = loadAccounts();
      const email = localStorage.getItem("demo_user_email") || DEMO_EMAIL;
      const account = accounts.find((a) => a.email === email);
      return { data: profileFor(account ?? demoUser) };
    },
  },
  {
    test: /^\/modules$/,
    methods: ["get"],
    handle: () => ({
      data: {
        items: demoModules,
        total: demoModules.length,
        page: 1,
        pageSize: demoModules.length,
        totalPages: 1,
      },
    }),
  },
  {
    test: /^\/modules\/([^/]+)$/,
    methods: ["get"],
    handle: ({ path }) => {
      const id = path.split("/")[2];
      const mod = demoModules.find((m) => m.id === id || m.slug === id);
      return mod ? { data: mod } : { status: 404, data: { detail: "Module not found" } };
    },
  },
  {
    test: /^\/modules\/([^/]+)\/lessons$/,
    methods: ["get"],
    handle: ({ path }) => {
      const id = path.split("/")[2];
      const mod = demoModules.find((m) => m.id === id || m.slug === id);
      const items = demoLessons.filter((l) => l.moduleId === mod?.id);
      return {
        data: {
          items,
          total: items.length,
          page: 1,
          pageSize: items.length || 10,
          totalPages: 1,
        },
      };
    },
  },
  {
    test: /^\/lessons\/([^/]+)\/content$/,
    methods: ["get"],
    handle: ({ path }) => {
      const id = path.split("/")[2] ?? "";
      const lesson = demoLessons.find((l) => l.id === id || l.slug === id);
      const content = demoLessonContent[id] || (lesson ? defaultLessonContent(lesson.title) : defaultLessonContent("Lesson"));
      return { data: content };
    },
  },
  {
    test: /^\/lessons\/([^/]+)$/,
    methods: ["get"],
    handle: ({ path }) => {
      const id = path.split("/")[2];
      const lesson = demoLessons.find((l) => l.id === id || l.slug === id);
      return lesson ? { data: lesson } : { status: 404, data: { detail: "Lesson not found" } };
    },
  },
  {
    test: /^\/progress\/stats\/summary$/,
    methods: ["get"],
    handle: () => ({ data: demoProgressSummary }),
  },
  {
    test: /^\/quizzes\/lesson\/([^/]+)\/questions$/,
    methods: ["get"],
    handle: () => ({ data: demoQuizQuestions }),
  },
  {
    test: /^\/quizzes\/attempt$/,
    methods: ["post"],
    handle: ({ body }) => {
      const data = body as { questionId?: string; userAnswer?: Record<string, unknown> };
      const correct = data.userAnswer?.option_id === "a" || data.userAnswer?.optionId === "a";
      return {
        data: {
          id: "demo-attempt",
          userId: demoUser.id,
          questionId: data.questionId,
          userAnswer: data.userAnswer,
          isCorrect: correct,
          timeSpentSeconds: 12,
          attemptedAt: new Date().toISOString(),
        },
      };
    },
  },
  {
    test: /^\/quizzes\/lesson\/([^/]+)\/results$/,
    methods: ["get"],
    handle: () => ({
      data: {
        total: demoQuizQuestions.length,
        correct: 1,
        score: 50,
        attempts: demoQuizQuestions.map((q, i) => ({
          questionId: q.id,
          questionText: q.questionText,
          isCorrect: i === 0,
        })),
      },
    }),
  },
  {
    test: /^\/quizzes\/stats\/overall$/,
    methods: ["get"],
    handle: () => ({
      data: { totalAttempts: 8, correct: 6, averageScore: 75 },
    }),
  },
  {
    test: /^\/trades\/stats\/summary$/,
    methods: ["get"],
    handle: () => ({ data: demoTradeStats }),
  },
  {
    test: /^\/trades$/,
    methods: ["get", "post"],
    handle: ({ method, body }) => {
      if (method === "post") {
        const data = body as Record<string, unknown>;
        const trade = {
          id: `demo-trade-${Date.now()}`,
          userId: demoUser.id,
          symbol: data.symbol ?? "BTCUSDT",
          side: data.side ?? "buy",
          orderType: data.orderType ?? "market",
          quantity: data.quantity ?? 0.01,
          price: data.price ?? 67000,
          status: "filled",
          filledQuantity: data.quantity ?? 0.01,
          filledPrice: data.price ?? 67000,
          commission: 1.5,
          pnl: 0,
          strategyName: data.strategyName,
          notes: data.notes,
          tags: data.tags ?? ["demo"],
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        return { status: 201, data: trade };
      }
      return {
        data: {
          items: demoTrades,
          total: demoTrades.length,
          page: 1,
          pageSize: demoTrades.length,
          totalPages: 1,
        },
      };
    },
  },
  {
    test: /^\/market-data\/symbols$/,
    methods: ["get"],
    handle: () => ({ data: demoSymbols }),
  },
  {
    test: /^\/market-data\/ohlcv$/,
    methods: ["get"],
    handle: ({ params }) => {
      const symbol = String(params.symbol || "BTCUSDT");
      const limit = Number(params.limit || 120);
      return { data: demoOhlcv(symbol, limit) };
    },
  },
  {
    test: /^\/market-data\/latest\/([^/]+)$/,
    methods: ["get"],
    handle: ({ path }) => {
      const symbol = path.split("/")[3];
      const found = demoSymbols.find((s) => s.symbol === symbol) ?? demoSymbols[0];
      return { data: found };
    },
  },
  {
    test: /^\/coaching\/analyze$/,
    methods: ["get"],
    handle: () => ({ data: demoCoachingAnalysis }),
  },
  {
    test: /^\/coaching\/trade\/([^/]+)\/analyze$/,
    methods: ["get"],
    handle: () => ({
      data: {
        feedback: [
          {
            type: "exit_timing",
            severity: "info",
            message: "Exit was inside the planned range. Process looks clean.",
          },
        ],
        recommendations: ["Write the trade thesis before entry next time."],
      },
    }),
  },
  {
    test: /^\/coaching\/recommendations$/,
    methods: ["get"],
    handle: () => ({
      data: {
        lessons: demoLessons.slice(2, 5),
        tips: demoCoachingAnalysis.recommendations,
      },
    }),
  },
  {
    test: /^\/gamification\/profile$/,
    methods: ["get"],
    handle: () => ({ data: demoGamification }),
  },
  {
    test: /^\/gamification\/login\/track$/,
    methods: ["post"],
    handle: () => ({ data: { ...demoGamification, streakDays: demoGamification.streakDays + 1, xp: demoGamification.xp + 10 } }),
  },
  {
    test: /^\/gamification\/badges$/,
    methods: ["get"],
    handle: () => ({ data: demoBadges }),
  },
  {
    test: /^\/gamification\/challenges$/,
    methods: ["get"],
    handle: () => ({ data: demoChallenges }),
  },
  {
    test: /^\/gamification\/leaderboard$/,
    methods: ["get"],
    handle: () => ({ data: demoLeaderboard }),
  },
  {
    test: /^\/gamification\/xp\/history$/,
    methods: ["get"],
    handle: () => ({
      data: Array.from({ length: 10 }, (_, i) => ({
        id: `xp-${i}`,
        amount: 20 + i * 5,
        reason: i % 2 === 0 ? "lesson_complete" : "daily_login",
        createdAt: new Date(Date.now() - i * 86400000).toISOString(),
      })),
    }),
  },
  {
    test: /^\/gamification\/tutorials$/,
    methods: ["get"],
    handle: () => ({ data: [] }),
  },
  {
    test: /^\/gamification\/pattern-games$/,
    methods: ["get"],
    handle: () => ({ data: [] }),
  },
  {
    test: /^\/gamification\/economic-calendar$/,
    methods: ["get"],
    handle: () => ({ data: [] }),
  },
  {
    test: /^\/gamification\/news$/,
    methods: ["get"],
    handle: () => ({ data: [] }),
  },
  {
    test: /^\/licenses\/current$/,
    methods: ["get"],
    handle: () => ({
      data: {
        id: "demo-license",
        licenseKey: "DEMO-PRO-0001",
        tier: "pro",
        status: "active",
        issuedAt: new Date().toISOString(),
        expiresAt: "2030-01-01T00:00:00.000Z",
        features: demoUser.features,
      },
    }),
  },
];

function parseBody(config: AxiosRequestConfig): {
  body: unknown;
  form: URLSearchParams | null;
} {
  const raw = config.data;
  if (raw == null || raw === "") return { body: undefined, form: null };
  if (typeof raw === "string") {
    if (raw.includes("=") && !raw.trim().startsWith("{")) {
      return { body: undefined, form: new URLSearchParams(raw) };
    }
    try {
      return { body: JSON.parse(raw), form: null };
    } catch {
      return { body: raw, form: null };
    }
  }
  if (raw instanceof URLSearchParams) {
    return { body: undefined, form: raw };
  }
  return { body: raw, form: null };
}

function normalizePath(url: string): string {
  let path = url.split("?")[0] || "/";
  // Strip configured API base if present (e.g. /api/v1)
  path = path.replace(/^\/api\/v1/, "");
  if (!path.startsWith("/")) path = `/${path}`;
  if (path.length > 1 && path.endsWith("/")) path = path.slice(0, -1);
  return path;
}

export const demoAdapter: AxiosAdapter = async (config) => {
  await new Promise((r) => setTimeout(r, 80));
  const method = (config.method || "get").toLowerCase();
  const path = normalizePath(config.url || "/");
  const { body, form } = parseBody(config);
  const params = { ...(config.params as Record<string, unknown> | undefined) };

  // Preserve demo identity for /users/me after register/login flows
  if (path === "/auth/login" && form?.get("username")) {
    localStorage.setItem("demo_user_email", String(form.get("username")));
  }
  if (path === "/auth/register" && body && typeof body === "object") {
    const email = (body as { email?: string }).email;
    if (email) localStorage.setItem("demo_user_email", email);
  }

  for (const route of handlers) {
    if (!route.methods.includes(method) || !route.test.test(path)) continue;
    const result = route.handle({ method, path, params, body, form });
    const response: AxiosResponse = {
      data: result.data,
      status: result.status ?? 200,
      statusText: result.status && result.status >= 400 ? "Error" : "OK",
      headers: {},
      config: config as AxiosResponse["config"],
    };
    if (response.status >= 400) {
      const error = new Error((result.data as { detail?: string })?.detail || "Request failed") as Error & {
        response: AxiosResponse;
        isAxiosError: boolean;
        config: AxiosRequestConfig;
      };
      error.response = response;
      error.isAxiosError = true;
      error.config = config;
      throw error;
    }
    return response;
  }

  // Unknown routes: empty success so pages degrade instead of hard-failing
  return {
    data: { items: [], total: 0, page: 1, pageSize: 0, totalPages: 0 },
    status: 200,
    statusText: "OK",
    headers: {},
    config: config as AxiosResponse["config"],
  };
};

export function isDemoMode(): boolean {
  return import.meta.env.VITE_DEMO === "true";
}

export { DEMO_EMAIL, DEMO_PASSWORD };
