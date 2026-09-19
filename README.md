# 🎓 Trading Academy

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)

> **A comprehensive trading education platform that teaches you to trade like a hedge fund professional — from crypto basics to advanced portfolio management.**

Trading Academy is a full-stack web application designed to take you from complete beginner to institutional-level trader. Learn fundamental analysis, technical analysis, sentiment analysis, risk management, and portfolio construction through interactive lessons, paper trading, and gamified challenges.

## ✨ Features

### 📚 Learning System
- **5 Learning Modules**: Crypto Basics → Technical Analysis → Risk Management → Fundamental Analysis → Portfolio Management
- **10+ Interactive Lessons**: Bilingual content in Persian & English with German support
- **Quizzes**: Multi-language quiz system with instant feedback and explanations
- **Guided Tutorials**: Step-by-step interactive walkthroughs
- **Pattern Recognition Games**: Identify chart patterns on real-looking charts

### 🎮 Gamification (Better than Trading Game)
- **XP System**: 20 levels from Beginner to Legend
- **15+ Achievement Badges**: Bronze → Silver → Gold → Platinum → Diamond tiers
- **Daily Challenges**: Earn XP and coins for completing lessons, quizzes, and trades
- **Login Streaks**: Escalating rewards for daily engagement (up to 30-day streaks)
- **Leaderboards**: Compete in 4 categories — XP, Trades, Quizzes, Streaks
- **Daily Rewards**: Claim login bonuses every day

### 📈 Paper Trading
- **Simulated Exchange**: Practice with virtual funds
- **Order Types**: Market, Limit, Stop-Limit, Trailing Stop
- **Trade Journal**: Track and review all your trades
- **Performance Analytics**: Win rate, P&L, Sharpe ratio, max drawdown
- **Real-time Charts**: TradingView lightweight charts with indicators

### 📊 Analysis Tools
- **Technical Indicators**: SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Supertrend, Ichimoku
- **Pattern Recognition**: Head & Shoulders, Double Top/Bottom, Triangles, Candlestick patterns
- **Risk Metrics**: VaR, Expected Shortfall, Sortino Ratio, Calmar Ratio
- **Backtesting Engine**: Vectorized backtester with walk-forward optimization
- **Position Sizing**: Fixed Fractional, Kelly Criterion, Volatility-based

### 🤖 Adaptive Coaching
- **Trade Analysis**: AI-powered feedback on every trade
- **Mistake Detection**: Identifies emotional trading, revenge trading, overtrading
- **Personalized Recommendations**: Lesson suggestions based on your weaknesses
- **Progress Tracking**: Visual dashboards for learning and trading performance

### 🌍 Multi-Language Support
- **English** (default)
- **Persian / فارسی** (full RTL support)
- **German / Deutsch**

### 🔐 Licensing & Subscriptions
- **Free Tier**: Basic lessons, quizzes, demo trading
- **Pro Tier**: Full curriculum, advanced features, backtesting
- **Institutional Tier**: API access, white-label, SSO, dedicated support

## 🏗️ Architecture

```
trading_academy/
├── backend/               # FastAPI + PostgreSQL + Redis
│   ├── app/
│   │   ├── api/v1/       # REST API + WebSocket endpoints
│   │   ├── core/         # Auth, i18n, licensing, coaching, gamification
│   │   ├── db/           # SQLAlchemy models + Alembic migrations
│   │   ├── tasks/        # Celery background jobs
│   │   └── seed_data.py  # Curriculum + gamification seed data
│   └── alembic/          # Database migrations
├── frontend/              # React + TypeScript + Vite + TailwindCSS
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── pages/        # 10+ page components
│       ├── services/     # API client
│       ├── store/        # Zustand state management
│       ├── hooks/        # Custom React hooks
│       └── i18n/         # Translation files (EN/FA/DE)
├── shared/                # Python analysis library
│   └── trading_academy/
│       ├── analysis/     # Technical indicators, patterns
│       ├── backtest/     # Backtesting engine
│       ├── risk/         # Position sizing, risk metrics
│       └── data_fetchers/ # Binance, CoinGecko
└── docker-compose.yml     # Full stack deployment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (with TimescaleDB)
- Redis 7+

### Docker (Recommended)
```bash
git clone https://github.com/alisadeghiaghili/trading-academy.git
cd trading-academy
cp backend/.env.example backend/.env
docker-compose up -d
# Seed the database
docker-compose exec backend python -m app.seed_data
```

### Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure DATABASE_URL and REDIS_URL in .env
alembic upgrade head
python -m app.seed_data
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Access Points
| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| WebSocket | ws://localhost:8000/api/v1/ws/market-data |

## 📖 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
| Category | Endpoint | Description |
|----------|----------|-------------|
| Auth | `POST /api/v1/auth/register` | Register new user |
| Auth | `POST /api/v1/auth/login` | Login (OAuth2) |
| Modules | `GET /api/v1/modules` | List learning modules |
| Lessons | `GET /api/v1/lessons/{id}` | Get lesson with progress |
| Trading | `POST /api/v1/trades` | Place paper trade |
| Gamification | `GET /api/v1/gamification/profile` | Get XP, badges, streaks |
| Gamification | `GET /api/v1/gamification/leaderboard` | Get leaderboard |
| Market Data | `GET /api/v1/market-data/ohlcv` | Get OHLCV data |

## 🛠️ Tech Stack

### Backend
- **FastAPI** — Modern async Python web framework
- **PostgreSQL + TimescaleDB** — Time-series database for market data
- **Redis** — Caching + Celery message broker
- **SQLAlchemy 2.0** — Async ORM
- **Alembic** — Database migrations
- **Celery** — Background task processing
- **JWT (RS256)** — Authentication with RSA keys

### Frontend
- **React 18** — UI library
- **TypeScript** — Type-safe JavaScript
- **Vite** — Fast build tool
- **TailwindCSS** — Utility-first CSS
- **Zustand** — State management
- **Lightweight Charts** — TradingView charts
- **React Hook Form + Zod** — Form validation
- **i18next** — Internationalization

### Shared Library
- **pandas / numpy** — Data analysis
- **TA-Lib / pandas-ta** — Technical indicators
- **scikit-learn** — Machine learning for coaching
- **httpx** — Async HTTP client for data fetchers

## 📊 Curriculum

| Module | Lessons | Tier |
|--------|---------|------|
| Crypto Basics | What is Crypto, Blockchain, Wallets, Exchanges | Free |
| Technical Analysis | Candlestick Patterns, RSI/MACD | Free |
| Risk Management | Position Sizing, Risk-Reward Ratio | Free |
| Fundamental Analysis | Whitepaper Analysis, Tokenomics | Pro |
| Portfolio Management | Diversification, Asset Allocation | Pro |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the Apache License 2.0 — see the [LICENSE](LICENSE) file for details.

```
Copyright 2026 Ali Sadeghi Aghili

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

## 👤 Author

**Ali Sadeghi Aghili**
- GitHub: [@alisadeghiaghili](https://github.com/alisadeghiaghili)
- Repository: [trading-academy](https://github.com/alisadeghiaghili/trading-academy)

---

<p align="center">
  <strong>Built with ❤️ for traders who want to learn the right way</strong>
</p>