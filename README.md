# Trading Academy

A comprehensive trading education platform that teaches trading from beginner to hedge-fund level. Built with FastAPI (backend) and React/TypeScript (frontend).

## Features

- **Multi-level Curriculum**: Beginner to hedge-fund level trading education
- **Multi-language Support**: English, Persian (RTL), German
- **Interactive Learning**: Jupyter-style notebooks, quizzes, simulations
- **Paper Trading**: Risk-free practice with real market data
- **Strategy Lab**: Backtesting, optimization, performance analysis
- **Risk Management**: Position sizing, portfolio optimization, drawdown controls
- **Adaptive Coaching**: AI-powered feedback on trades and decisions
- **Subscription Model**: Tiered licensing (Free/Pro/Institutional)

## Architecture

```
trading_academy/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/       # REST API endpoints
│   │   ├── core/      # Config, security, i18n, licensing
│   │   ├── db/        # Database models & sessions
│   │   ├── services/  # Business logic
│   │   ├── schemas/   # Pydantic models
│   │   └── tasks/     # Celery background jobs
│   ├── alembic/       # Database migrations
│   └── locale/        # Translation catalogs
├── frontend/          # React + TypeScript (TODO)
├── shared/            # Shared Python packages
├── notebooks/         # Jupyter lessons
├── data/              # Runtime cache
└── docker-compose.yml # Local development stack
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 16+ (with TimescaleDB extension)
- Redis 7+
- Docker & Docker Compose (recommended)

### Using Docker (Recommended)

```bash
# Clone and navigate
cd trading_academy

# Copy environment template
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run migrations
docker-compose exec backend alembic upgrade head
```

### Local Development

```bash
# Install dependencies
make install

# Start database & Redis
docker-compose up -d postgres redis

# Run migrations
make upgrade

# Start development server
make dev
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login (OAuth2 password flow)
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user profile

### Licenses
- `POST /api/v1/licenses/validate` - Validate license key
- `POST /api/v1/licenses/activate` - Activate license for current user
- `GET /api/v1/licenses/current` - Get active license

### Modules & Lessons
- `GET /api/v1/modules` - List accessible modules
- `GET /api/v1/modules/{id}` - Get module details
- `GET /api/v1/modules/{id}/lessons` - Get module lessons with progress
- `GET /api/v1/lessons/{id}` - Get lesson with progress
- `GET /api/v1/lessons/{id}/content` - Get lesson content

### Progress
- `GET /api/v1/progress` - List user progress
- `POST /api/v1/progress/lesson/{id}/start` - Start lesson
- `PATCH /api/v1/progress/lesson/{id}` - Update progress
- `POST /api/v1/progress/lesson/{id}/complete` - Complete lesson
- `GET /api/v1/progress/stats/summary` - Get progress summary

### Quizzes
- `POST /api/v1/quizzes/attempt` - Submit quiz answer
- `GET /api/v1/quizzes/lesson/{id}/questions` - Get quiz questions
- `GET /api/v1/quizzes/lesson/{id}/results` - Get quiz results
- `GET /api/v1/quizzes/stats/overall` - Get overall quiz stats

### Paper Trading
- `POST /api/v1/trades` - Create paper trade
- `GET /api/v1/trades` - List trades
- `GET /api/v1/trades/{id}` - Get trade details
- `POST /api/v1/trades/{id}/cancel` - Cancel pending trade
- `GET /api/v1/trades/stats/summary` - Get trading stats

### Market Data
- `GET /api/v1/market-data/ohlcv` - Get OHLCV data
- `GET /api/v1/market-data/symbols` - Get available symbols
- `GET /api/v1/market-data/latest/{symbol}` - Get latest price

## Development

### Code Quality

```bash
# Run all checks
make check

# Individual checks
make lint       # Ruff linter
make format     # Ruff formatter
make typecheck  # MyPy type checker
make test       # Pytest with coverage
```

### Database Migrations

```bash
# Create new migration
make migrate

# Apply migrations
make upgrade

# Rollback last migration
make downgrade
```

### License Keys

```bash
# Generate sample license keys
make keys
```

## Internationalization

Supported locales:
- `en` - English (default)
- `fa` - Persian (فارسی) - RTL support
- `de` - German (Deutsch)

Translation files are in `backend/locale/{locale}/LC_MESSAGES/messages.po`.

## Licensing

This is a proprietary, closed-source application. All rights reserved.

Subscription tiers:
- **Free**: Basic lessons, quizzes, demo paper trading
- **Pro**: Full curriculum, advanced features, backtesting, coaching
- **Institutional**: API access, white-label, SSO, dedicated support

## Project Structure Details

### Backend Core Modules

- **`app.core.config`**: Pydantic Settings configuration
- **`app.core.security`**: Password hashing, JWT tokens, license tokens
- **`app.core.licensing`**: License generation, validation, feature flags
- **`app.core.i18n`**: Babel/gettext integration, locale detection

### Database Models

- **User**: Authentication, roles, preferences
- **License**: Subscription management, feature flags
- **Module/Lesson**: Curriculum structure
- **UserProgress**: Learning progress tracking
- **QuizQuestion/QuizAttempt**: Assessment system
- **PaperTrade**: Simulated trading
- **MarketData**: Cached OHLCV data

## Environment Variables

See `backend/.env.example` for all configuration options.

Key variables:
- `SECRET_KEY` - JWT signing key (min 32 chars, CHANGE IN PRODUCTION)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `BINANCE_API_KEY/SECRET` - For live market data
- `LICENSE_PUBLIC_KEY_PATH` - RSA public key for license validation
- `LICENSE_PRIVATE_KEY_PATH` - RSA private key for license signing

## Deployment

### Production Checklist

1. Generate RSA keys for licensing:
   ```bash
   openssl genrsa -out keys/license_private.pem 2048
   openssl rsa -in keys/license_private.pem -pubout -out keys/license_public.pem
   ```

2. Set strong `SECRET_KEY` (64+ random chars)

3. Configure production database with SSL

4. Set `ENVIRONMENT=production`, `DEBUG=false`

5. Use reverse proxy (nginx) with TLS

6. Configure monitoring (Prometheus metrics at `:9090/metrics`)

## Contributing

This is a proprietary project. Internal development only.

## Support

For technical issues, contact the development team.