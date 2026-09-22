/**
 * In-memory demo fixtures for GitHub Pages (no backend).
 * Shapes mirror backend response models used by the frontend.
 */

export const DEMO_EMAIL = "demo@trading.academy";
export const DEMO_PASSWORD = "demo1234";

const now = () => new Date().toISOString();

export const demoUser = {
  id: "00000000-0000-4000-8000-000000000001",
  email: DEMO_EMAIL,
  fullName: "Demo Trader",
  role: "pro",
  locale: "en",
  isActive: true,
  isVerified: true,
  createdAt: now(),
  lastLoginAt: now(),
  licenseTier: "pro",
  licenseStatus: "active",
  licenseExpiresAt: "2030-01-01T00:00:00.000Z",
  features: ["demo_paper_trading", "curriculum", "coaching", "gamification"],
};

export const demoModules = [
  {
    id: "00000000-0000-4000-8000-000000000101",
    slug: "crypto-basics",
    title: "Crypto Basics",
    description: "Blockchain, wallets, exchanges, and how crypto markets work.",
    order: 1,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    lessonsCount: 4,
  },
  {
    id: "00000000-0000-4000-8000-000000000102",
    slug: "technical-analysis",
    title: "Technical Analysis",
    description: "Price action, indicators, and chart patterns used by funds.",
    order: 2,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    lessonsCount: 3,
  },
  {
    id: "00000000-0000-4000-8000-000000000103",
    slug: "risk-management",
    title: "Risk Management",
    description: "Position sizing, drawdown control, and survival first.",
    order: 3,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    lessonsCount: 2,
  },
  {
    id: "00000000-0000-4000-8000-000000000104",
    slug: "fundamental-analysis",
    title: "Fundamental Analysis",
    description: "Tokenomics, on-chain metrics, and narrative research.",
    order: 4,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    lessonsCount: 2,
  },
  {
    id: "00000000-0000-4000-8000-000000000105",
    slug: "portfolio-management",
    title: "Portfolio Management",
    description: "Allocation, rebalancing, and institutional portfolio construction.",
    order: 5,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    lessonsCount: 2,
  },
];

