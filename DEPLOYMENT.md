# Content Orchestrator v2.0 - Deployment Guide

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Railway Deployment](#railway-deployment)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Production Best Practices](#production-best-practices)

## Prerequisites

### Required
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Optional
- Railway CLI (for Railway deployments)
- GitHub account (for Railway GitHub integration)
- Virtual environment tool (venv, conda, etc.)

## Local Development Setup

### Step 1: Clone and Navigate

```bash
git clone <your-repository-url>
cd agents/content_orchestrator/v2
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:
```bash
# Minimal configuration for local dev
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info
ALLOWED_ORIGINS=*
USE_MOCK_CLIENTS=true
```

### Step 5: Run the Server

**Option A - Using Python directly:**
```bash
python main.py
```

**Option B - Using uvicorn (recommended for development):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### Step 6: Verify Installation

Open your browser and navigate to:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Status**: http://localhost:8000/api/v2/status

You should see the FastAPI interactive documentation.

## Railway Deployment

### Method 1: GitHub Integration (Recommended)

#### Step 1: Prepare Repository

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "feat: Content Orchestrator v2.0 ready for deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy on Railway

1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Select the branch (usually `main`)
7. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Use the `railway.json` configuration
   - Start the server using the command in `Procfile`

#### Step 3: Configure Environment Variables

In the Railway dashboard:

1. Go to your project
2. Click on **"Variables"** tab
3. Add the following variables:

```
ALLOWED_ORIGINS=*
USE_MOCK_CLIENTS=true
TEXT_API_DELAY_MS=100
CHART_API_DELAY_MS=150
IMAGE_API_DELAY_MS=200
DIAGRAM_API_DELAY_MS=150
```

Note: `PORT` is automatically set by Railway.

#### Step 4: Verify Deployment

1. Wait for deployment to complete (1-3 minutes)
2. Railway will provide a URL like `https://your-app.railway.app`
3. Test the health endpoint:

```bash
curl https://your-app.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "orchestrator": "ready"
}
```

### Method 2: Railway CLI

#### Step 1: Install Railway CLI

**macOS/Linux:**
```bash
npm i -g @railway/cli
# or
brew install railway
```

**Windows:**
```bash
npm i -g @railway/cli
```

#### Step 2: Login

```bash
railway login
```

This will open a browser window for authentication.

#### Step 3: Initialize Project

```bash
cd agents/content_orchestrator/v2
railway init
```

Select **"Create new project"** and give it a name.

#### Step 4: Deploy

```bash
railway up
```

This will:
- Upload your code
- Install dependencies
- Start the service

#### Step 5: Set Environment Variables

```bash
railway variables set ALLOWED_ORIGINS="*"
railway variables set USE_MOCK_CLIENTS="true"
railway variables set TEXT_API_DELAY_MS="100"
railway variables set CHART_API_DELAY_MS="150"
railway variables set IMAGE_API_DELAY_MS="200"
railway variables set DIAGRAM_API_DELAY_MS="150"
```

#### Step 6: Open Deployment

```bash
railway open
```

This opens your deployed application in the browser.

## Environment Variables

### Required Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `PORT` | Server port | `8000` | `8000` |
| `HOST` | Server host | `0.0.0.0` | `0.0.0.0` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LOG_LEVEL` | Logging level | `info` | `debug`, `info`, `warning`, `error` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` | `https://yourdomain.com,https://app.yourdomain.com` |
| `RELOAD` | Auto-reload on changes | `false` | `true` (dev only) |
| `USE_MOCK_CLIENTS` | Use mock API clients | `true` | `false` |
| `TEXT_API_DELAY_MS` | Text API delay (ms) | `100` | `50-500` |
| `CHART_API_DELAY_MS` | Chart API delay (ms) | `150` | `50-500` |
| `IMAGE_API_DELAY_MS` | Image API delay (ms) | `200` | `50-500` |
| `DIAGRAM_API_DELAY_MS` | Diagram API delay (ms) | `150` | `50-500` |

### Production Variables (when using real APIs)

| Variable | Description | Example |
|----------|-------------|---------|
| `TEXT_API_URL` | Text generation API endpoint | `https://api.openai.com/v1` |
| `TEXT_API_KEY` | Text API authentication key | `sk-...` |
| `CHART_API_URL` | Chart generation API endpoint | `https://chart-api.example.com` |
| `CHART_API_KEY` | Chart API authentication key | `key123` |
| `IMAGE_API_URL` | Image generation API endpoint | `https://image-api.example.com` |
| `IMAGE_API_KEY` | Image API authentication key | `key456` |
| `DIAGRAM_API_URL` | Diagram generation API endpoint | `https://diagram-api.example.com` |
| `DIAGRAM_API_KEY` | Diagram API authentication key | `key789` |

## API Endpoints

### Base Endpoints

#### GET `/`
Root endpoint with API information.

**Response:**
```json
{
  "name": "Content Orchestrator v2.0",
  "version": "2.0.0",
  "status": "running",
  "docs": "/docs",
  "health": "/health"
}
```

#### GET `/health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "orchestrator": "ready"
}
```

#### GET `/api/v2/status`
Detailed status information.

**Response:**
```json
{
  "orchestrator": {
    "version": "2.0.0",
    "architecture": "lightweight",
    "initialized": true
  },
  "api_clients": {
    "text": "mock",
    "chart": "mock",
    "image": "mock",
    "diagram": "mock"
  },
  "environment": {
    "text_api_delay_ms": "100",
    "chart_api_delay_ms": "150",
    "image_api_delay_ms": "200",
    "diagram_api_delay_ms": "150"
  }
}
```

### Main Endpoint

#### POST `/api/v2/enrich`
Enrich a presentation with generated content.

**Request Body:**
```json
{
  "strawman": {
    "main_title": "AI in Healthcare",
    "overall_theme": "professional",
    "target_audience": "healthcare executives",
    "slides": [
      {
        "slide_id": "slide_000",
        "slide_number": 0,
        "slide_type": "title_slide",
        "slide_title": "AI in Healthcare",
        "content_guidance": "Main title with subtitle",
        "analytics_needed": false,
        "visuals_needed": false
      }
    ]
  },
  "layout_assignments": null,
  "layout_specifications": null
}
```

**Response:**
```json
{
  "original_strawman": { ... },
  "enriched_slides": [ ... ],
  "validation_report": {
    "overall_compliant": true,
    "total_slides": 1,
    "compliant_slides": 1,
    "total_violations": 0,
    "critical_violations": 0
  },
  "generation_metadata": {
    "total_items_generated": 1,
    "successful_items": 1,
    "failed_items": 0,
    "generation_time_seconds": 0.15,
    "timestamp": "2025-01-19T10:30:00",
    "failures": [],
    "orchestrator_version": "2.0",
    "architecture": "lightweight",
    "total_api_requests": 1
  }
}
```

## Troubleshooting

### Issue: `ModuleNotFoundError`

**Symptom:**
```
ModuleNotFoundError: No module named 'pydantic'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Import errors with relative imports

