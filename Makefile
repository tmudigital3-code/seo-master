# Makefile for SEO Tracker Application

# Variables
PYTHON := python3
PIP := pip3
NODE := node
NPM := npm

# Default target
.PHONY: help
help:
	@echo "SEO Tracker - Development Commands"
	@echo "=================================="
	@echo "make install-backend    - Install Python dependencies"
	@echo "make install-frontend   - Install frontend dependencies"
	@echo "make dev-backend        - Run backend development server"
	@echo "make dev-frontend       - Run frontend development server"
	@echo "make build-frontend     - Build frontend for production"
	@echo "make docker-build       - Build Docker images"
	@echo "make docker-up          - Start all services with Docker Compose"
	@echo "make docker-down        - Stop all services"
	@echo "make docker-logs        - View logs from Docker services"
	@echo "make test               - Run tests"
	@echo "make clean              - Clean build artifacts"

# Install dependencies
.PHONY: install-backend
install-backend:
	$(PIP) install -r requirements.txt

.PHONY: install-frontend
install-frontend:
	cd frontend && $(NPM) install

# Development servers
.PHONY: dev-backend
dev-backend:
	$(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

.PHONY: dev-frontend
dev-frontend:
	cd frontend && $(NPM) start

# Build frontend
.PHONY: build-frontend
build-frontend:
	cd frontend && $(NPM) run build

# Docker commands
.PHONY: docker-build
docker-build:
	docker-compose build

.PHONY: docker-up
docker-up:
	docker-compose up -d

.PHONY: docker-down
docker-down:
	docker-compose down

.PHONY: docker-logs
docker-logs:
	docker-compose logs -f

# Testing
.PHONY: test
test:
	$(PYTHON) -m pytest tests/

# Clean
.PHONY: clean
clean:
	rm -rf frontend/build
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete