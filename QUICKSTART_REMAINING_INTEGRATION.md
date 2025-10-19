# Quick Start: Complete Remaining Service Integrations

## What's Done ✅
- Text Service: Fully integrated and tested
- Environment configuration: All URLs in .env

## What's Left 🚧
You need to create 3 more client implementations following the exact same pattern as RealTextClient.

---

## Pattern to Follow

All clients follow the SAME structure as `clients/real_text_client.py`:

1. Import os, asyncio, requests, dotenv, logging
2. Load environment variables
3. Initialize with URL from environment
4. Implement `async def generate()` method
5. Use `run_in_executor()` for sync HTTP calls (Image) OR polling pattern (Diagram, Chart)
6. Transform requests/responses to match orchestrator models

---

## Quick Implementation Steps

### Step 1: Copy real_text_client.py as template
```bash
cp clients/real_text_client.py clients/real_image_client.py
```

### Step 2: Modify for Image service
- Change URL env var: `IMAGE_SERVICE_URL`
- Change endpoint: `/api/v2/generate`  
- Transform to `GeneratedImage` model instead of `GeneratedText`
- Request includes: `prompt`, `aspect_ratio`, `archetype`, `options`
- Response has: `urls{cropped, original}`, `image_id`, `metadata`

### Step 3: Diagram & Chart (Async Pattern)
These need polling instead of direct HTTP:

```python
# Submit job
job_response = await loop.run_in_executor(None, lambda: requests.post(...))
job_id = job_response["job_id"]

# Poll for completion
async def _poll_job(self, job_id):
    for attempt in range(max_attempts):
        await asyncio.sleep(self.poll_interval)  # Non-blocking!
        status = await loop.run_in_executor(None, lambda: requests.get(f"/status/{job_id}"))
        if status["status"] == "completed":
            return status["result"]
```

---

## Testing Pattern

Copy `tests/test_text_integration.py` and modify:
1. Change client import
2. Change request structure
3. Change assertions for response format
4. Run: `python3 tests/test_<service>_integration.py`

---

## Main.py Updates

For each service, update main.py:

```python
# Add import
from clients.real_image_client import RealImageClient

# Update initialization in lifespan()
image_client = RealImageClient()  # Instead of MockImageClient
```

---

## Service-Specific Details

### Image Service
- URL: IMAGE_SERVICE_URL
- Endpoint: POST /api/v2/generate
- Request: {prompt, aspect_ratio, archetype, options}
- Response: {urls{cropped, original}, image_id, metadata}
- Model: GeneratedImage

### Diagram Service  
- URL: DIAGRAM_SERVICE_URL
- Submit: POST /generate → {job_id}
- Poll: GET /status/{job_id}
- Request: {content, diagram_type, theme}
- Response: {diagram_url, diagram_type, metadata}
- Model: GeneratedDiagram

### Chart Service
- URL: CHART_SERVICE_URL
- Submit: POST /generate → {job_id}
- Poll: GET /status/{job_id}
- Request: {content, chart_type, data, theme}
- Response: {chart_url, chart_data, chart_type, metadata}
- Model: GeneratedChart

---

## Full Integration Test

Create `tests/test_full_integration.py`:

```python
from clients.real_text_client import RealTextClient
from clients.real_image_client import RealImageClient
from clients.real_diagram_client import RealDiagramClient
from clients.real_chart_client import RealChartClient

async def test_all():
    results = []
    
    # Test each service
    text_client = RealTextClient()
    text = await text_client.generate({...})
    results.append(("Text", bool(text.content)))
    
    # Repeat for image, diagram, chart
    
    # Print summary
    for service, passed in results:
        print(f"{service}: {'✅' if passed else '❌'}")
```

---

## Key Files Reference

- `clients/real_text_client.py` - Your working template
- `tests/test_text_integration.py` - Your working test template  
- `REAL_SERVICES_INTEGRATION.md` - Full API documentation
- `.env` - All service URLs configured

---

## Commands Summary

```bash
# Test individual services
python3 tests/test_text_integration.py
python3 tests/test_image_integration.py
python3 tests/test_diagram_integration.py
python3 tests/test_chart_integration.py

# Full integration
python3 tests/test_full_integration.py
```

---

