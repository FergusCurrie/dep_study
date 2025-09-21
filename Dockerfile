# Multi-stage build
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci 
COPY frontend .
RUN npm run build

# Backend 
FROM ghcr.io/astral-sh/uv:python3.10-bookworm
WORKDIR /app
COPY backend .
RUN uv sync 

# Get fronend 
COPY --from=frontend-build /app/frontend/dist ./dist
EXPOSE 8000


CMD ["uv", "run", "main.py"]