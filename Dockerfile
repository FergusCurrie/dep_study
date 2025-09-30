# Multi-stage build
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci 
COPY frontend .

# Set environment variable for production API URL
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Backend 
FROM ghcr.io/astral-sh/uv:python3.10-bookworm
WORKDIR /app
COPY backend .
RUN uv sync 

# Get fronend 
COPY --from=frontend-build /app/frontend/dist ./dist
# EXPOSE 8000
EXPOSE 9897


CMD ["uv", "run", "main.py"]