export const demoLessons = [
  {
    id: "00000000-0000-4000-8000-000000000201",
    moduleId: demoModules[0]!.id,
    slug: "what-is-crypto",
    title: "What is Cryptocurrency?",
    description: "Digital money, Bitcoin history, and how it differs from fiat.",
    lessonType: "theory",
    order: 1,
    estimatedMinutes: 25,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    progress: { status: "completed", score: 90, completedAt: now(), timeSpentSeconds: 1200 },
  },
  {
    id: "00000000-0000-4000-8000-000000000202",
    moduleId: demoModules[0]!.id,
    slug: "blockchain-explained",
    title: "How Blockchain Works",
    description: "Blocks, mining, consensus, and network types.",
    lessonType: "theory",
    order: 2,
    estimatedMinutes: 30,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
    progress: { status: "in_progress", timeSpentSeconds: 400 },
  },
  {
    id: "00000000-0000-4000-8000-000000000203",
    moduleId: demoModules[0]!.id,
    slug: "wallets-and-keys",
    title: "Wallets and Private Keys",
    description: "Hot vs cold wallets, seed phrases, and custody tradeoffs.",
    lessonType: "theory",
    order: 3,
    estimatedMinutes: 20,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000204",
    moduleId: demoModules[0]!.id,
    slug: "exchanges-and-order-books",
    title: "Exchanges and Order Books",
    description: "Spot vs derivatives, liquidity, and market microstructure.",
    lessonType: "practice",
    order: 4,
    estimatedMinutes: 35,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000205",
    moduleId: demoModules[1]!.id,
    slug: "market-structure",
    title: "Market Structure",
    description: "Trends, ranges, liquidity sweeps, and session behavior.",
    lessonType: "theory",
    order: 1,
    estimatedMinutes: 40,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000206",
    moduleId: demoModules[1]!.id,
    slug: "indicators-that-matter",
    title: "Indicators That Matter",
    description: "SMA, EMA, RSI, MACD, and when they actually help.",
    lessonType: "theory",
    order: 2,
    estimatedMinutes: 45,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000207",
    moduleId: demoModules[1]!.id,
    slug: "chart-patterns",
    title: "Chart Patterns",
    description: "Head & shoulders, triangles, and confirmation rules.",
    lessonType: "practice",
    order: 3,
    estimatedMinutes: 35,
    requiredTier: "free",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000208",
    moduleId: demoModules[2]!.id,
    slug: "position-sizing",
    title: "Position Sizing",
    description: "Fixed fractional, Kelly, and volatility-based sizing.",
    lessonType: "theory",
    order: 1,
    estimatedMinutes: 30,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000209",
    moduleId: demoModules[2]!.id,
    slug: "drawdown-control",
    title: "Drawdown Control",
    description: "Stop placement, risk of ruin, and survival math.",
    lessonType: "theory",
    order: 2,
    estimatedMinutes: 28,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000210",
    moduleId: demoModules[3]!.id,
    slug: "tokenomics",
    title: "Tokenomics",
    description: "Supply schedules, unlocks, incentives, and value capture.",
    lessonType: "theory",
    order: 1,
    estimatedMinutes: 32,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000211",
    moduleId: demoModules[3]!.id,
    slug: "on-chain-research",
    title: "On-chain Research",
    description: "Flows, holders, activity, and narrative confirmation.",
    lessonType: "practice",
    order: 2,
    estimatedMinutes: 38,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000212",
    moduleId: demoModules[4]!.id,
    slug: "portfolio-construction",
    title: "Portfolio Construction",
    description: "Strategic allocation, risk budgets, and rebalancing rules.",
    lessonType: "theory",
    order: 1,
    estimatedMinutes: 40,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000213",
    moduleId: demoModules[4]!.id,
    slug: "performance-review",
    title: "Performance Review",
    description: "Sharpe, Sortino, Calmar, and process scorecards.",
    lessonType: "practice",
    order: 2,
    estimatedMinutes: 30,
    requiredTier: "pro",
    isPublished: true,
    createdAt: now(),
    updatedAt: now(),
  },
];

export const demoLessonContent: Record<string, { html: string }> = {
  [demoLessons[0]!.id]: {
    html: `
      <h2>What is Cryptocurrency?</h2>
      <p>Cryptocurrency is digital money secured by cryptography and typically issued on a decentralized network without a central bank.</p>
      <h3>Key properties</h3>
      <ul>
        <li><strong>Decentralized:</strong> no single point of control</li>
        <li><strong>Transparent:</strong> transactions are auditable on-chain</li>
        <li><strong>Scarce:</strong> many assets have a hard supply cap</li>
        <li><strong>Global:</strong> settlement without banking hours</li>
      </ul>
      <h3>Bitcoin in one paragraph</h3>
      <p>Bitcoin launched in 2009 by Satoshi Nakamoto as peer-to-peer electronic cash with a fixed 21M supply schedule.</p>
    `,
  },
};

export function defaultLessonContent(title: string) {
  return {
    html: `
      <h2>${title}</h2>
      <p>This is demo lesson content on GitHub Pages. Connect a real backend for the full curriculum, quizzes, and progress tracking.</p>
      <h3>What you would study here</h3>
      <ul>
        <li>Core concepts with worked examples</li>
        <li>Market case studies</li>
        <li>Practice checks and quizzes</li>
      </ul>
    `,
  };
}

