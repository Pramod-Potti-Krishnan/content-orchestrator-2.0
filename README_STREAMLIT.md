# Content Orchestrator v2.0 - Streamlit Testing Interface

Interactive web UI for testing the Content Orchestrator v2.0 with all 4 production Railway services.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)
- All dependencies from `requirements.txt`

### Installation

1. **Navigate to the v2 directory:**
   ```bash
   cd agents/content_orchestrator/v2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (if using production services):
   ```bash
   # Copy example env file if available
   cp .env.example .env

   # Edit .env with your API keys (if required)
   ```

4. **Run the Streamlit UI:**
   ```bash
   streamlit run streamlit_ui.py
   ```

5. **Open in browser:**
   - The UI should automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## 📋 Features

### 🏠 Home Page
- Overview of the Content Orchestrator v2.0 system
- Architecture documentation
- Quick start guide
- Service endpoint information

### 🔧 Individual Service Testing

Test each microservice individually with custom inputs:

#### 📝 Text & Table Builder Service
- **Model:** Gemini 2.5-flash
- **Test:** Rich text generation, HTML tables, narrative content
- **Inputs:** Topics, narrative, context
- **Output:** Generated HTML content with metadata

#### 🎨 Image Builder Service
- **Model:** Imagen 3.0 Fast
- **Test:** Spot illustrations, photographs, vector art
- **Inputs:** Prompt, aspect ratio (16:9, 4:3, 1:1, etc.), style
- **Output:** Generated image with URL and metadata

#### 📊 Diagram Generator Service
- **Methods:** SVG templates, Mermaid, Python charts
- **Test:** Flowcharts, cycles, pyramids, timelines, etc.
- **Inputs:** Content, diagram type, theme colors
- **Output:** Generated diagram SVG with metadata

#### 📈 Analytics/Chart Service
- **Model:** GPT-4o-mini (LLM-enhanced data synthesis)
- **Test:** 20+ chart types with automatic data generation
- **Inputs:** Content description, title, chart type, theme
- **Output:** Generated chart image with data and metadata

### 🎯 Full Orchestrator Testing

Test the complete presentation enrichment workflow:

- Create test presentations with 1-10 slides
- Run full async enrichment pipeline
- Generate content using all 4 services simultaneously
- Validate results and compliance
- Compare v1.0 vs v2.0 performance
- View detailed progress logs
- Inspect enriched slides with generated content

**Features:**
- Progress bar with real-time updates
- Summary metrics (total time, time/slide, compliance rate)
- Generation metadata (successful items, failed items, API requests)
- Validation report (compliant slides, violations)
- Performance comparison showing speedup vs v1.0

### 📊 Metrics Dashboard

Monitor service performance and health:

- **Overall Statistics:** Total calls, success rates for all 4 services
- **Response Time Charts:** Interactive Plotly visualizations
- **Per-Service Details:**
  - Total calls and success rate
  - Average response time
  - Response time trends over time (color-coded by success/failure)
  - Recent calls table
- **Export Metrics:** Download metrics data as JSON
- **Clear Metrics:** Reset metrics for individual services or all

## ⚙️ Configuration

### Service Mode Toggle

Switch between two modes in the sidebar:

#### 🌐 Production Mode
- Uses actual Railway deployment endpoints
- Real API calls to production microservices
- Response times: 2-10 seconds per service
- **Requires:** Active Railway deployments and valid API credentials

**Production Endpoints:**
- Text: `https://text-table-builder-v1-production.up.railway.app`
- Image: `https://image-builder-service-production.up.railway.app`
- Diagram: `https://diagram-microservice-v2-production.up.railway.app`
- Chart: `https://analytics-microservice-v3-production.up.railway.app`

#### 🧪 Mock Mode
- Uses local mock clients for development
- Fast responses: 100-150ms
- No API keys required
- Great for UI testing and development

**Toggle between modes:**
- Use the radio buttons in the sidebar under "Configuration"
- Changes take effect immediately with automatic page refresh

## 📁 File Structure

```
v2/
├── streamlit_ui.py              # Main Streamlit application (entry point)
├── ui/                          # UI components module
│   ├── __init__.py             # Module initialization
│   ├── utils.py                # Helper functions (session state, clients, metrics)
│   ├── service_tester.py       # Individual service testing pages
│   ├── orchestrator_tester.py  # Full orchestrator testing page
│   └── metrics.py              # Metrics dashboard page
├── requirements.txt             # Python dependencies (includes Streamlit)
└── README_STREAMLIT.md         # This file
```

## 🎯 Usage Examples

### Testing Individual Services

1. **Navigate to a service tab** (Text, Image, Diagram, or Chart)
2. **Choose service mode** (Production or Mock) in sidebar
3. **Fill in input parameters:**
   - For Text: Topics, narrative, context
   - For Image: Prompt, aspect ratio, style
   - For Diagram: Content, diagram type, colors
   - For Chart: Data description, title, chart type
