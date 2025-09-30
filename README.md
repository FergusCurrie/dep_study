# Dep Study

POC application for solving practice problems. 

FastAPI is used as backend, which generates a problem description in markdown + latex, solution and multi-choice answers. 

React + mui renders the problem for solving. 

## Environment Configuration

The application supports different API endpoints for development and production environments.

### Development
- **Default API URL**: `http://127.0.0.1:8000/`
- **Frontend**: `cd frontend && npm run dev`
- **Backend**: `cd backend && uv run poe run`

### Production (Docker)
- **Build**: `docker-compose up -d`
- **Custom URL**: `docker build --build-arg VITE_API_BASE_URL=http://your-url/ .`

### Environment Variables
- `VITE_API_BASE_URL`: API base URL for the frontend
- Copy `frontend/env.example` to `frontend/.env.local` for local development overrides
- Copy `env.example` to `.env` for Docker Compose production setup

## Creating new problem 

1. Define problem name. 
2. Create new template in `problem_templates/<name>.j2`
3. Add python file to `src/problems/<name>.py` with logic for generating question data + solving. 
4. Use `manual_db.py` to add to problem database
5. Update `src/problems/dispatch.py` to correctly dispatch name to problem generation

## Development Setup

### Backend
```bash
cd backend
uv sync
uv run poe run
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Build 

### Docker
```bash
docker build -t test-app-build .
docker run -p 8000:8000 test-app-build
```

### Docker Compose
1. Copy `env.example` to `.env` and set your production API URL:
```bash
cp env.example .env
# Edit .env and set VITE_API_BASE_URL=http://your-production-url/
```

2. Build and run:
```bash
docker-compose up --build
```

### Docker with Custom API URL
```bash
docker build --build-arg VITE_API_BASE_URL=http://your-production-url/ -t dep-study .
docker run -p 8000:8000 dep-study
```

## Testing

Backend tests run automatically on pull requests:
```bash
cd backend
uv run poe test
```