# Content Orchestrator v2.0 - API Documentation

## 📋 Overview

The Content Orchestrator v2.0 is a production-ready REST API service that enriches presentation slides by orchestrating content generation across multiple specialized microservices. It takes a presentation "strawman" (outline) and returns fully enriched slides with generated text, charts, images, and diagrams.

**Production Service URL**: `https://web-production-3b42.up.railway.app`

---

## 🎯 What It Does

The Content Orchestrator:
1. Receives a presentation outline (strawman) with slide specifications
2. Analyzes each slide's content requirements (text, charts, images, diagrams)
3. Orchestrates parallel calls to specialized generation services
4. Validates generated content against layout constraints
5. Returns enriched slides with all content URLs and metadata

---

## 🔗 Base URL

```
https://web-production-3b42.up.railway.app
```

---

## 📡 API Endpoints

### 1. Health Check

**GET** `/health`

Check if the service is operational.

**Response**:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "orchestrator": "ready"
}
```

**Example**:
```bash
curl https://web-production-3b42.up.railway.app/health
```

---

### 2. Enrich Presentation (Main Endpoint)

**POST** `/api/v2/enrich`

Enrich a presentation strawman with generated content.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body Schema**:

```json
{
  "strawman": {
    "main_title": "string",
    "overall_theme": "string",
    "target_audience": "string",
    "design_suggestions": "string",
    "presentation_duration": number,
    "slides": [
      {
        "slide_number": number,
        "slide_id": "string",
        "title": "string",
        "slide_type": "string",
        "narrative": "string",
        "key_points": ["string"],
        "analytics_needed": "string | null",
        "visuals_needed": "string | null",
        "diagrams_needed": "string | null",
        "tables_needed": "string | null",
        "structure_preference": "string",
        "speaker_notes": "string | null"
      }
    ]
  }
}
```

**Field Descriptions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `strawman.main_title` | string | Yes | Main title of the presentation |
| `strawman.overall_theme` | string | Yes | Overall theme/topic |
| `strawman.target_audience` | string | Yes | Target audience description |
| `strawman.design_suggestions` | string | Yes | Design preferences |
| `strawman.presentation_duration` | number | Yes | Duration in minutes |
| `strawman.slides` | array | Yes | Array of slide objects |
| `slide.slide_number` | number | Yes | Slide index (0-based) |
| `slide.slide_id` | string | Yes | Unique slide identifier |
| `slide.title` | string | Yes | Slide title |
| `slide.slide_type` | string | Yes | Type: `"data_driven"`, `"visual_heavy"`, `"text_heavy"`, etc. |
| `slide.narrative` | string | Yes | Main narrative/message |
| `slide.key_points` | array | Yes | Array of key points (strings) |
| `slide.analytics_needed` | string or null | No | Chart/analytics requirements (format: "Goal: X, Content: Y, Style: Z") |
| `slide.visuals_needed` | string or null | No | Image requirements (format: "Goal: X, Content: Y, Style: Z") |
| `slide.diagrams_needed` | string or null | No | Diagram requirements (format: "Goal: X, Content: Y, Style: Z") |
| `slide.tables_needed` | string or null | No | Table requirements |
| `slide.structure_preference` | string | Yes | Layout preference: `"single-column"`, `"two-column"`, `"three-column"` |
| `slide.speaker_notes` | string or null | No | Optional speaker notes |

**Response Schema**:

```json
{
  "original_strawman": { /* Echo of input strawman */ },
  "enriched_slides": [
    {
      "original_slide": { /* Original slide input */ },
      "slide_id": "string",
      "layout_id": "string",
      "generated_content": {
        "slide_title": "string",
        "subtitle": "string",
        "chart_url": "string | null",
        "chart_data": { /* Chart data object */ },
        "image_url": "string | null",
        "diagram_url": "string | null",
        "key_insights": ["string"],
        "table_data": { /* Table data */ },
        "summary": "string"
      },
      "validation_status": {
        "compliant": boolean,
        "violations": []
      }
    }
  ],
  "validation_report": {
    "overall_compliant": boolean,
    "total_slides": number,
    "compliant_slides": number,
    "total_violations": number,
    "critical_violations": number
  },
  "generation_metadata": {
    "total_items_generated": number,
    "successful_items": number,
    "failed_items": number,
    "generation_time_seconds": number,
    "timestamp": "string",
    "failures": [],
    "orchestrator_version": "string",
    "architecture": "string",
    "total_api_requests": number
  }
}
```

**Response Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `enriched_slides[].layout_id` | string | Assigned layout ID (e.g., "L17", "L18") |
| `enriched_slides[].generated_content.chart_url` | string | URL to generated chart (Supabase Storage) |
| `enriched_slides[].generated_content.image_url` | string | URL to generated image (Supabase Storage) |
| `enriched_slides[].generated_content.diagram_url` | string | URL to generated diagram (Supabase Storage) |
| `enriched_slides[].generated_content.key_insights` | array | Generated text insights (HTML formatted) |
| `enriched_slides[].validation_status.compliant` | boolean | Whether slide meets layout constraints |
| `validation_report.overall_compliant` | boolean | Whether all slides are compliant |
| `generation_metadata.generation_time_seconds` | number | Total generation time |
| `generation_metadata.successful_items` | number | Number of successfully generated items |
| `generation_metadata.failed_items` | number | Number of failed generation attempts |

---

## 📝 Complete Example Request

```bash
curl -X POST https://web-production-3b42.up.railway.app/api/v2/enrich \
  -H "Content-Type: application/json" \
  -d '{
    "strawman": {
      "main_title": "Q4 2024 Business Review",
      "overall_theme": "Financial Performance and Strategic Growth",
      "target_audience": "Board of Directors and Executive Team",
      "design_suggestions": "Professional corporate theme with clean layouts",
      "presentation_duration": 30,
      "slides": [
        {
          "slide_number": 0,
          "slide_id": "slide_001",
          "title": "Revenue Growth Overview",
          "slide_type": "data_driven",
          "narrative": "Q4 demonstrated exceptional revenue growth across all segments",
          "key_points": [
            "Revenue increased 25% year-over-year",
            "EBITDA margin improved to 32%",
            "Customer acquisition costs decreased 15%"
          ],
          "analytics_needed": "Goal: Show quarterly revenue trend, Content: Q4 revenue by segment, Style: Line chart with growth indicators",
          "visuals_needed": null,
          "diagrams_needed": null,
          "tables_needed": null,
          "structure_preference": "two-column",
          "speaker_notes": "Emphasize the YoY growth and margin improvement"
        },
        {
          "slide_number": 1,
          "slide_id": "slide_002",
          "title": "Market Expansion Strategy",
          "slide_type": "visual_heavy",
          "narrative": "Strategic expansion into emerging markets drives future growth",
          "key_points": [
            "Entered 3 new geographic markets",
            "Established partnerships with 12 regional distributors",
            "Market share increased in target segments"
          ],
          "analytics_needed": null,
          "visuals_needed": "Goal: Show global expansion, Content: World map with new markets highlighted, Style: Professional infographic",
          "diagrams_needed": "Goal: Illustrate expansion process, Content: Strategic market entry workflow, Style: Process flowchart",
          "tables_needed": null,
          "structure_preference": "single-column",
          "speaker_notes": null
        },
        {
          "slide_number": 2,
          "slide_id": "slide_003",
          "title": "Operational Efficiency Gains",
          "slide_type": "data_driven",
          "narrative": "Process optimization delivered significant cost savings",
          "key_points": [
            "Operating costs reduced by 18%",
            "Automation increased productivity by 30%",
            "Supply chain efficiency improved"
          ],
          "analytics_needed": "Goal: Compare cost efficiency, Content: Cost reduction by category, Style: Bar chart showing savings",
          "visuals_needed": null,
          "diagrams_needed": null,
          "tables_needed": null,
          "structure_preference": "two-column",
          "speaker_notes": "Highlight automation ROI and efficiency metrics"
        }
      ]
    }
  }'