4. **Click "Generate"** button
5. **View results:**
   - Generated content (text/image/diagram/chart)
   - Metadata (model, generation time, etc.)
   - Recorded in metrics automatically

### Testing Full Orchestrator

1. **Navigate to "Full Orchestrator" tab**
2. **Choose service mode** in sidebar
3. **Set number of slides** (1-10) using slider
4. **Click "Run Full Enrichment Test"**
5. **Watch progress bar** with real-time updates
6. **Review results:**
   - Summary metrics and performance comparison
   - Generation metadata and validation report
   - Individual enriched slides with content
   - Progress log of all operations

### Viewing Metrics

1. **Navigate to "Metrics Dashboard" tab**
2. **View overall statistics** across all services
3. **Explore response time charts** (interactive Plotly graphs)
4. **Click on service tabs** for detailed per-service metrics
5. **Export metrics** as JSON for analysis
6. **Clear metrics** when needed (per-service or all)

## 🔍 Troubleshooting

### Issue: Services not responding in Production mode

**Possible causes:**
- Railway services are down or sleeping
- API credentials missing or invalid
- Network connectivity issues

**Solutions:**
1. Check Railway deployment status
2. Verify environment variables and API keys
3. Try Mock mode to verify UI functionality
4. Check service URLs in sidebar service status

### Issue: Streamlit won't start

**Solutions:**
1. Ensure dependencies are installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.9+)
3. Try running with verbose flag: `streamlit run streamlit_ui.py --logger.level=debug`

### Issue: Async errors in service calls

**Solutions:**
1. This is handled automatically by the UI using `asyncio.new_event_loop()`
2. If errors persist, check that service clients are properly implemented
3. Review error details in the expandable "Error Details" section

### Issue: Metrics not recording

**Solutions:**
1. Check that `record_metric()` is called after each service call
2. Verify session state is initialized: Check sidebar for metrics
3. Try clearing browser cache and restarting Streamlit

## 📊 Performance Benchmarks

### Expected Response Times

**Production Mode:**
- Text Service: 2-5 seconds
- Image Service: 3-8 seconds
- Diagram Service: 2-6 seconds
- Chart Service: 2-5 seconds
- Full Orchestrator (3 slides): 15-30 seconds

**Mock Mode:**
- All services: 100-150ms
- Full Orchestrator (3 slides): ~500ms

### Performance Comparison

**v1.0 (Sequential):**
- Average: ~11 seconds per slide
- 3 slides: ~33 seconds
- 10 slides: ~110 seconds

**v2.0 (Async + Parallel):**
- Average: ~3-5 seconds per slide
- 3 slides: ~10-15 seconds (3-5x faster)
- 10 slides: ~35-50 seconds (2-3x faster)

## 🛠️ Development

### Running in Development Mode

```bash
# Use Mock mode for fast iteration
streamlit run streamlit_ui.py

# Enable auto-reload (default in Streamlit)
# Just save files and UI will reload automatically
```

### Adding New Features

1. **New service page:** Add function to `ui/service_tester.py`
2. **New metrics:** Update `ui/metrics.py` and `record_metric()` in `ui/utils.py`
3. **New navigation tab:** Add tab to `streamlit_ui.py` main tabs list

### Code Style

- Follow existing patterns in UI modules
- Use type hints for function parameters
- Add docstrings to all functions
- Keep pages modular and focused

## 📝 Environment Variables

The UI works with or without environment variables:

**Optional (for Production mode):**
```bash
# Add to .env if services require authentication
TEXT_SERVICE_API_KEY=your_key_here
IMAGE_SERVICE_API_KEY=your_key_here
DIAGRAM_SERVICE_API_KEY=your_key_here
CHART_SERVICE_API_KEY=your_key_here
```

**Note:** Current production services don't require API keys, but this may change.

## 🎨 Customization

### Changing UI Theme

Streamlit uses `.streamlit/config.toml` for theming:

```toml
[theme]
primaryColor = "#3B82F6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Modifying Service Endpoints

Edit the client files in `clients/` directory:
- `clients/real_text_client.py`
- `clients/real_image_client.py`
- `clients/real_diagram_client.py`
- `clients/real_chart_client.py`

## 📚 Additional Resources

- **Streamlit Documentation:** https://docs.streamlit.io
- **Plotly Documentation:** https://plotly.com/python/
- **Content Orchestrator v2.0 Main README:** See `README.md` in parent directory
- **API Documentation:** See individual service repositories

## 🆘 Support

For issues or questions:
1. Check this README and troubleshooting section
2. Review error messages in UI (expandable error details)
3. Check Streamlit logs in terminal
4. Verify service endpoints and deployment status

## 📄 License

Part of the Content Orchestrator v2.0 project.

---

**Version:** 2.0.0
**Last Updated:** 2025
**Built with:** Streamlit, Plotly, FastAPI, Pydantic
