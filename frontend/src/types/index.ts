/* Architecture Types for Trading Academy */

// ===== Core =====

export interface User {
  id: string;
  email: string;
  fullName?: string;
  role: UserRole;
  locale: string;
  isActive: boolean;
  isVerified: boolean;
  createdAt: string;
  lastLoginAt?: string;
}

export interface UserWithLicense extends User {
  licenseTier?: LicenseTier;
  licenseStatus?: LicenseStatus;
  licenseExpiresAt?: string;
  features: string[];
}

export enum UserRole {
  FREE = "free",
  PRO = "pro",
  INSTITUTIONAL = "institutional",
  ADMIN = "admin",
}

export enum LicenseTier {
  FREE = "free",
  PRO = "pro",
  INSTITUTIONAL = "institutional",
}

export enum LicenseStatus {
  ACTIVE = "active",
  EXPIRED = "expired",
  REVOKED = "revoked",
  PENDING = "pending",
}

// ===== Auth =====

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  fullName?: string;
  locale?: string;
}

export interface LicenseResponse {
  id: string;
  licenseKey: string;
  tier: string;
  status: string;
  issuedAt: string;
  expiresAt?: string;
  features: string[];
}

// ===== Modules & Lessons =====

export interface Module {
  id: string;
  slug: string;
  title: string;
  description: string;
  order: number;
  requiredTier: string;
  isPublished: boolean;
  createdAt: string;
  updatedAt: string;
  lessonsCount: number;
}

export enum LessonType {
  THEORY = "theory",
  PRACTICE = "practice",
  QUIZ = "quiz",
  SIMULATION = "simulation",
}

export interface Lesson {
  id: string;
  moduleId: string;
  slug: string;
  title: string;
  description: string;
  lessonType: LessonType;
  order: number;
  estimatedMinutes: number;
  requiredTier: string;
  isPublished: boolean;
  createdAt: string;
  updatedAt: string;
  progress?: LessonProgress;
}

export interface LessonProgress {
  status: ProgressStatus;
  score?: number;
  completedAt?: string;
  timeSpentSeconds: number;
}

export enum ProgressStatus {
  NOT_STARTED = "not_started",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
}

// ===== Quiz =====

export interface QuizQuestion {
  id: string;
  questionText: Record<string, string>;
  questionType: QuizQuestionType;
  options: QuizOption[];
  difficulty: number;
  order: number;
}

export interface QuizOption {
  optionId: string;
  text: Record<string, string>;
}

export enum QuizQuestionType {
  SINGLE_CHOICE = "single_choice",
  MULTIPLE_CHOICE = "multiple_choice",
  TRUE_FALSE = "true_false",
  NUMERIC = "numeric",
}

export interface QuizAttemptResponse {
  id: string;
  userId: string;
  questionId: string;
  userAnswer: Record<string, unknown>;
  isCorrect: boolean;
  timeSpentSeconds: number;
  attemptedAt: string;
}

export interface QuizResults {
  total: number;
  correct: number;
  score: number;
  attempts: QuizAttempt[];
}

export interface QuizAttempt {
  questionId: string;
  questionText: Record<string, string>;
  userAnswer?: Record<string, unknown>;
  isCorrect: boolean;
  explanation?: Record<string, string>;
}

// ===== Paper Trading =====

export enum TradeSide {
  BUY = "buy",
  SELL = "sell",
}

export enum OrderType {
  MARKET = "market",
  LIMIT = "limit",
  STOP_LIMIT = "stop_limit",
  TRAILING_STOP = "trailing_stop",
}

export enum OrderStatus {
  PENDING = "pending",
  FILLED = "filled",
  PARTIALLY_FILLED = "partially_filled",
  CANCELLED = "cancelled",
  REJECTED = "rejected",
}

export interface PaperTrade {
  id: string;
  userId: string;
  symbol: string;
  side: TradeSide;
  orderType: OrderType;
  quantity: number;
  price?: number;
  stopPrice?: number;
  trailAmount?: number;
  status: OrderStatus;
  filledQuantity: number;
  filledPrice?: number;
  commission: number;
  pnl: number;
  strategyName?: string;
  notes?: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  closedAt?: string;
}

export interface TradeStats {
  totalTrades: number;
  closedTrades: number;
  openTrades: number;
  totalPnl: number;
  winRate: number;
  winningTrades: number;
  losingTrades: number;
  bestTrade: number;
  worstTrade: number;
  bySymbol: Record<string, { trades: number; pnl: number }>;
}