```

---

## 📊 Example Response

```json
{
  "original_strawman": {
    "type": "PresentationStrawman",
    "main_title": "Q4 2024 Business Review",
    "overall_theme": "Financial Performance and Strategic Growth",
    "slides": [ /* ... */ ]
  },
  "enriched_slides": [
    {
      "original_slide": {
        "slide_number": 0,
        "slide_id": "slide_001",
        "title": "Revenue Growth Overview",
        /* ... */
      },
      "slide_id": "slide_001",
      "layout_id": "L17",
      "generated_content": {
        "slide_title": "Revenue Growth Overview",
        "subtitle": "Q4 demonstrated exceptional revenue growth across all segments",
        "chart_url": "https://eshvntffcestlfuofwhv.supabase.co/storage/v1/object/public/analytics-charts/line_20251019_221710_7a71941b.png",
        "chart_data": {
          "labels": ["Q1", "Q2", "Q3", "Q4"],
          "values": [100000, 120000, 145000, 181250],
          "title": "Quarterly Revenue Growth"
        },
        "key_insights": [
          "<p>Q4 2024 showcased <strong>exceptional revenue growth</strong> across all segments.</p><h3>Key Highlights</h3><ul><li>Revenue increased by <span class=\"metric positive\">25% YoY</span></li><li>EBITDA margin improved to <span class=\"metric\">32%</span></li><li>Customer acquisition costs decreased <span class=\"metric positive\">15%</span></li></ul>"
        ],
        "summary": "Q4 demonstrated exceptional revenue growth across all segments"
      },
      "validation_status": {
        "compliant": true,
        "violations": []
      }
    },
    /* Additional enriched slides... */
  ],
  "validation_report": {
    "overall_compliant": true,
    "total_slides": 3,
    "compliant_slides": 3,
    "total_violations": 0,
    "critical_violations": 0
  },
  "generation_metadata": {
    "total_items_generated": 6,
    "successful_items": 6,
    "failed_items": 0,
    "generation_time_seconds": 18.45,
    "timestamp": "2025-10-19T22:30:00.000000",
    "failures": [],
    "orchestrator_version": "2.0",
    "architecture": "lightweight",
    "total_api_requests": 6
  }
}
```

---

## 🎨 Content Generation Rules

### Analytics (Charts)
**Triggered when**: `analytics_needed` field is not null

**Format**: `"Goal: [purpose], Content: [data description], Style: [chart type]"`

**Example**: `"Goal: Show revenue trend, Content: Q4 revenue by segment, Style: Line chart with growth indicators"`

**Generated Content**:
- `chart_url`: Public URL to chart image (PNG)
- `chart_data`: Chart data structure

**Supported Chart Types**:
- Line charts
- Bar charts
- Pie charts
- Area charts
- Mixed charts

---

### Visuals (Images)
**Triggered when**: `visuals_needed` field is not null

**Format**: `"Goal: [purpose], Content: [image description], Style: [visual style]"`

**Example**: `"Goal: Show team, Content: Executive leadership group photo, Style: Professional corporate"`

**Generated Content**:
- `image_url`: Public URL to generated image

---

### Diagrams
**Triggered when**: `diagrams_needed` field is not null

**Format**: `"Goal: [purpose], Content: [diagram description], Style: [diagram type]"`

**Example**: `"Goal: Illustrate workflow, Content: Sales process steps, Style: Process flowchart"`

**Generated Content**:
- `diagram_url`: Public URL to diagram (SVG)

**Supported Diagram Types**:
- Flowcharts
- Process diagrams
- Organization charts
- System diagrams
- Cycle diagrams

---

### Text & Insights
**Triggered**: Automatically for all slides

**Generated Content**:
- `key_insights`: Array of HTML-formatted insights
- `summary`: Text summary
- `slide_title`: Enhanced title
- `subtitle`: Enhanced subtitle

---

## 📐 Layout Assignment

The orchestrator automatically assigns optimal layouts based on:
- Content types present (text, chart, image, diagram)
- Structure preference (single/two/three column)
- Content constraints

**Example Layout IDs**:
- `L17`: Two-column with chart and text
- `L18`: Single-column visual-heavy
- `L19`: Three-column mixed content

---

## ⚡ Performance Characteristics

| Metric | Typical Value |
|--------|---------------|
| **Response Time (1 slide)** | 5-8 seconds |
| **Response Time (3 slides)** | 15-25 seconds |
| **Response Time (10 slides)** | 50-90 seconds |
| **Concurrent Requests** | Up to 10 simultaneous |
| **Max Slides per Request** | 50 slides recommended |
| **Timeout** | 120 seconds (configurable) |

**Note**: Generation time depends on:
- Number of slides
- Content types requested (charts take 2-6s, images take 3-8s, diagrams take 2-5s)
- Complexity of content requirements

---

## 🔧 Integration Code Examples

### Python Example

```python
import requests
import json