export const demoQuizQuestions = [
  {
    id: "00000000-0000-4000-8000-000000000301",
    questionText: {
      en: "Who created Bitcoin?",
      fa: "بیت‌کوین توسط چه کسی ایجاد شد؟",
      de: "Wer hat Bitcoin erstellt?",
    },
    questionType: "single_choice",
    options: [
      { optionId: "a", text: { en: "Satoshi Nakamoto", fa: "ساتوشی ناکاموتو", de: "Satoshi Nakamoto" } },
      { optionId: "b", text: { en: "Vitalik Buterin", fa: "ویتالیک بوترین", de: "Vitalik Buterin" } },
      { optionId: "c", text: { en: "Elon Musk", fa: "ایلان ماسک", de: "Elon Musk" } },
      { optionId: "d", text: { en: "Mark Zuckerberg", fa: "مارک زاکربرگ", de: "Mark Zuckerberg" } },
    ],
    difficulty: 1,
    order: 1,
  },
  {
    id: "00000000-0000-4000-8000-000000000302",
    questionText: {
      en: "What is the maximum supply of Bitcoin?",
      fa: "حداکثر عرضه بیت‌کوین چقدر است؟",
      de: "Was ist das maximale Angebot an Bitcoin?",
    },
    questionType: "single_choice",
    options: [
      { optionId: "a", text: { en: "21 million", fa: "۲۱ میلیون", de: "21 Millionen" } },
      { optionId: "b", text: { en: "100 million", fa: "۱۰۰ میلیون", de: "100 Millionen" } },
      { optionId: "c", text: { en: "Unlimited", fa: "نامحدود", de: "Unbegrenzt" } },
      { optionId: "d", text: { en: "1 billion", fa: "۱ میلیارد", de: "1 Milliarde" } },
    ],
    difficulty: 1,
    order: 2,
  },
];

export const demoTrades = [
  {
    id: "00000000-0000-4000-8000-000000000401",
    userId: demoUser.id,
    symbol: "BTCUSDT",
    side: "buy",
    orderType: "market",
    quantity: 0.05,
    price: 64200,
    status: "filled",
    filledQuantity: 0.05,
    filledPrice: 64200,
    commission: 3.21,
    pnl: 310.5,
    strategyName: "Breakout",
    notes: "Demo filled trade",
    tags: ["demo"],
    createdAt: now(),
    updatedAt: now(),
    closedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000402",
    userId: demoUser.id,
    symbol: "ETHUSDT",
    side: "sell",
    orderType: "limit",
    quantity: 1.2,
    price: 3180,
    status: "filled",
    filledQuantity: 1.2,
    filledPrice: 3180,
    commission: 1.9,
    pnl: -85.2,
    strategyName: "Mean reversion",
    notes: "Demo losing trade",
    tags: ["demo"],
    createdAt: now(),
    updatedAt: now(),
    closedAt: now(),
  },
  {
    id: "00000000-0000-4000-8000-000000000403",
    userId: demoUser.id,
    symbol: "SOLUSDT",
    side: "buy",
    orderType: "stop_limit",
    quantity: 12,
    price: 148,
    stopPrice: 145,
    status: "pending",
    filledQuantity: 0,
    commission: 0,
    pnl: 0,
    strategyName: "Pullback",
    tags: ["demo"],
    createdAt: now(),
    updatedAt: now(),
  },
];

export const demoTradeStats = {
  totalTrades: 12,
  closedTrades: 10,
  openTrades: 2,
  totalPnl: 1240.75,
  winRate: 0.6,
  winningTrades: 6,
  losingTrades: 4,
  bestTrade: 520.1,
  worstTrade: -190.4,
  bySymbol: {
    BTCUSDT: { trades: 6, pnl: 880.2 },
    ETHUSDT: { trades: 4, pnl: 210.55 },
    SOLUSDT: { trades: 2, pnl: 150 },
  },
};

export const demoProgressSummary = {
  totalModules: 5,
  totalLessons: 13,
  completedLessons: 3,
  inProgressLessons: 2,
  completionRate: 0.23,
  totalTimeHours: 4.5,
  averageScore: 86,
};