// ===== Market Data =====

export interface OHLCV {
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface Ticker {
  symbol: string;
  price: number;
  change24h: number;
  change24hPct: number;
  volume24h: number;
  marketCap?: number;
  lastUpdated?: string;
}

export interface MarketDataQuery {
  symbol: string;
  timeframe?: string;
  start?: string;
  end?: string;
  limit?: number;
}

// ===== Technical Analysis =====

export interface IndicatorConfig {
  name: string;
  parameters: Record<string, number>;
  visible: boolean;
}

export interface TechnicalIndicators {
  sma20?: number;
  sma50?: number;
  sma200?: number;
  ema12?: number;
  ema26?: number;
  rsi14?: number;
  macd?: { macd: number; signal: number; histogram: number };
  bbUpper?: number;
  bbMiddle?: number;
  bbLower?: number;
  atr14?: number;
  obv?: number;
  vwap?: number;
  adx14?: number;
  supertrend?: { value: number; direction: number };
}

export interface PatternSignal {
  patternType: string;
  direction: PatternDirection;
  confidence: number;
  keyLevels: Record<string, number>;
  targetPrice?: number;
  stopLoss?: number;
  description: string;
}

export enum PatternDirection {
  BULLISH = "bullish",
  BEARISH = "bearish",
  NEUTRAL = "neutral",
}

// ===== Risk Management =====

export enum SizingMethod {
  FIXED_FRACTIONAL = "fixed_fractional",
  KELLY = "kelly",
  VOLATILITY_BASED = "volatility_based",
  FIXED_RISK = "fixed_risk",
}

export interface PositionSizeResult {
  size: number;
  sizePct: number;
  riskAmount: number;
  riskPct: number;
  shares: number;
  method: SizingMethod;
}

export interface RiskMetrics {
  var95: number;
  var99: number;
  expectedShortfall95: number;
  maxDrawdown: number;
  maxDrawdownDuration: number;
  sharpeRatio: number;
  sortinoRatio: number;
  calmarRatio: number;
  volatility: number;
  downsideVolatility: number;
  skew: number;
  kurtosis: number;
  beta: number;
}

// ===== Backtest =====

export interface BacktestResult {
  initialCapital: number;
  finalCapital: number;
  totalReturn: number;
  totalReturnPct: number;
  trades: BacktestTrade[];
  metrics: Record<string, number>;
}

export interface BacktestTrade {
  symbol: string;
  side: string;
  entryPrice: number;
  exitPrice: number;
  quantity: number;
  entryTime: string;
  exitTime: string;
  pnl: number;
  pnlPct: number;
  commission: number;
  tag: string;
}

// ===== Coaching =====

export interface CoachingFeedback {
  type: FeedbackType;
  severity: FeedbackSeverity;
  title: string;
  message: string;
  tradeId?: string;
  lessonId?: string;
  actionableAdvice?: string;
  relatedConcepts: string[];
}

export enum FeedbackType {
  RISK_MANAGEMENT = "risk_management",
  STRATEGY_ADHERENCE = "strategy_adherence",
  POSITION_SIZING = "position_sizing",
  ENTRY_TIMING = "entry_timing",
  EXIT_TIMING = "exit_timing",
  EMOTIONAL_CONTROL = "emotional_control",
  LEARNING_GAP = "learning_gap",
  POSITIVE_REINFORCEMENT = "positive_reinforcement",
}

export enum FeedbackSeverity {
  INFO = "info",
  WARNING = "warning",
  CRITICAL = "critical",
}

export interface CoachingAnalysis {
  summary: {
    totalTrades: number;
    winRate: number;
    avgWin: number;
    avgLoss: number;
    profitFactor: number;
    expectancy: number;
    maxWinStreak: number;
    maxLossStreak: number;
  };
  bySymbol: Record<string, { trades: number; pnl: number; winRate: number }>;
  bySide: Record<string, { trades: number; pnl: number; winRate: number }>;
  recommendations: string[];
}

// ===== API =====

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ProgressSummary {
  totalModules: number;
  totalLessons: number;
  completedLessons: number;
  inProgressLessons: number;
  completionRate: number;
  totalTimeHours: number;
  averageScore: number;
}

export interface HealthResponse {
  status: string;
  version: string;
  environment: string;
  database: string;
  redis: string;
}

export interface WebSocketMessage {
  type: string;
  timestamp: string;
  data: Record<string, unknown>;
}