def enrich_presentation(strawman_data):
    """
    Enrich a presentation using the Content Orchestrator API.

    Args:
        strawman_data: Dictionary containing presentation strawman

    Returns:
        Enriched presentation data
    """
    url = "https://web-production-3b42.up.railway.app/api/v2/enrich"
    headers = {"Content-Type": "application/json"}

    payload = {"strawman": strawman_data}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()

        result = response.json()

        print(f"✅ Enriched {result['validation_report']['total_slides']} slides")
        print(f"⏱️  Generation time: {result['generation_metadata']['generation_time_seconds']}s")
        print(f"✅ Success rate: {result['generation_metadata']['successful_items']}/{result['generation_metadata']['total_items_generated']}")

        return result

    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling orchestrator: {e}")
        return None

# Example usage
strawman = {
    "main_title": "Q4 Business Review",
    "overall_theme": "Financial Performance",
    "target_audience": "Board of Directors",
    "design_suggestions": "Professional",
    "presentation_duration": 20,
    "slides": [
        {
            "slide_number": 0,
            "slide_id": "slide_001",
            "title": "Revenue Growth",
            "slide_type": "data_driven",
            "narrative": "Strong Q4 performance",
            "key_points": ["Revenue up 25%", "EBITDA at 32%"],
            "analytics_needed": "Goal: Show trend, Content: Revenue, Style: Line chart",
            "visuals_needed": None,
            "diagrams_needed": None,
            "tables_needed": None,
            "structure_preference": "two-column",
            "speaker_notes": None
        }
    ]
}

