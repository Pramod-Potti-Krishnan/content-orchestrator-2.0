# Railway Deployment Setup for Content Orchestrator v2.0

## 🚀 Deployment Status

✅ **Code pushed to GitHub**: https://github.com/Pramod-Potti-Krishnan/content-orchestrator-2.0.git

Railway will automatically detect the push and begin deployment using:
- `railway.json` - Build and deploy configuration
- `Procfile` - Start command: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`
- `requirements.txt` - Python dependencies

## 📋 Required Railway Environment Variables

### Critical Configuration

Set these environment variables in your Railway dashboard to use **production services**:

```bash
# Switch from mock clients to real production services
USE_MOCK_CLIENTS=false

# Text & Table Builder v1.0
TEXT_SERVICE_URL=https://web-production-e3796.up.railway.app
TEXT_SERVICE_TIMEOUT=30

# Image Builder v2.0
IMAGE_SERVICE_URL=https://web-production-1b5df.up.railway.app
IMAGE_SERVICE_TIMEOUT=20

# Diagram Generator v3.0
DIAGRAM_SERVICE_URL=https://web-production-e0ad0.up.railway.app
DIAGRAM_SERVICE_TIMEOUT=60
DIAGRAM_POLL_INTERVAL=2

# Analytics Microservice v3
CHART_SERVICE_URL=https://analytics-v30-production.up.railway.app
CHART_SERVICE_TIMEOUT=60
CHART_POLL_INTERVAL=2
```

### Optional Variables (Already Have Defaults)

These are already configured in the code but can be overridden:

```bash
# Server configuration (Railway sets PORT automatically)
HOST=0.0.0.0
LOG_LEVEL=info

# CORS configuration
ALLOWED_ORIGINS=*
```

## 🔧 How to Set Environment Variables in Railway

1. Go to your Railway project dashboard
2. Select the Content Orchestrator v2.0 service
3. Click on "Variables" tab
4. Add each variable individually:
   - Click "New Variable"
   - Enter variable name (e.g., `USE_MOCK_CLIENTS`)
   - Enter variable value (e.g., `false`)
   - Click "Add"
5. Railway will automatically redeploy after adding variables

## ✅ Verify Deployment

Once Railway completes deployment, verify the service:

### Health Check
```bash
curl https://[your-railway-url]/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "content-orchestrator-v2",
  "version": "2.0.0",
  "timestamp": "2025-10-19T..."
}
```

### API Documentation
Visit: `https://[your-railway-url]/docs`

You should see interactive FastAPI documentation with:
- `/health` - Health check endpoint
- `/enrich` - Main enrichment endpoint
- `/status/{job_id}` - Job status endpoint (if async)

### Test Enrichment Endpoint

```bash
curl -X POST https://[your-railway-url]/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "presentation": {
      "main_title": "Test Presentation",
      "overall_theme": "Business",
      "target_audience": "Executives",
      "design_suggestions": "Modern",
      "presentation_duration": 10,
      "slides": [
        {
          "slide_number": 0,
          "slide_id": "slide_001",
          "title": "Q4 Results",
          "slide_type": "data_driven",
          "narrative": "Strong growth",
          "key_points": ["Revenue up 25%"],
          "analytics_needed": "Goal: Revenue trend, Content: Q4 data, Style: Line chart",
          "visuals_needed": null,
          "diagrams_needed": null,
          "tables_needed": null,
          "structure_preference": "two-column"
        }
      ]
    }
  }'
```

## 🏗️ Architecture

The deployed service will:
1. **Receive** presentation strawman via REST API
2. **Orchestrate** content generation across 4 production services:
   - Text & Table Builder (generates text and tables)
   - Image Builder (generates images)
   - Diagram Generator (generates diagrams)
   - Analytics Microservice (generates charts)
3. **Validate** generated content against layout constraints
4. **Return** enriched presentation with all content URLs

## 📊 Service Dependencies

This orchestrator depends on these Railway services being available:

| Service | URL | Status |
|---------|-----|--------|
| Text & Table Builder v1.0 | https://web-production-e3796.up.railway.app | ✅ |
| Image Builder v2.0 | https://web-production-1b5df.up.railway.app | ✅ |
| Diagram Generator v3.0 | https://web-production-e0ad0.up.railway.app | ✅ |
| Analytics Microservice v3 | https://analytics-v30-production.up.railway.app | ✅ |

## 🐛 Troubleshooting

### Issue: Service returns mock data instead of real content

**Solution**: Ensure `USE_MOCK_CLIENTS=false` is set in Railway environment variables

### Issue: Timeout errors when calling services

**Solution**: Increase timeout values:
```bash
TEXT_SERVICE_TIMEOUT=60
IMAGE_SERVICE_TIMEOUT=40
DIAGRAM_SERVICE_TIMEOUT=120
CHART_SERVICE_TIMEOUT=120
```

### Issue: CORS errors when calling from frontend

**Solution**: Update `ALLOWED_ORIGINS` to your frontend domain:
```bash
ALLOWED_ORIGINS=https://your-frontend.com,https://app.your-domain.com
```

### Issue: Service crashes on startup

**Check Railway logs** for errors. Common issues:
- Missing required dependencies (check requirements.txt)
- Invalid environment variables
- Port binding issues (Railway sets PORT automatically)

## 📝 Important Notes

1. **Railway auto-deploys** from GitHub main branch - any push triggers a new deployment
2. **Environment variables** must be set in Railway dashboard, not in code
3. **Health check** is configured in railway.json (path: /health, timeout: 100s)
4. **Restart policy** is set to ON_FAILURE with max 10 retries
5. **Region** is set to us-west1 (can be changed in railway.json)

## 🎯 Next Steps

After Railway deployment completes:

1. ✅ Verify health check endpoint
2. ✅ Test /docs API documentation
3. ✅ Test /enrich endpoint with sample presentation
4. ✅ Monitor Railway logs for any errors
5. ✅ Update frontend/clients with new orchestrator URL

## 🔗 Related Documentation

- **Streamlit UI**: See `README_STREAMLIT.md` for local testing interface
- **Integration Guide**: See `INTEGRATION_COMPLETE.md` for full integration details
- **Real Clients**: See `REAL_SERVICES_INTEGRATION.md` for client implementation
