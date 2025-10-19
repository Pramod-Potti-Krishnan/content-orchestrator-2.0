"""
Content Orchestrator v2.0 - FastAPI Application
================================================

Production-ready API for Railway deployment.

This service provides a REST API for content orchestration with:
- Health checks and status endpoints
- Async presentation enrichment
- Mock API clients (can be replaced with real clients)
- Comprehensive error handling
- CORS support for web clients
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import v2 orchestrator and clients
from core.orchestrator import ContentOrchestratorV2
from clients.mock_text_client import MockTextClient
from clients.mock_chart_client import MockChartClient
from clients.mock_image_client import MockImageClient
from clients.mock_diagram_client import MockDiagramClient

# Import models
from models.agents import PresentationStrawman, Slide
from models.layout_models import LayoutAssignment

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Content Orchestrator v2.0 API")
    global orchestrator

    # Initialize API clients (using mock clients for now)
    # Replace with real clients in production
    text_client = MockTextClient(delay_ms=int(os.getenv("TEXT_API_DELAY_MS", "100")))
    chart_client = MockChartClient(delay_ms=int(os.getenv("CHART_API_DELAY_MS", "150")))
    image_client = MockImageClient(delay_ms=int(os.getenv("IMAGE_API_DELAY_MS", "200")))
    diagram_client = MockDiagramClient(delay_ms=int(os.getenv("DIAGRAM_API_DELAY_MS", "150")))

    # Create orchestrator
    orchestrator = ContentOrchestratorV2(
        text_client=text_client,
        chart_client=chart_client,
        image_client=image_client,
        diagram_client=diagram_client
    )

    logger.info("Content Orchestrator v2.0 initialized successfully")

    yield

    # Shutdown
    logger.info("Shutting down Content Orchestrator v2.0 API")


# Create FastAPI app
app = FastAPI(
    title="Content Orchestrator v2.0",
    description="Fast, lightweight content orchestration API",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class EnrichPresentationRequest(BaseModel):
    """Request model for presentation enrichment."""
    strawman: PresentationStrawman
    layout_assignments: Optional[list[LayoutAssignment]] = None
    layout_specifications: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
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
                            "analytics_needed": False,
                            "visuals_needed": False
                        }
                    ]
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(default="healthy")
    version: str = Field(default="2.0.0")
    orchestrator: str = Field(default="ready")


# API Endpoints
@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Content Orchestrator v2.0",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        orchestrator="ready" if orchestrator is not None else "not_initialized"
    )


@app.post("/api/v2/enrich", response_class=JSONResponse)
async def enrich_presentation(request: EnrichPresentationRequest):
    """
    Enrich a presentation strawman with generated content.

    This endpoint:
    1. Receives a presentation strawman and optional layout assignments
    2. Uses the v2.0 orchestrator to generate content in parallel
    3. Returns enriched slides with validation reports

    Performance: <10s for 10 slides with mock APIs
    """
    if orchestrator is None:
        raise HTTPException(
            status_code=503,
            detail="Orchestrator not initialized"
        )

    try:
        logger.info(f"Enriching presentation: {request.strawman.main_title}")

        # Call orchestrator
        result = await orchestrator.enrich_presentation(
            strawman=request.strawman,
            layout_assignments=request.layout_assignments,
            layout_specifications=request.layout_specifications,
            progress_callback=None  # Can add WebSocket support for progress
        )

        # Convert to dict for JSON response
        response_data = {
            "original_strawman": result.original_strawman.model_dump(),
            "enriched_slides": [slide.model_dump() for slide in result.enriched_slides],
            "validation_report": result.validation_report.model_dump(),
            "generation_metadata": result.generation_metadata
        }

        logger.info(
            f"Enrichment complete: {result.validation_report.compliant_slides}/"
            f"{result.validation_report.total_slides} compliant slides"
        )

        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"Enrichment failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Enrichment failed: {str(e)}"
        )


@app.get("/api/v2/status", response_class=JSONResponse)
async def get_status():
    """Get detailed status information."""
    return {
        "orchestrator": {
            "version": "2.0.0",
            "architecture": "lightweight",
            "initialized": orchestrator is not None
        },
        "api_clients": {
            "text": "mock" if os.getenv("USE_MOCK_CLIENTS", "true") == "true" else "real",
            "chart": "mock" if os.getenv("USE_MOCK_CLIENTS", "true") == "true" else "real",
            "image": "mock" if os.getenv("USE_MOCK_CLIENTS", "true") == "true" else "real",
            "diagram": "mock" if os.getenv("USE_MOCK_CLIENTS", "true") == "true" else "real"
        },
        "environment": {
            "text_api_delay_ms": os.getenv("TEXT_API_DELAY_MS", "100"),
            "chart_api_delay_ms": os.getenv("CHART_API_DELAY_MS", "150"),
            "image_api_delay_ms": os.getenv("IMAGE_API_DELAY_MS", "200"),
            "diagram_api_delay_ms": os.getenv("DIAGRAM_API_DELAY_MS", "150")
        }
    }


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors."""
    logger.error(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"error": "Validation error", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# Run with uvicorn
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting server on {host}:{port}")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("RELOAD", "false").lower() == "true",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