result = enrich_presentation(strawman)

# Access generated content
if result and result['enriched_slides']:
    for slide in result['enriched_slides']:
        print(f"\nSlide: {slide['slide_id']}")
        print(f"Layout: {slide['layout_id']}")

        content = slide['generated_content']
        if content.get('chart_url'):
            print(f"Chart: {content['chart_url']}")
        if content.get('image_url'):
            print(f"Image: {content['image_url']}")
        if content.get('diagram_url'):
            print(f"Diagram: {content['diagram_url']}")
```

---

### JavaScript/TypeScript Example

```typescript
interface Strawman {
  main_title: string;
  overall_theme: string;
  target_audience: string;
  design_suggestions: string;
  presentation_duration: number;
  slides: Slide[];
}

interface Slide {
  slide_number: number;
  slide_id: string;
  title: string;
  slide_type: string;
  narrative: string;
  key_points: string[];
  analytics_needed?: string | null;
  visuals_needed?: string | null;
  diagrams_needed?: string | null;
  tables_needed?: string | null;
  structure_preference: string;
  speaker_notes?: string | null;
}

async function enrichPresentation(strawman: Strawman) {
  const url = 'https://web-production-3b42.up.railway.app/api/v2/enrich';

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ strawman }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    console.log(`✅ Enriched ${result.validation_report.total_slides} slides`);
    console.log(`⏱️  Generation time: ${result.generation_metadata.generation_time_seconds}s`);

    return result;

  } catch (error) {
    console.error('❌ Error calling orchestrator:', error);
    throw error;
  }
}

// Example usage
const strawman: Strawman = {
  main_title: 'Q4 Business Review',
  overall_theme: 'Financial Performance',
  target_audience: 'Board of Directors',
  design_suggestions: 'Professional',
  presentation_duration: 20,
  slides: [
    {
      slide_number: 0,
      slide_id: 'slide_001',
      title: 'Revenue Growth',
      slide_type: 'data_driven',
      narrative: 'Strong Q4 performance',
      key_points: ['Revenue up 25%', 'EBITDA at 32%'],
      analytics_needed: 'Goal: Show trend, Content: Revenue, Style: Line chart',
      visuals_needed: null,
      diagrams_needed: null,
      tables_needed: null,
      structure_preference: 'two-column',
      speaker_notes: null,
    },
  ],
};