**Symptom:**
```
ImportError: attempted relative import with no known parent package
```

**Solution:**
Make sure you're running the app from the v2 directory:
```bash
cd agents/content_orchestrator/v2
python main.py
```

### Issue: Port already in use

**Symptom:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
Either change the port in `.env`:
```bash
PORT=8001
```

Or kill the process using the port:
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Issue: CORS errors

**Symptom:**
Browser console shows CORS errors.

**Solution:**
Update `ALLOWED_ORIGINS` in environment variables:
```bash
# For development (allow all)
ALLOWED_ORIGINS=*

# For production (specific domains)
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Issue: Railway deployment fails

**Common causes:**

1. **Missing `requirements.txt`**: Ensure the file exists and is committed.
2. **Wrong Python version**: Update `railway.json` if needed.
3. **Environment variables**: Check all required variables are set in Railway dashboard.

**Debug steps:**

```bash
# Check Railway logs
railway logs

# Check build logs
railway logs --build

# Redeploy
railway up --detach
```

### Issue: Slow response times

**Symptom:**
API responses take longer than expected.

**Solution:**
Adjust mock API delays:
```bash
railway variables set TEXT_API_DELAY_MS="50"
railway variables set CHART_API_DELAY_MS="50"
railway variables set IMAGE_API_DELAY_MS="50"
railway variables set DIAGRAM_API_DELAY_MS="50"
```

## Production Best Practices

### 1. Security

- **Never commit `.env` file** - Use Railway environment variables
- **Use specific CORS origins** - Don't use `*` in production
- **Implement API authentication** - Add API key validation
- **Use HTTPS only** - Railway provides this by default

### 2. Monitoring

- **Set up health check monitoring** - Use `/health` endpoint
- **Configure logging** - Use structured logging (JSON format)
- **Add error tracking** - Consider Sentry integration
- **Monitor performance** - Track API response times

### 3. Performance

- **Use production ASGI server** - uvicorn with multiple workers
- **Enable caching** - Cache frequently accessed data
- **Optimize API clients** - Use connection pooling
- **Set appropriate timeouts** - Prevent hanging requests

### 4. Scaling

Railway auto-scales, but consider:

- **Horizontal scaling** - Multiple instances for high traffic
- **Database caching** - If you add database integration
- **CDN for static assets** - If serving files
- **Load balancing** - Railway handles this automatically

### 5. Updates

**Deployment workflow:**

```bash
# 1. Make changes locally
git add .
git commit -m "feat: your changes"

# 2. Test locally
python main.py

# 3. Push to GitHub
git push origin main

# 4. Railway auto-deploys
# Monitor at: railway.app dashboard
```

### 6. Rollback

If deployment fails:

```bash
# Via Railway CLI
railway rollback

# Or redeploy previous commit
git revert HEAD
git push origin main
```

## Support

For issues and questions:

1. Check this deployment guide
2. Review the main [README.md](./README.md)
3. Check Railway logs: `railway logs`
4. Open an issue in the repository

---

**Last Updated**: 2025-01-19
**Status**: Production Ready ✅
