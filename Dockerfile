# Multi-stage Dockerfile for SEO Tracker application

# Backend stage
FROM python:3.9-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Frontend stage
FROM node:16-alpine as frontend

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy frontend source
COPY frontend/. .

# Build frontend
RUN npm run build

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy frontend build
COPY --from=frontend /app/build /app/frontend/build

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 8000 80

# Start services
CMD ["sh", "-c", "nginx && uvicorn main:app --host 0.0.0.0 --port 8000"]