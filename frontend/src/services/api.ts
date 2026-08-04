import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from "axios";
import { AuthTokens } from "@/types";

const API_BASE_URL = import.meta.env.VITE_API_URL || "/api/v1";

class ApiClient {
  private client: AxiosInstance;
  private refreshPromise: Promise<AuthTokens> | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
      timeout: 30000,
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = this.getAccessToken();
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const tokens = await this.refreshTokens();
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${tokens.accessToken}`;
            }
            return this.client(originalRequest);
          } catch (refreshError) {
            this.clearTokens();
            window.location.href = "/login";
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private getAccessToken(): string | null {
    return localStorage.getItem("access_token");
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem("refresh_token");
  }

  private setTokens(tokens: AuthTokens): void {
    localStorage.setItem("access_token", tokens.accessToken);
    localStorage.setItem("refresh_token", tokens.refreshToken);
  }

  private clearTokens(): void {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  private async refreshTokens(): Promise<AuthTokens> {
    if (!this.refreshPromise) {
      const refreshToken = this.getRefreshToken();
      if (!refreshToken) {
        throw new Error("No refresh token");
      }

      this.refreshPromise = this.client
        .post<AuthTokens>("/auth/refresh", { refresh_token: refreshToken })
        .then((response) => {
          this.setTokens(response.data);
          return response.data;
        })
        .finally(() => {
          this.refreshPromise = null;
        });
    }

    return this.refreshPromise;
  }

  // Auth
  async login(email: string, password: string): Promise<AuthTokens> {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await this.client.post<AuthTokens>("/auth/login", formData.toString(), {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    this.setTokens(response.data);
    return response.data;
  }

  async register(data: {
    email: string;
    password: string;
    fullName?: string;
    locale?: string;
  }): Promise<void> {
    await this.client.post("/auth/register", data);
  }

  async refreshToken(): Promise<AuthTokens> {
    return this.refreshTokens();
  }

  async logout(): Promise<void> {
    try {
      await this.client.post("/auth/logout");
    } finally {
      this.clearTokens();
    }
  }

  async getProfile() {
    const { data } = await this.client.get("/users/me");
    return data;
  }

  // Modules & Lessons
  async getModules(params?: { page?: number; pageSize?: number }) {
    const { data } = await this.client.get("/modules", { params });
    return data;
  }

  async getModule(id: string) {
    const { data } = await this.client.get(`/modules/${id}`);
    return data;
  }

  async getModuleLessons(moduleId: string) {
    const { data } = await this.client.get(`/modules/${moduleId}/lessons`);
    return data;
  }

  async getLesson(id: string) {
    const { data } = await this.client.get(`/lessons/${id}`);
    return data;
  }

  async getLessonContent(id: string) {
    const { data } = await this.client.get(`/lessons/${id}/content`);
    return data;
  }

  // Progress
  async startLesson(lessonId: string) {
    const { data } = await this.client.post(`/progress/lesson/${lessonId}/start`);
    return data;
  }

  async updateProgress(lessonId: string, update: { status?: string; score?: number; timeSpentSeconds?: number }) {
    const { data } = await this.client.patch(`/progress/lesson/${lessonId}`, update);
    return data;
  }

  async completeLesson(lessonId: string, score?: number, timeSpent?: number) {
    const params = new URLSearchParams();
    if (score !== undefined) params.append("score", String(score));
    if (timeSpent !== undefined) params.append("time_spent", String(timeSpent));
    const { data } = await this.client.post(`/progress/lesson/${lessonId}/complete?${params}`);
    return data;
  }

  async getProgressSummary() {
    const { data } = await this.client.get("/progress/stats/summary");
    return data;
  }

  // Quizzes
  async getQuizQuestions(lessonId: string) {
    const { data } = await this.client.get(`/quizzes/lesson/${lessonId}/questions`);
    return data;
  }

  async submitQuizAttempt(attempt: {
    questionId: string;
    userAnswer: Record<string, unknown>;
    timeSpentSeconds: number;
  }) {
    const { data } = await this.client.post("/quizzes/attempt", attempt);
    return data;
  }

  async getQuizResults(lessonId: string) {
    const { data } = await this.client.get(`/quizzes/lesson/${lessonId}/results`);
    return data;
  }

  async getQuizStats() {
    const { data } = await this.client.get("/quizzes/stats/overall");
    return data;
  }

  // Paper Trading
  async createTrade(trade: {
    symbol: string;
    side: string;
    orderType: string;
    quantity: number;
    price?: number;
    stopPrice?: number;
    strategyName?: string;
    notes?: string;
    tags?: string[];
  }) {
    const { data } = await this.client.post("/trades", trade);
    return data;
  }

  async getTrades(params?: {
    page?: number;
    pageSize?: number;
    symbol?: string;
    status?: string;
    side?: string;
  }) {
    const { data } = await this.client.get("/trades", { params });
    return data;
  }

  async getTradeStats() {
    const { data } = await this.client.get("/trades/stats/summary");
    return data;
  }

  async cancelTrade(id: string) {
    const { data } = await this.client.post(`/trades/${id}/cancel`);
    return data;
  }

  // Market Data
  async getOHLCV(params: { symbol: string; timeframe?: string; start?: string; end?: string; limit?: number }) {
    const { data } = await this.client.get("/market-data/ohlcv", { params });
    return data;
  }

  async getLatestPrice(symbol: string) {
    const { data } = await this.client.get(`/market-data/latest/${symbol}`);
    return data;
  }

  async getSymbols() {
    const { data } = await this.client.get("/market-data/symbols");
    return data;
  }

  // Coaching
  async analyzeTrade(tradeId: string) {
    const { data } = await this.client.get(`/coaching/trade/${tradeId}/analyze`);
    return data;
  }

  async getCoachingAnalysis() {
    const { data } = await this.client.get("/coaching/analyze");
    return data;
  }

  async getLessonRecommendations() {
    const { data } = await this.client.get("/coaching/recommendations");
    return data;
  }

  // Licenses
  async validateLicense(licenseKey: string) {
    const { data } = await this.client.post("/licenses/validate", { license_key: licenseKey });
    return data;
  }

  async activateLicense(licenseKey: string) {
    const { data } = await this.client.post("/licenses/activate", { license_key: licenseKey });
    return data;
  }

  async getCurrentLicense() {
    const { data } = await this.client.get("/licenses/current");
    return data;
  }

  // Health
  async healthCheck() {
    const { data } = await this.client.get("/health");
    return data;
  }
}

export const api = new ApiClient();
export default api;