export const demoCoachingAnalysis = {
  summary: {
    totalTrades: 12,
    winRate: 0.6,
    avgWin: 145.2,
    avgLoss: -88.4,
    profitFactor: 1.8,
    expectancy: 42.5,
    maxWinStreak: 4,
    maxLossStreak: 2,
  },
  bySymbol: {
    BTCUSDT: { trades: 6, pnl: 880.2, winRate: 0.67 },
    ETHUSDT: { trades: 4, pnl: 210.55, winRate: 0.5 },
    SOLUSDT: { trades: 2, pnl: 150, winRate: 0.5 },
  },
  bySide: {
    buy: { trades: 8, pnl: 920.3, winRate: 0.62 },
    sell: { trades: 4, pnl: 320.45, winRate: 0.55 },
  },
  recommendations: [
    "Keep risk per trade at 1R or below while win rate is stabilizing.",
    "Journal the two ETH mean-reversion losses — exits were early.",
    "Complete the Risk Management module before sizing up.",
  ],
};

export const demoGamification = {
  level: 7,
  xp: 3420,
  xpToNextLevel: 580,
  coins: 240,
  streakDays: 5,
  rank: 14,
  totalXp: 3420,
};

export const demoBadges = [
  { id: "b1", name: "First Steps", tier: "bronze", description: "Complete first lesson", earned: true },
  { id: "b2", name: "Chart Reader", tier: "silver", description: "Finish Technical Analysis intro", earned: true },
  { id: "b3", name: "Risk Aware", tier: "gold", description: "Score 90%+ on risk quiz", earned: false },
  { id: "b4", name: "Streak Master", tier: "platinum", description: "30-day login streak", earned: false },
];

export const demoChallenges = [
  { id: "c1", title: "Complete 1 lesson", xp: 50, coins: 10, progress: 1, target: 1, completed: true },
  { id: "c2", title: "Place 3 paper trades", xp: 80, coins: 15, progress: 1, target: 3, completed: false },
  { id: "c3", title: "Score 80%+ on a quiz", xp: 60, coins: 12, progress: 0, target: 1, completed: false },
];

export const demoLeaderboard = Array.from({ length: 10 }, (_, i) => ({
  rank: i + 1,
  displayName: i === 0 ? "Demo Trader" : `Trader ${i + 1}`,
  value: 5200 - i * 320,
  isCurrentUser: i === 0,
}));

export const demoSymbols = [
  { symbol: "BTCUSDT", price: 67250.4, change24h: 820.1, change24hPct: 1.23, volume24h: 28400000000, marketCap: 1320000000000, lastUpdated: now() },
  { symbol: "ETHUSDT", price: 3210.8, change24h: -28.4, change24hPct: -0.88, volume24h: 12100000000, marketCap: 386000000000, lastUpdated: now() },
  { symbol: "SOLUSDT", price: 152.3, change24h: 4.2, change24hPct: 2.84, volume24h: 3200000000, marketCap: 70000000000, lastUpdated: now() },
];

/** Deterministic synthetic OHLCV series for charts. */
export function demoOhlcv(symbol: string, limit = 120) {
  const base = demoSymbols.find((s) => s.symbol === symbol)?.price ?? 100;
  const out: Array<{ timestamp: string; open: number; high: number; low: number; close: number; volume: number }> = [];
  let price = base * 0.92;
  const start = Date.now() - limit * 3600_000;
  for (let i = 0; i < limit; i += 1) {
    const wave = Math.sin(i / 9) * base * 0.012;
    const drift = (base - price) * 0.03;
    const open = price;
    const close = open + wave + drift + ((i * 17) % 7) - 3;
    const high = Math.max(open, close) + Math.abs(wave) * 0.6;
    const low = Math.min(open, close) - Math.abs(wave) * 0.6;
    out.push({
      timestamp: new Date(start + i * 3600_000).toISOString(),
      open: round(open),
      high: round(high),
      low: round(low),
      close: round(close),
      volume: Math.round(1000 + ((i * 131) % 900)),
    });
    price = close;
  }
  return out;
}

function round(n: number) {
  return Math.round(n * 100) / 100;
}
