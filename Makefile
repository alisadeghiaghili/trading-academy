# Trading Academy Makefile

.PHONY: help install dev test lint format typecheck migrate upgrade docker-up docker-down seed clean

help:
	@echo "Trading Academy - Development Commands"
	@echo ""
	@echo "Backend:"
	@echo "  install        Install backend dependencies"
	@echo "  dev            Run backend development server"
	@echo "  test           Run backend tests"
	@echo "  lint           Run backend linter"
	@echo "  format         Format backend code"
	@echo "  typecheck      Run backend type checker"
	@echo "  seed           Seed database with curriculum data"
	@echo ""
	@echo "Frontend:"
	@echo "  frontend-install  Install frontend dependencies"
	@echo "  frontend-dev      Run frontend dev server"
	@echo "  frontend-build    Build frontend for production"
	@echo ""
	@echo "Docker:"
	@echo "  docker-up      Start all services"
	@echo "  docker-down    Stop all services"
	@echo "  docker-logs    View docker logs"
	@echo "  docker-build   Build docker images"
	@echo ""
	@echo "Utilities:"
	@echo "  clean          Clean build artifacts"
	@echo "  keys           Generate license keys"

install:
	cd backend && pip install -r requirements.txt

dev:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

seed:
	cd backend && python -m app.seed_data

test:
	cd backend && pytest -v --cov=app --cov-report=term-missing

lint:
	cd backend && ruff check .

format:
	cd backend && ruff format .

typecheck:
	cd backend && mypy app/

migrate:
	cd backend && alembic revision --autogenerate -m "update"

upgrade:
	cd backend && alembic upgrade head

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-build:
	docker-compose build

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

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	rm -rf frontend/node_modules 2>/dev/null || true