enrichPresentation(strawman)
  .then((result) => {
    result.enriched_slides.forEach((slide: any) => {
      console.log(`\nSlide: ${slide.slide_id}`);
      console.log(`Layout: ${slide.layout_id}`);

      const content = slide.generated_content;
      if (content.chart_url) console.log(`Chart: ${content.chart_url}`);
      if (content.image_url) console.log(`Image: ${content.image_url}`);
      if (content.diagram_url) console.log(`Diagram: ${content.diagram_url}`);
    });
  })
  .catch((error) => {
    console.error('Failed to enrich presentation:', error);
  });
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| `200` | Success | Request processed successfully |
| `400` | Bad Request | Invalid request body or missing required fields |
| `422` | Validation Error | Request body doesn't match expected schema |
| `500` | Internal Server Error | Server-side error during processing |
| `503` | Service Unavailable | Service temporarily unavailable |

### Error Response Format

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "strawman"],
      "msg": "Field required",
      "input": { /* ... */ }
    }
  ]
}
```

### Common Errors and Solutions

**Error**: `Field required: strawman`
**Solution**: Ensure request body has `strawman` field (not `presentation`)

**Error**: `422 Validation Error`
**Solution**: Check that all required slide fields are present and correctly typed

**Error**: `Timeout`
**Solution**: Reduce number of slides or increase client timeout (generation can take 5-10s per slide)

**Error**: `Service unavailable`
**Solution**: Retry after a few seconds (service may be restarting)

---

## 🔐 Authentication

**Current Status**: No authentication required (public API)

**Future**: May require API key authentication
```
Authorization: Bearer YOUR_API_KEY
```

---

## 📊 Rate Limits

**Current Limits**: None enforced

**Recommendations**:
- Maximum 10 concurrent requests per client
- Maximum 50 slides per request
- Allow 10 seconds per slide for processing

---

## 🐛 Troubleshooting

### Issue: Slow response times

**Causes**:
- Large number of slides (>20)
- Multiple content types per slide
- Downstream service latency

**Solutions**:
- Break large presentations into smaller batches
- Process slides asynchronously if possible
- Implement retry logic with exponential backoff

---

### Issue: Failed content generation

**Symptoms**:
- `failed_items` > 0 in response
- Missing `chart_url`, `image_url`, or `diagram_url`

**Solutions**:
- Check `generation_metadata.failures` for error details
- Verify content requirement format matches specification
- Retry failed items individually

---

### Issue: Validation errors

**Symptoms**:
- `validation_status.compliant` = false
- Violations listed in response

**Solutions**:
- Check `validation_status.violations` for specific issues
- Adjust slide content or structure_preference
- Consult layout constraints documentation

---

## 📚 Additional Resources

- **API Documentation (Swagger UI)**: https://web-production-3b42.up.railway.app/docs
- **Health Check**: https://web-production-3b42.up.railway.app/health
- **GitHub Repository**: https://github.com/Pramod-Potti-Krishnan/content-orchestrator-2.0
- **Test Report**: See `RAILWAY_TEST_REPORT.md` for comprehensive test results

---

## 📞 Support

For issues or questions about the Content Orchestrator API:
1. Check the Swagger UI documentation at `/docs`
2. Review test examples in `RAILWAY_TEST_REPORT.md`
3. Check Railway deployment logs for errors

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| **2.0.0** | 2025-10-19 | Production release with Railway deployment |
| - | - | Integrated with 4 production microservices |
| - | - | Added comprehensive validation |
| - | - | Improved performance and error handling |

---

## ✅ Quick Start Checklist

For the Director service to integrate with the Content Orchestrator:

- [ ] Use base URL: `https://web-production-3b42.up.railway.app`
- [ ] Send POST requests to `/api/v2/enrich`
- [ ] Use `strawman` field in request body (not `presentation`)
- [ ] Include all required slide fields
- [ ] Set request timeout to at least 120 seconds
- [ ] Handle 200 responses with enriched content
- [ ] Extract URLs from `generated_content` (chart_url, image_url, diagram_url)
- [ ] Check `validation_status.compliant` for layout compliance
- [ ] Monitor `generation_metadata.failed_items` for failures
- [ ] Implement retry logic for failed items

---

**Last Updated**: 2025-10-19
**Service Status**: ✅ Production Ready
**Deployment**: Railway (Auto-deploy from GitHub)
