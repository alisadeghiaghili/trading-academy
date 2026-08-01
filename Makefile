# Trading Academy Makefile

.PHONY: help install dev test lint format typecheck migrate upgrade downgrade db-shell clean docker-up docker-down docker-logs

# Default target
help:
	@echo "Trading Academy - Development Commands"
	@echo ""
	@echo "Backend:"
	@echo "  install        Install backend dependencies"
	@echo "  dev            Run backend development server"
	@echo "  test           Run backend tests"
	@echo "  lint           Run backend linter (ruff)"
	@echo "  format         Format backend code (black + ruff)"
	@echo "  typecheck      Run backend type checker (mypy)"
	@echo "  migrate        Create new alembic migration"
	@echo "  upgrade        Apply database migrations"
	@echo "  downgrade      Rollback last migration"
	@echo "  db-shell       Open database shell"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up      Start all services with docker-compose"
	@echo "  docker-down    Stop all services"
	@echo "  docker-logs    View docker-compose logs"
	@echo "  docker-build   Build docker images"
	@echo ""
	@echo "Utilities:"
	@echo "  clean          Clean build artifacts"
	@echo "  keys           Generate license keys"

# Backend commands
install:
	cd backend && pip install -e ".[dev]"

dev:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	cd backend && pytest -v --cov=app --cov-report=term-missing

test-watch:
	cd backend && pytest-watch -v

lint:
	cd backend && ruff check .

lint-fix:
	cd backend && ruff check --fix .

format:
	cd backend && ruff format .

typecheck:
	cd backend && mypy app/

migrate:
	@read -p "Migration message: " msg; \
	cd backend && alembic revision --autogenerate -m "$$msg"

upgrade:
	cd backend && alembic upgrade head

downgrade:
	cd backend && alembic downgrade -1

db-shell:
	cd backend && psql "$(grep DATABASE_URL .env | cut -d'=' -f2-)"

# Docker commands
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-down-v:
	docker-compose down -v

docker-logs:
	docker-compose logs -f

docker-build:
	docker-compose build

docker-ps:
	docker-compose ps

# License key generation
keys:
	@cd backend && python -c "
from app.core.licensing import LicenseManager
from app.db.models import UserRole
from uuid import uuid4

class MockUser:
    id = uuid4()

mgr = LicenseManager()
for tier in ['free', 'pro', 'institutional']:
    key = mgr.generate_license_key(MockUser.id, UserRole(tier))
    print(f'{tier.upper()}: {key}')
"

# Clean
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true

# Generate requirements.txt from pyproject.toml
requirements:
	cd backend && pip freeze > requirements.txt

# Run all checks
check: lint typecheck test

# CI simulation
ci: install check