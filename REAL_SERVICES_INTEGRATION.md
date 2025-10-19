# Content Orchestrator v2.0 - Real Services Integration Guide

**Document Version**: 1.0
**Last Updated**: 2025-01-19
**Status**: Production Ready

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Service Profiles](#service-profiles)
3. [Integration Architecture](#integration-architecture)
4. [Client Implementation Guide](#client-implementation-guide)
5. [Code Examples](#code-examples)
6. [Migration Checklist](#migration-checklist)
7. [Performance Analysis](#performance-analysis)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Executive Summary

This document provides comprehensive guidance for integrating Content Orchestrator v2.0 with four production-ready microservices deployed on Railway. These services replace the mock clients currently used in v2.0.

### Service Mapping Overview

| Mock Client | Real Service | Production URL | API Type | Response Time |
|-------------|-------------|----------------|----------|---------------|
| `MockTextClient` | Text & Table Builder v1.0 | https://web-production-e3796.up.railway.app | Synchronous | 5-15s |
| `MockChartClient` | Analytics Microservice v3 | https://analytics-v30-production.up.railway.app | Async (Job-based) | Varies |
| `MockImageClient` | Image Builder v2.0 | https://web-production-1b5df.up.railway.app | Synchronous | 7-12s |
| `MockDiagramClient` | Diagram Generator v3.0 | https://web-production-e0ad0.up.railway.app | Async (Job-based) | <2s |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│         Content Orchestrator v2.0 (FastAPI)                 │
│  • Parallel API execution with asyncio.gather()             │
│  • Request building and result stitching                    │
└──────────┬──────────┬────────────┬─────────────────────────┘
           │          │            │            │
           │          │            │            │
    ┌──────▼──┐  ┌───▼────┐  ┌────▼────┐  ┌───▼─────┐
    │  Text   │  │Analytics│  │ Image   │  │Diagram  │
    │   &     │  │  Micro  │  │ Builder │  │Generator│
    │ Table   │  │ service │  │   v2    │  │   v3    │
    │Builder  │  │   v3    │  │         │  │         │
    │  v1.0   │  │         │  │         │  │         │
    └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
         │            │            │            │
         │            │            │            │
    SYNC│         ASYNC│       SYNC│       ASYNC│
         │      (polling)│          │     (polling)│
         ▼            ▼            ▼            ▼
    ┌────────────────────────────────────────────┐
    │        Supabase Storage & Database         │
    │    • Public URLs for generated content     │
    │    • Metadata tracking                     │
    └────────────────────────────────────────────┘
```

### Key Integration Challenges

1. **Mixed Async/Sync API Patterns**
   - Text & Image services return results immediately (synchronous)
   - Analytics & Diagram services use job polling (asynchronous)
   - Content Orchestrator needs unified async interface for all

2. **Session Management**
   - Text service uses `presentation_id` for context retention across slides
   - Must maintain session throughout presentation generation

3. **Parallel Execution Optimization**
   - Content Orchestrator uses `asyncio.gather()` for parallel execution
   - Async services need efficient polling without blocking
   - Synchronous services need async wrappers

4. **Response Format Transformation**
   - Each service has unique response schemas
   - Must transform to Content Orchestrator's expected format

---

## Service Profiles

### Service 1: Text & Table Builder v1.0

**Production URL**: `https://web-production-e3796.up.railway.app`

#### Purpose
LLM-powered HTML text and table generation for presentation slides with context retention.

#### Capabilities
- **Rich HTML Text Generation**: Semantic HTML with proper tags (p, ul, ol, strong, em, etc.)
- **Word Count Control**: ±10% tolerance with automatic optimization
- **Smart Table Generation**: LLM-optimized structures from JSON data or descriptions
- **Context Retention**: Session-based tracking of last 5 slides for coherent narrative
- **Multi-Provider LLM**: Supports Gemini (default), OpenAI, Anthropic

#### API Endpoints

##### POST `/api/v1/generate/text`
Generate HTML text content for a slide.

**Request Schema**:
```json
{
  "presentation_id": "pres_001",          // Required: Unique presentation ID
  "slide_id": "slide_001",                // Required: Slide identifier
  "slide_number": 1,                      // Required: Slide position
  "topics": [                             // Required: Key points to cover
    "Revenue growth",
    "Market expansion"
  ],
  "narrative": "Strong Q3 performance",   // Required: Overall slide narrative
  "context": {                            // Required: Presentation context
    "theme": "professional",
    "audience": "executives",
    "slide_title": "Q3 Results"
  },
  "constraints": {                        // Optional: Generation constraints
    "max_characters": 300,
    "style": "professional",
    "tone": "data-driven"
  }
}
```

**Response Schema**:
```json
{
  "content": "<p>Generated HTML content...</p>",
  "metadata": {
    "word_count": 48,
    "target_word_count": 54,
    "variance_percent": -11.1,
    "within_tolerance": false,
    "html_tags_used": ["p", "strong", "ul"],
    "generation_time_ms": 1245.3,
    "model_used": "gemini-2.5-flash",
    "provider": "gemini",
    "prompt_tokens": 456,
    "completion_tokens": 182
  }
}
```

##### POST `/api/v1/generate/table`
Generate HTML table from data.

**Request Schema**:
```json
{
  "presentation_id": "pres_001",
  "slide_id": "slide_002",
  "slide_number": 2,
  "description": "Regional revenue comparison Q2 vs Q3",
  "data": {
    "Q2": {"North America": 45.2, "Europe": 32.1},
    "Q3": {"North America": 58.3, "Europe": 39.4}
  },
  "context": {
    "theme": "professional",
    "audience": "executives",
    "slide_title": "Regional Performance"
  },
  "constraints": {
    "max_rows": 10,
    "max_columns": 5
  }
}
```

**Response Schema**:
```json
{
  "html": "<table class=\"data-table\">...</table>",
  "metadata": {
    "rows": 3,
    "columns": 4,
    "data_points": 12,
    "has_header": true,
    "numeric_columns": 3,
    "generation_time_ms": 1876.2
  }
}
```

##### GET `/api/v1/session/{presentation_id}`
Get session information.

**Response Schema**:
```json
{
  "presentation_id": "pres_001",
  "slides_in_context": 3,
  "context_size_bytes": 2458,
  "last_updated": "2024-01-15T10:30:00",
  "ttl_remaining_seconds": 3240
}
```

##### DELETE `/api/v1/session/{presentation_id}`
Delete session and context.

**Response**: `{"message": "Session deleted"}`

#### Performance Characteristics
- **Response Time**: 5-15 seconds (LLM generation)
- **Session TTL**: 1 hour (configurable)
- **Context Window**: Last 5 slides
- **Concurrent Requests**: Up to 10 simultaneous

#### Authentication
- No authentication required currently

#### Error Codes
- `200 OK` - Successful generation
- `400 Bad Request` - Invalid request format
- `404 Not Found` - Session not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error (retry recommended)

---

### Service 2: Analytics Microservice v3

**Production URL**: `https://analytics-v30-production.up.railway.app`

#### Purpose
Comprehensive chart and analytics generation with LLM-enhanced data synthesis.

#### Capabilities
- **20+ Chart Types**: Bar, line, pie, scatter, heatmap, violin, box, funnel, treemap, sankey
- **LLM Data Synthesis**: OpenAI GPT-4o-mini for intelligent data generation
- **Theme Customization**: 5 pre-defined themes (default, dark, professional, colorful, minimal)
- **Cloud Storage**: Supabase Storage with public URLs
- **Job Processing**: Async job-based with progress tracking

#### API Endpoints

##### POST `/generate`
Submit chart generation request (async job-based).

**Request Schema**:
```json
{
  "content": "Show quarterly revenue growth for 2024",
  "title": "Q1-Q4 2024 Revenue",             // Optional
  "data": [                                  // Optional user data
    {"label": "Q1", "value": 100},
    {"label": "Q2", "value": 150}
  ],
  "chart_type": "bar_vertical",              // Optional, defaults to bar_vertical
  "theme": "professional"                    // Optional: default, dark, professional, colorful, minimal
}
```

**Response Schema**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing"
}
```

##### GET `/status/{job_id}`
Poll for job status and results.

**Response (Processing)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 60,
  "stage": "chart_rendering",
  "created_at": "2025-01-19T10:30:00",
  "updated_at": "2025-01-19T10:30:15"
}
```

**Response (Completed)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "stage": "completed",
  "chart_url": "https://your-supabase-url.supabase.co/storage/v1/object/public/analytics-charts/chart_xyz.png",
  "chart_data": {
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "values": [25, 35, 30, 40],
    "title": "Q1-Q4 2024 Revenue"
  },
  "chart_type": "bar_vertical",
  "theme": "professional",
  "metadata": {
    "generated_at": "2025-01-19T10:30:20",
    "data_points": 4
  }
}
```

**Response (Failed)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "error": "Chart generation failed: Invalid chart type"
}
```

#### Available Chart Types
- `bar_vertical`, `bar_horizontal`, `bar_grouped`, `bar_stacked`
- `line`, `line_multi`, `area`, `area_stacked`
- `pie`, `donut`
- `scatter`, `bubble`
- `heatmap`, `radar`, `box`, `violin`
- `histogram`, `funnel`, `treemap`, `sankey`

#### Available Themes
- `default` - Clean blue theme
- `dark` - Dark mode with neon colors
- `professional` - Muted professional colors
- `colorful` - Bright, vibrant colors
- `minimal` - Grayscale minimalist

#### Performance Characteristics
- **Generation Time**: Varies by complexity
- **Job Cleanup**: 1 hour after completion
- **Polling Recommended**: 1-second intervals
- **Max Wait**: 60 seconds recommended

#### Authentication
- No authentication required currently

#### Error Codes
- `200 OK` - Job created or status retrieved
- `404 Not Found` - Job not found
- `500 Internal Server Error` - Generation failed

---

### Service 3: Image Builder v2.0

**Production URL**: `https://web-production-1b5df.up.railway.app`

#### Purpose
AI-powered image generation with custom aspect ratio support using Vertex AI Imagen 3.

#### Capabilities
- **Vertex AI Imagen 3**: High-quality AI image generation
- **Custom Aspect Ratios**: Any ratio (2:7, 21:9, 3:5, etc.) with intelligent cropping
- **Cloud Storage**: Supabase Storage with public URLs
- **Background Removal**: Optional transparency
- **Multiple Versions**: Original, cropped, transparent

#### API Endpoints

##### POST `/api/v2/generate`
Generate an AI image.

**Request Schema**:
```json
{
  "prompt": "A modern tech startup logo with blue gradient",
  "aspect_ratio": "2:7",                      // Default: "16:9"
  "archetype": "minimalist_vector_art",       // Default: "spot_illustration"
  "negative_prompt": "blurry, low quality",   // Optional
  "options": {
    "remove_background": true,                // Default: false
    "crop_anchor": "center",                  // center, top, bottom, left, right, smart
    "store_in_cloud": true,                   // Default: true
    "quality": "high"                         // high, medium
  },
  "metadata": {}                              // Optional metadata
}
```

**Response Schema**:
```json
{
  "success": true,
  "image_id": "123e4567-e89b-12d3-a456-426614174000",
  "urls": {
    "original": "https://your-project.supabase.co/storage/v1/object/public/generated-images/123e4567_original.png",
    "cropped": "https://your-project.supabase.co/storage/v1/object/public/generated-images/123e4567_cropped.png",
    "transparent": "https://your-project.supabase.co/storage/v1/object/public/generated-images/123e4567_transparent.png"
  },
  "metadata": {
    "model": "imagen-3.0-generate-002",
    "source_aspect_ratio": "9:16",
    "target_aspect_ratio": "2:7",
    "cropped": true,
    "background_removed": true,
    "generation_time_ms": 8500,
    "file_sizes": {
      "original_kb": 245,
      "cropped_kb": 180,
      "transparent_kb": 150
    }
  }
}
```

##### GET `/api/v2/health`
Health check endpoint.

**Response Schema**:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "services": {
    "vertex_ai": true,
    "supabase": true,
    "image_service": true
  },
  "timestamp": "2025-01-19T10:30:00"
}
```

#### Performance Characteristics
- **Generation Time**: 7-12 seconds average
- **Upload Time**: 1-2 seconds to Supabase
- **Total Response**: <15 seconds
- **Image Quality**: High (1024x1024 base)

#### Authentication
- Optional `X-API-Key` header

#### Error Codes
- `200 OK` - Image generated successfully
- `400 Bad Request` - Invalid request
- `500 Internal Server Error` - Generation failed

---

### Service 4: Diagram Generator v3.0

**Production URL**: `https://web-production-e0ad0.up.railway.app`

#### Purpose
SVG templates, Mermaid diagrams, and Python charts with AI-powered semantic routing.

#### Capabilities
- **21 SVG Templates**: Cycle, pyramid, venn, honeycomb, hub-spoke, matrix, funnel, timeline
- **7 Mermaid Types**: Flowchart, sequence, gantt, state, ER, journey, quadrant
- **6 Python Charts**: Pie, bar, line, scatter, network, sankey
- **AI Routing**: Google Gemini for intelligent diagram type selection
- **Smart Theming**: Customizable colors and styles
- **Job Processing**: Async with progress tracking

#### API Endpoints

##### POST `/generate`
Submit diagram generation request (async job-based).

**Request Schema**:
```json
{
  "content": "Step 1: Plan\nStep 2: Execute\nStep 3: Review",
  "diagram_type": "cycle_3_step",
  "data_points": [],                          // Optional structured data
  "theme": {
    "primaryColor": "#3B82F6",
    "secondaryColor": "#10B981",
    "style": "professional"                   // professional, playful, minimal, bold
  },
  "constraints": {
    "maxWidth": 800,
    "maxHeight": 600
  },
  "method": null                              // Force: svg_template, mermaid, python_chart
}
```

**Response Schema**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing"
}
```

##### GET `/status/{job_id}`
Poll for job status and results.

**Response (Completed)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "stage": "completed",
  "diagram_url": "https://your-supabase-url.supabase.co/storage/v1/object/public/diagram-charts/diagram_xyz.svg",
  "diagram_type": "cycle_3_step",
  "generation_method": "svg_template",
  "metadata": {
    "generation_time_ms": 245,
    "cache_hit": false,
    "dimensions": {"width": 800, "height": 600},
    "generated_at": "2025-01-19T10:30:20"
  },
  "completed_at": "2025-01-19T10:30:20"
}
```

#### Supported Diagram Types

**SVG Templates** (21 types):
- Cycle: `cycle_3_step`, `cycle_4_step`, `cycle_5_step`
- Pyramid: `pyramid_3_level`, `pyramid_4_level`, `pyramid_5_level`
- Venn: `venn_2_circle`, `venn_3_circle`
- Honeycomb: `honeycomb_3_cell`, `honeycomb_5_cell`, `honeycomb_7_cell`
- Hub & Spoke: `hub_spoke_4`, `hub_spoke_6`, `hub_spoke_8`
- Matrix: `matrix_2x2`, `matrix_3x3`
- Funnel: `funnel_3_stage`, `funnel_4_stage`, `funnel_5_stage`
- Timeline: `timeline_3_event`, `timeline_5_event`

**Mermaid** (7 types):
- `flowchart`, `sequence`, `gantt`, `state`, `erDiagram`, `journey`, `quadrantChart`

**Python Charts** (6 types):
- `pie`, `bar`, `line`, `scatter`, `network`, `sankey`

#### Performance Characteristics
- **SVG Templates**: <200ms
- **Mermaid Diagrams**: <500ms
- **Python Charts**: <2s
- **Cache Hit Rate**: 70%+

#### Authentication
- No authentication required currently

---

## Integration Architecture

### Overview
Content Orchestrator v2.0 uses a parallel execution model with `asyncio.gather()` to call multiple services simultaneously. The integration must handle:

1. **Mixed API Patterns**: Synchronous (Text, Image) and Asynchronous (Analytics, Diagram)
2. **Session Management**: Text service requires presentation_id for context retention
3. **Polling Logic**: Efficient polling for async services without blocking parallel execution
4. **Error Handling**: Graceful degradation when services fail
5. **Response Transformation**: Mapping service responses to Content Orchestrator format

### Integration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  Content Orchestrator v2.0: enrich_presentation()               │
│  • Receives PresentationStrawman with slides                    │
│  • Builds API requests from content guidance                    │
└────────────┬────────────────────────────────────────────────────┘
             │
             │ RequestBuilder.build_api_requests()
             ▼
┌─────────────────────────────────────────────────────────────────┐
│  APIDispatcher: Parallel Execution (asyncio.gather)             │
│  ┌──────────┬──────────────┬──────────────┬──────────────┐     │
│  │  Text    │  Analytics   │  Image       │  Diagram     │     │
│  │  Client  │  Client      │  Client      │  Client      │     │
│  │  (sync)  │  (async poll)│  (sync)      │  (async poll)│     │
│  └──────┬───┴──────┬───────┴──────┬───────┴──────┬───────┘     │
│         │          │              │              │             │
│         ▼          ▼              ▼              ▼             │
│    ┌────────┬────────────┬────────────┬─────────────┐         │
│    │ Await  │ Job Submit │  Await     │ Job Submit  │         │
│    │ Result │ + Poll     │  Result    │ + Poll      │         │
│    └────┬───┴─────┬──────┴─────┬──────┴──────┬──────┘         │
│         │         │            │             │                │
└─────────┼─────────┼────────────┼─────────────┼────────────────┘
          │         │            │             │
          ▼         ▼            ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│  ResultStitcher: Combine Results                                │
│  • Transform service responses to EnrichedSlide format          │
│  • Add metadata (generation times, URLs, etc.)                  │
│  • Handle partial failures                                      │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│  SLAValidator: Minimal Validation                               │
│  • Required fields present                                      │
│  • Critical violations only                                     │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│  Return EnrichedPresentationStrawman                            │
│  • enriched_slides: List[EnrichedSlide]                         │
│  • validation_report: ValidationReport                          │
│  • generation_metadata: Dict with stats                         │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

#### 1. Unified Async Interface
All clients must expose async methods even if the underlying API is synchronous:

```python
class RealTextClient:
    async def generate(self, request: Dict) -> GeneratedText:
        # Wrap synchronous HTTP call in async
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_generate, request)

    def _sync_generate(self, request: Dict) -> GeneratedText:
        response = requests.post(self.url, json=request)
        return self._transform_response(response.json())
```

#### 2. Efficient Polling for Async Services
Async services need non-blocking polling:

```python
class RealChartClient:
    async def generate(self, request: Dict) -> GeneratedChart:
        # Submit job
        job_response = requests.post(f"{self.base_url}/generate", json=request)
        job_id = job_response.json()["job_id"]

        # Poll asynchronously
        max_attempts = 60
        for attempt in range(max_attempts):
            await asyncio.sleep(1)  # Non-blocking sleep

            status_response = requests.get(f"{self.base_url}/status/{job_id}")
            status = status_response.json()

            if status["status"] == "completed":
                return self._transform_response(status)
            elif status["status"] == "failed":
                raise RuntimeError(f"Chart generation failed: {status.get('error')}")

        raise TimeoutError("Chart generation timed out")
```

#### 3. Session Management for Text Service
Text service requires session management:

```python
class RealTextClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.active_sessions = {}  # Track presentation sessions

    async def generate(self, request: Dict) -> GeneratedText:
        presentation_id = request.get("presentation_id")

        # Register session on first call
        if presentation_id not in self.active_sessions:
            self.active_sessions[presentation_id] = True

        # Generate content (session automatically managed by service)
        response = await self._make_request(request)
        return response

    async def cleanup_session(self, presentation_id: str):
        """Call at end of presentation generation"""
        if presentation_id in self.active_sessions:
            requests.delete(f"{self.base_url}/api/v1/session/{presentation_id}")
            del self.active_sessions[presentation_id]
```

#### 4. Response Transformation
Each service returns different schemas - transform to standard format:

```python
class RealTextClient:
    def _transform_response(self, service_response: Dict) -> GeneratedText:
        """Transform Text service response to Content Orchestrator format"""
        return GeneratedText(
            content=service_response["content"],
            word_count=service_response["metadata"]["word_count"],
            generation_time_ms=service_response["metadata"]["generation_time_ms"],
            model_used=service_response["metadata"]["model_used"],
            html_tags=service_response["metadata"]["html_tags_used"]
        )

class RealChartClient:
    def _transform_response(self, service_response: Dict) -> GeneratedChart:
        """Transform Analytics service response to Content Orchestrator format"""
        return GeneratedChart(
            chart_url=service_response["chart_url"],
            chart_data=service_response["chart_data"],
            chart_type=service_response["chart_type"],
            generation_time_ms=service_response["metadata"].get("generation_time_ms", 0)
        )
```

---

## Client Implementation Guide

This section provides detailed implementation guidance for each client replacement.

### 1. RealTextClient (replaces MockTextClient)

#### Request Transformation

**From Content Orchestrator**:
```python
{
    "slide_id": "slide_001",
    "topics": ["Revenue growth", "Market expansion"],
    "narrative": "Strong Q3 performance",
    "max_characters": 300
}
```

**To Text Service**:
```python
{
    "presentation_id": "pres_001",              # From presentation context
    "slide_id": "slide_001",
    "slide_number": 1,                          # From slide position
    "topics": ["Revenue growth", "Market expansion"],
    "narrative": "Strong Q3 performance",
    "context": {
        "theme": "professional",                # From presentation theme
        "audience": "executives",               # From presentation audience
        "slide_title": "Q3 Results"            # From slide title
    },
    "constraints": {
        "max_characters": 300
    }
}
```

#### Implementation Pattern

```python
import requests
import asyncio
from typing import Dict, Any

class RealTextClient:
    """Client for Text & Table Builder v1.0"""

    def __init__(self, base_url: str = "https://web-production-e3796.up.railway.app"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api/v1"
        self.timeout = 30
        self.active_sessions = set()

    async def generate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate HTML text content (async wrapper around sync API)"""
        # Transform request
        service_request = self._transform_request(request)

        # Track session
        presentation_id = service_request["presentation_id"]
        self.active_sessions.add(presentation_id)

        # Make synchronous request in thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self._sync_generate_text,
            service_request
        )

        return self._transform_response(response)

    def _sync_generate_text(self, request: Dict) -> Dict:
        """Synchronous HTTP call to text service"""
        response = requests.post(
            f"{self.api_base}/generate/text",
            json=request,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def _transform_request(self, orchestrator_request: Dict) -> Dict:
        """Transform Content Orchestrator format to Text service format"""
        return {
            "presentation_id": orchestrator_request.get("presentation_id"),
            "slide_id": orchestrator_request["slide_id"],
            "slide_number": orchestrator_request.get("slide_number", 1),
            "topics": orchestrator_request.get("topics", []),
            "narrative": orchestrator_request.get("narrative", ""),
            "context": {
                "theme": orchestrator_request.get("theme", "professional"),
                "audience": orchestrator_request.get("audience", "general"),
                "slide_title": orchestrator_request.get("slide_title", "")
            },
            "constraints": {
                "max_characters": orchestrator_request.get("max_characters", 300)
            }
        }

    def _transform_response(self, service_response: Dict) -> Dict:
        """Transform Text service response to Content Orchestrator format"""
        return {
            "content": service_response["content"],
            "metadata": {
                "word_count": service_response["metadata"]["word_count"],
                "generation_time_ms": service_response["metadata"]["generation_time_ms"],
                "model_used": service_response["metadata"]["model_used"],
                "html_tags": service_response["metadata"]["html_tags_used"]
            }
        }

    async def cleanup_session(self, presentation_id: str):
        """Clean up session after presentation completion"""
        if presentation_id in self.active_sessions:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    None,
                    lambda: requests.delete(
                        f"{self.api_base}/session/{presentation_id}",
                        timeout=5
                    )
                )
                self.active_sessions.remove(presentation_id)
            except Exception as e:
                print(f"Failed to cleanup session {presentation_id}: {e}")
```

### 2. RealChartClient (replaces MockChartClient)

#### Request Transformation

**From Content Orchestrator**:
```python
{
    "slide_id": "slide_002",
    "chart_type": "bar",
    "data": [{"label": "Q1", "value": 100}]
}
```

**To Analytics Service**:
```python
{
    "content": "Show quarterly revenue for 2024",
    "title": "Q1-Q4 Revenue",
    "chart_type": "bar_vertical",
    "theme": "professional",
    "data": [{"label": "Q1", "value": 100}]
}
```

#### Implementation Pattern

```python
import requests
import asyncio
from typing import Dict, Any

class RealChartClient:
    """Client for Analytics Microservice v3"""

    def __init__(self, base_url: str = "https://analytics-v30-production.up.railway.app"):
        self.base_url = base_url
        self.timeout = 60
        self.poll_interval = 1.0

    async def generate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate chart with polling for async completion"""
        # Transform request
        service_request = self._transform_request(request)

        # Submit job
        job_id = await self._submit_job(service_request)

        # Poll for completion
        result = await self._poll_job(job_id)

        return self._transform_response(result)

    async def _submit_job(self, request: Dict) -> str:
        """Submit chart generation job"""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(
                f"{self.base_url}/generate",
                json=request,
                timeout=10
            )
        )
        response.raise_for_status()
        return response.json()["job_id"]

    async def _poll_job(self, job_id: str) -> Dict:
        """Poll for job completion (non-blocking)"""
        max_attempts = int(self.timeout / self.poll_interval)

        for attempt in range(max_attempts):
            await asyncio.sleep(self.poll_interval)

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.get(
                    f"{self.base_url}/status/{job_id}",
                    timeout=5
                )
            )
            response.raise_for_status()
            status = response.json()

            if status["status"] == "completed":
                return status
            elif status["status"] == "failed":
                raise RuntimeError(f"Chart generation failed: {status.get('error')}")

        raise TimeoutError(f"Chart generation timed out after {self.timeout}s")

    def _transform_request(self, orchestrator_request: Dict) -> Dict:
        """Transform Content Orchestrator format to Analytics format"""
        return {
            "content": orchestrator_request.get("description", ""),
            "title": orchestrator_request.get("title", "Chart"),
            "chart_type": orchestrator_request.get("chart_type", "bar_vertical"),
            "theme": orchestrator_request.get("theme", "professional"),
            "data": orchestrator_request.get("data")
        }

    def _transform_response(self, service_response: Dict) -> Dict:
        """Transform Analytics response to Content Orchestrator format"""
        return {
            "chart_url": service_response["chart_url"],
            "chart_data": service_response["chart_data"],
            "chart_type": service_response["chart_type"],
            "metadata": {
                "generation_time_ms": service_response.get("metadata", {}).get("generation_time_ms", 0),
                "theme": service_response.get("theme", "professional")
            }
        }
```

### 3. RealImageClient (replaces MockImageClient)

#### Request Transformation

**From Content Orchestrator**:
```python
{
    "slide_id": "slide_003",
    "prompt": "Modern tech startup logo",
    "aspect_ratio": "2:7"
}
```

**To Image Service**:
```python
{
    "prompt": "Modern tech startup logo",
    "aspect_ratio": "2:7",
    "archetype": "minimalist_vector_art",
    "options": {
        "remove_background": true,
        "crop_anchor": "center",
        "store_in_cloud": true
    }
}
```

#### Implementation Pattern

```python
import requests
import asyncio
from typing import Dict, Any, Optional

class RealImageClient:
    """Client for Image Builder v2.0"""

    def __init__(self, base_url: str = "https://web-production-1b5df.up.railway.app"):
        self.base_url = base_url
        self.timeout = 30

    async def generate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI image (async wrapper around sync API)"""
        # Transform request
        service_request = self._transform_request(request)

        # Make synchronous request in thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self._sync_generate_image,
            service_request
        )

        return self._transform_response(response)

    def _sync_generate_image(self, request: Dict) -> Dict:
        """Synchronous HTTP call to image service"""
        response = requests.post(
            f"{self.base_url}/api/v2/generate",
            json=request,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def _transform_request(self, orchestrator_request: Dict) -> Dict:
        """Transform Content Orchestrator format to Image service format"""
        return {
            "prompt": orchestrator_request["prompt"],
            "aspect_ratio": orchestrator_request.get("aspect_ratio", "16:9"),
            "archetype": orchestrator_request.get("archetype", "minimalist_vector_art"),
            "options": {
                "remove_background": orchestrator_request.get("remove_background", True),
                "crop_anchor": orchestrator_request.get("crop_anchor", "center"),
                "store_in_cloud": True
            }
        }

    def _transform_response(self, service_response: Dict) -> Dict:
        """Transform Image service response to Content Orchestrator format"""
        if not service_response.get("success"):
            raise RuntimeError(f"Image generation failed: {service_response.get('error')}")

        return {
            "image_url": service_response["urls"]["cropped"],  # Use cropped version
            "image_id": service_response["image_id"],
            "metadata": {
                "generation_time_ms": service_response["metadata"]["generation_time_ms"],
                "aspect_ratio": service_response["metadata"]["target_aspect_ratio"],
                "model": service_response["metadata"]["model"]
            }
        }
```

### 4. RealDiagramClient (replaces MockDiagramClient)

#### Request Transformation

**From Content Orchestrator**:
```python
{
    "slide_id": "slide_004",
    "diagram_type": "cycle_3_step",
    "content": "Plan\\nExecute\\nReview"
}
```

**To Diagram Service**:
```python
{
    "content": "Plan\\nExecute\\nReview",
    "diagram_type": "cycle_3_step",
    "theme": {
        "primaryColor": "#3B82F6",
        "style": "professional"
    }
}
```

#### Implementation Pattern

```python
import requests
import asyncio
from typing import Dict, Any

class RealDiagramClient:
    """Client for Diagram Generator v3.0"""

    def __init__(self, base_url: str = "https://web-production-e0ad0.up.railway.app"):
        self.base_url = base_url
        self.timeout = 30
        self.poll_interval = 1.0

    async def generate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diagram with polling for async completion"""
        # Transform request
        service_request = self._transform_request(request)

        # Submit job
        job_id = await self._submit_job(service_request)

        # Poll for completion
        result = await self._poll_job(job_id)

        return self._transform_response(result)

    async def _submit_job(self, request: Dict) -> str:
        """Submit diagram generation job"""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(
                f"{self.base_url}/generate",
                json=request,
                timeout=10
            )
        )
        response.raise_for_status()
        return response.json()["job_id"]

    async def _poll_job(self, job_id: str) -> Dict:
        """Poll for job completion (non-blocking)"""
        max_attempts = int(self.timeout / self.poll_interval)

        for attempt in range(max_attempts):
            await asyncio.sleep(self.poll_interval)

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.get(
                    f"{self.base_url}/status/{job_id}",
                    timeout=5
                )
            )
            response.raise_for_status()
            status = response.json()

            if status["status"] == "completed":
                return status
            elif status["status"] == "failed":
                raise RuntimeError(f"Diagram generation failed: {status.get('error')}")

        raise TimeoutError(f"Diagram generation timed out after {self.timeout}s")

    def _transform_request(self, orchestrator_request: Dict) -> Dict:
        """Transform Content Orchestrator format to Diagram format"""
        return {
            "content": orchestrator_request["content"],
            "diagram_type": orchestrator_request["diagram_type"],
            "theme": {
                "primaryColor": orchestrator_request.get("primary_color", "#3B82F6"),
                "style": orchestrator_request.get("style", "professional")
            }
        }

    def _transform_response(self, service_response: Dict) -> Dict:
        """Transform Diagram service response to Content Orchestrator format"""
        return {
            "diagram_url": service_response["diagram_url"],
            "diagram_type": service_response["diagram_type"],
            "metadata": {
                "generation_time_ms": service_response["metadata"]["generation_time_ms"],
                "generation_method": service_response["generation_method"]
            }
        }
```

---

## Code Examples

### Complete Integration Example

This example shows how to integrate all four real clients into Content Orchestrator v2.0.

```python
# clients/real_clients_factory.py
"""Factory for creating real service clients"""

from clients.real_text_client import RealTextClient
from clients.real_chart_client import RealChartClient
from clients.real_image_client import RealImageClient
from clients.real_diagram_client import RealDiagramClient

def create_production_clients():
    """Create all production clients with Railway URLs"""
    return {
        "text_client": RealTextClient(
            base_url="https://web-production-e3796.up.railway.app"
        ),
        "chart_client": RealChartClient(
            base_url="https://analytics-v30-production.up.railway.app"
        ),
        "image_client": RealImageClient(
            base_url="https://web-production-1b5df.up.railway.app"
        ),
        "diagram_client": RealDiagramClient(
            base_url="https://web-production-e0ad0.up.railway.app"
        )
    }

def create_local_clients():
    """Create clients for local development"""
    return {
        "text_client": RealTextClient(base_url="http://localhost:8001"),
        "chart_client": RealChartClient(base_url="http://localhost:8002"),
        "image_client": RealImageClient(base_url="http://localhost:8003"),
        "diagram_client": RealDiagramClient(base_url="http://localhost:8004")
    }
```

### Updated main.py

```python
# main.py
import os
from fastapi import FastAPI
from dotenv import load_dotenv

from core.orchestrator import ContentOrchestratorV2
from clients.real_clients_factory import create_production_clients, create_local_clients

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Content Orchestrator v2.0",
    version="2.0.0"
)

# Create clients based on environment
USE_PRODUCTION = os.getenv("USE_PRODUCTION_SERVICES", "true") == "true"

if USE_PRODUCTION:
    clients = create_production_clients()
else:
    clients = create_local_clients()

# Create orchestrator with real clients
orchestrator = ContentOrchestratorV2(
    text_client=clients["text_client"],
    chart_client=clients["chart_client"],
    image_client=clients["image_client"],
    diagram_client=clients["diagram_client"]
)

@app.post("/api/v2/enrich")
async def enrich_presentation(request: dict):
    """Enrich presentation with real services"""
    result = await orchestrator.enrich_presentation(
        strawman=request["strawman"],
        layout_assignments=request.get("layout_assignments"),
        layout_specifications=request.get("layout_specifications")
    )

    return {
        "enriched_slides": [slide.dict() for slide in result.enriched_slides],
        "validation_report": result.validation_report.dict(),
        "generation_metadata": result.generation_metadata
    }
```

### Parallel Execution Example

```python
# Example showing how real clients work with asyncio.gather()

async def enrich_multiple_slides(slides: List[Dict]):
    """Process multiple slides in parallel"""

    # Create tasks for parallel execution
    tasks = []
    for slide in slides:
        if slide.get("needs_text"):
            tasks.append(text_client.generate(slide["text_request"]))
        if slide.get("needs_chart"):
            tasks.append(chart_client.generate(slide["chart_request"]))
        if slide.get("needs_image"):
            tasks.append(image_client.generate(slide["image_request"]))
        if slide.get("needs_diagram"):
            tasks.append(diagram_client.generate(slide["diagram_request"]))

    # Execute all tasks in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle results
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded")

    return results
```

---

## Migration Checklist

### Pre-Migration

- [ ] **Review Service READMEs**: Ensure understanding of all 4 services
- [ ] **Test Services Individually**: Verify all production APIs are working
- [ ] **Document Current Mock Behavior**: Baseline for comparison
- [ ] **Set Up Environment Variables**: Configure production URLs

### Environment Configuration

Add to `.env`:
```bash
# Production Services
USE_PRODUCTION_SERVICES=true

# Service URLs
TEXT_SERVICE_URL=https://web-production-e3796.up.railway.app
CHART_SERVICE_URL=https://analytics-v30-production.up.railway.app
IMAGE_SERVICE_URL=https://web-production-1b5df.up.railway.app
DIAGRAM_SERVICE_URL=https://web-production-e0ad0.up.railway.app

# Timeouts
TEXT_SERVICE_TIMEOUT=30
CHART_SERVICE_TIMEOUT=60
IMAGE_SERVICE_TIMEOUT=30
DIAGRAM_SERVICE_TIMEOUT=30

# Polling Configuration
CHART_POLL_INTERVAL=1.0
DIAGRAM_POLL_INTERVAL=1.0
```

### Dependencies

Add to `requirements.txt`:
```
requests>=2.31.0
httpx>=0.24.0  # Optional: for better async HTTP support
```

### Implementation Steps

1. **Create Real Client Classes** (Priority: High)
   - [ ] Implement `clients/real_text_client.py`
   - [ ] Implement `clients/real_chart_client.py`
   - [ ] Implement `clients/real_image_client.py`
   - [ ] Implement `clients/real_diagram_client.py`
   - [ ] Create `clients/real_clients_factory.py`

2. **Update Content Orchestrator** (Priority: High)
   - [ ] Modify `main.py` to use real clients
   - [ ] Update environment variable handling
   - [ ] Add client initialization logic

3. **Testing** (Priority: Critical)
   - [ ] Unit tests for each client
   - [ ] Integration tests with real services
   - [ ] End-to-end presentation generation test
   - [ ] Load testing for parallel execution
   - [ ] Error handling tests

4. **Documentation Updates** (Priority: Medium)
   - [ ] Update README.md with real service integration
   - [ ] Document environment variables
   - [ ] Add troubleshooting guide

5. **Monitoring & Logging** (Priority: Medium)
   - [ ] Add logging for service calls
   - [ ] Track response times
   - [ ] Monitor error rates

### Post-Migration

- [ ] **Validate Performance**: Compare with mock client baseline
- [ ] **Monitor Production**: Track errors and response times
- [ ] **Session Cleanup**: Verify text service sessions are cleaned up
- [ ] **Cost Monitoring**: Track API usage and costs

---

## Performance Analysis

### Expected Response Times

| Service | Operation | Expected Time | Mock Time | Difference |
|---------|-----------|---------------|-----------|------------|
| Text Service | Generate text | 5-15s | 0.1s | +5-15s |
| Analytics | Generate chart | Variable | 0.15s | +Variable |
| Image Service | Generate image | 7-12s | 0.2s | +7-12s |
| Diagram Service | Generate diagram | <2s | 0.15s | +<2s |

### Parallel Execution Impact

**With Mock Clients** (10 slides):
- 10 slides × 0.2s (mock delay) = ~2s total (with parallel execution)

**With Real Services** (10 slides):
- Text: 5-15s (slowest determines overall time)
- Charts: Variable (polling overhead)
- Images: 7-12s
- Diagrams: <2s

**Expected Total Time**: 15-25s for 10 slides (still significantly faster than v1.0's 110s)

### Optimization Strategies

1. **Connection Pooling**: Reuse HTTP connections
2. **Timeout Tuning**: Set appropriate timeouts per service
3. **Retry Logic**: Implement exponential backoff
4. **Caching**: Cache frequently generated content
5. **Batch Operations**: Use batch endpoints where available (Text service)

### Bottleneck Identification

**Primary Bottleneck**: Text service (5-15s per request)
**Mitigation**:
- Use batch endpoint when generating multiple text blocks
- Implement caching for similar content
- Consider request coalescing

**Secondary Bottleneck**: Image service (7-12s per request)
**Mitigation**:
- Pre-generate common images
- Use lower quality setting for drafts
- Cache generated images

---

## Troubleshooting Guide

### Common Issues

#### 1. Connection Timeouts

**Symptom**: `requests.exceptions.Timeout` errors

**Cause**: Service taking longer than configured timeout

**Solution**:
```python
# Increase timeout for specific service
text_client = RealTextClient(base_url="...", timeout=60)
```

#### 2. Job Polling Failures

**Symptom**: "Job not found" errors when polling

**Cause**: Job already cleaned up or invalid job_id

**Solution**:
```python
# Increase polling frequency, reduce max wait time
async def _poll_job(self, job_id: str) -> Dict:
    max_attempts = 120  # Increase from 60
    poll_interval = 0.5  # Decrease from 1.0
    # ... rest of polling logic
```

#### 3. Session Not Found (Text Service)

**Symptom**: 404 errors when generating text for later slides

**Cause**: Session expired (1-hour TTL)

**Solution**:
- Generate all slides for a presentation within 1 hour
- Or increase session TTL via Text service environment variable

#### 4. Mixed Results in Parallel Execution

**Symptom**: Some slides succeed, others fail

**Cause**: One service failing doesn't stop others

**Solution**:
```python
# Use return_exceptions=True in asyncio.gather
results = await asyncio.gather(*tasks, return_exceptions=True)

# Handle exceptions gracefully
for i, result in enumerate(results):
    if isinstance(result, Exception):
        logger.error(f"Task {i} failed: {result}")
        # Continue with partial results
```

#### 5. Rate Limiting

**Symptom**: 429 Too Many Requests errors

**Cause**: Exceeding service rate limits

**Solution**:
- Implement request queuing
- Add delays between requests
- Use batch endpoints

### Health Check Procedures

#### Quick Health Check Script

```python
# quick_health_check.py
import requests

SERVICES = {
    "Text": "https://web-production-e3796.up.railway.app/health",
    "Analytics": "https://analytics-v30-production.up.railway.app/health",
    "Image": "https://web-production-1b5df.up.railway.app/api/v2/health",
    "Diagram": "https://web-production-e0ad0.up.railway.app/health"
}

def check_all_services():
    for name, url in SERVICES.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} Service: HEALTHY")
            else:
                print(f"❌ {name} Service: UNHEALTHY (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ {name} Service: UNREACHABLE ({e})")

if __name__ == "__main__":
    check_all_services()
```

### Debugging Steps

1. **Enable Verbose Logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Test Service Independently**:
```python
# Test text service directly
import requests
response = requests.post(
    "https://web-production-e3796.up.railway.app/api/v1/generate/text",
    json={...}
)
print(response.json())
```

3. **Check Service Status**:
```bash
# Health check
curl https://web-production-e3796.up.railway.app/health

# Check job status
curl https://analytics-v30-production.up.railway.app/status/job-id
```

4. **Monitor Response Times**:
```python
import time

start = time.time()
result = await client.generate(request)
elapsed = time.time() - start
print(f"Generation took {elapsed:.2f}s")
```

### Contact & Support

- **Text Service Issues**: Check Text & Table Builder v1.0 README
- **Analytics Issues**: Check Analytics Microservice v3 README
- **Image Issues**: Check Image Builder v2.0 README
- **Diagram Issues**: Check Diagram Generator v3.0 README

---

## Appendix

### A. Service URL Reference

| Service | Production URL | Health Check | Documentation |
|---------|---------------|--------------|---------------|
| Text & Table Builder | https://web-production-e3796.up.railway.app | /health | /docs |
| Analytics Microservice | https://analytics-v30-production.up.railway.app | /health | /docs |
| Image Builder | https://web-production-1b5df.up.railway.app | /api/v2/health | /docs |
| Diagram Generator | https://web-production-e0ad0.up.railway.app | /health | /docs |

### B. Response Schema Quick Reference

**Text Service**:
```json
{"content": "HTML", "metadata": {...}}
```

**Analytics Service** (after polling):
```json
{"chart_url": "URL", "chart_data": {...}, "chart_type": "type"}
```

**Image Service**:
```json
{"success": true, "urls": {...}, "metadata": {...}}
```

**Diagram Service** (after polling):
```json
{"diagram_url": "URL", "diagram_type": "type", "metadata": {...}}
```

### C. Environment Variables Reference

```bash
# Service URLs
TEXT_SERVICE_URL=https://web-production-e3796.up.railway.app
CHART_SERVICE_URL=https://analytics-v30-production.up.railway.app
IMAGE_SERVICE_URL=https://web-production-1b5df.up.railway.app
DIAGRAM_SERVICE_URL=https://web-production-e0ad0.up.railway.app

# Timeouts (seconds)
TEXT_SERVICE_TIMEOUT=30
CHART_SERVICE_TIMEOUT=60
IMAGE_SERVICE_TIMEOUT=30
DIAGRAM_SERVICE_TIMEOUT=30

# Polling Configuration
CHART_POLL_INTERVAL=1.0
DIAGRAM_POLL_INTERVAL=1.0
CHART_MAX_WAIT=60
DIAGRAM_MAX_WAIT=30

# Feature Flags
USE_PRODUCTION_SERVICES=true
ENABLE_SERVICE_CACHING=false
ENABLE_RETRY_LOGIC=true
```

---

**Document Status**: Complete ✅
**Next Steps**: Implement real client classes → Test integration → Deploy to production

**Last Updated**: 2025-01-19
**Maintained By**: Content Orchestrator Development Team
