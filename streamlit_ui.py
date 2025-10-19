# -*- coding: utf-8 -*-
"""
Content Orchestrator v2.0 - Streamlit Testing Interface
=======================================================

Interactive web UI for testing the Content Orchestrator v2.0 with all 4 production services.

Features:
- Test individual services (Text, Image, Diagram, Chart)
- Test full orchestrator workflow
- Monitor service metrics and performance
- Switch between Mock and Production modes
- View generated content in real-time

Run with: streamlit run streamlit_ui.py
"""

import streamlit as st
from ui.utils import initialize_session_state, display_service_status
from ui.service_tester import (
    text_service_page,
    image_service_page,
    diagram_service_page,
    chart_service_page
)
from ui.orchestrator_tester import orchestrator_testing_page
from ui.metrics import metrics_dashboard_page


# Page configuration
st.set_page_config(
    page_title="Content Orchestrator v2.0 Testing",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Sidebar
with st.sidebar:
    st.title("🎯 Content Orchestrator v2.0")
    st.markdown("---")

    # Service mode toggle
    st.subheader("⚙️ Configuration")
    mode = st.radio(
        "Service Mode",
        ["Production", "Mock"],
        index=0 if st.session_state.service_mode == 'Production' else 1,
        help="Switch between production Railway services and mock clients"
    )

    # Update session state if mode changed
    if mode != st.session_state.service_mode:
        st.session_state.service_mode = mode
        st.rerun()

    st.markdown("---")

    # Service status
    display_service_status(mode)

    st.markdown("---")

    # Environment info
    st.subheader("📋 Environment")
    st.caption(f"**Version**: v2.0.0")
    st.caption(f"**Mode**: {mode}")
    if mode == 'Production':
        st.caption("**Deployment**: Railway")
        st.caption("**Services**: 4 microservices")
    else:
        st.caption("**Environment**: Local Mock")
        st.caption("**Response Delay**: 100-150ms")

# Main content area
st.title("🎯 Content Orchestrator v2.0 - Testing Interface")

# Navigation tabs
tabs = st.tabs([
    "🏠 Home",
    "📝 Text Service",
    "🎨 Image Service",
    "📊 Diagram Service",
    "📈 Chart Service",
    "🎯 Full Orchestrator",
    "📊 Metrics Dashboard"
])

# Home tab
with tabs[0]:
    st.header("Welcome to Content Orchestrator v2.0 Testing Interface")

    st.markdown("""
    This interactive testing interface allows you to test all components of the Content Orchestrator v2.0
    system with both **Production** (Railway deployment) and **Mock** services.
    """)

    # Overview cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔧 Individual Services")
        st.markdown("""
        Test each of the 4 microservices individually:
        - **Text & Table Builder** (Gemini 2.5-flash)
        - **Image Builder** (Imagen 3.0 Fast)
        - **Diagram Generator** (SVG/Mermaid)
        - **Analytics/Chart** (GPT-4o-mini)

        Each service can be tested with custom inputs and parameters.
        """)

    with col2:
        st.markdown("### 🎯 Full Orchestrator")
        st.markdown("""
        Test the complete presentation enrichment workflow:
        - Create test presentations with multiple slides
        - Run full async enrichment pipeline
        - Generate content using all 4 services
        - Validate results and compliance
        - Compare v1.0 vs v2.0 performance
        """)

    with col3:
        st.markdown("### 📊 Metrics Dashboard")
        st.markdown("""
        Monitor service performance:
        - Response time tracking
        - Success rate analysis
        - Service health monitoring
        - Historical metrics visualization
        - Export metrics data
        """)

    # Quick start guide
    st.markdown("---")
    st.subheader("🚀 Quick Start")

    st.markdown("""
    1. **Choose Service Mode** in the sidebar (Production or Mock)
    2. **Navigate to a tab** above to test individual services or the full orchestrator
    3. **Configure inputs** and click "Generate" to test the service
    4. **View results** including generated content, metadata, and metrics
    5. **Monitor performance** in the Metrics Dashboard tab
    """)

    # Architecture overview
    with st.expander("🏗️ Architecture Overview"):
        st.markdown("""
        ### Content Orchestrator v2.0 Architecture

        **Core Components:**
        - **ContentOrchestratorV2**: Lightweight async orchestration engine
        - **4 Production Microservices**: Text, Image, Diagram, Chart
        - **Validation System**: Slide compliance and quality checks
        - **Metrics Tracking**: Performance monitoring and analytics

        **Production Services (Railway Deployment):**
        1. **Text & Table Builder v1.0**
           - Model: Gemini 2.5-flash
           - Endpoint: https://text-table-builder-v1-production.up.railway.app
           - Features: Rich text generation, HTML tables, narrative content

        2. **Image Builder v2.0**
           - Model: Imagen 3.0 Fast
           - Endpoint: https://image-builder-service-production.up.railway.app
           - Features: Spot illustrations, photographs, various aspect ratios

        3. **Diagram Generator v3.0**
           - Methods: 21 SVG templates, 7 Mermaid types, 6 Python charts
           - Endpoint: https://web-production-e0ad0.up.railway.app
           - Features: Flowcharts, cycles, pyramids, timelines, etc.
           - Status: ✅ Operational (SVG generation validated)

        4. **Analytics/Chart Service v3**
           - Model: GPT-4o-mini (LLM-enhanced data synthesis)
           - Endpoint: https://analytics-microservice-v3-production.up.railway.app
           - Features: 20+ chart types, automatic data generation

        **Performance Improvements:**
        - Async/await patterns for concurrency
        - Parallel service calls where possible
        - Smart caching and polling strategies
        - Target: 3-5x faster than v1.0
        """)

    # Current status
    st.markdown("---")
    st.info(f"**Current Mode**: {mode} | **Status**: Ready for Testing")

# Text Service tab
with tabs[1]:
    text_service_page()

# Image Service tab
with tabs[2]:
    image_service_page()

# Diagram Service tab
with tabs[3]:
    diagram_service_page()

# Chart Service tab
with tabs[4]:
    chart_service_page()

# Full Orchestrator tab
with tabs[5]:
    orchestrator_testing_page()

# Metrics Dashboard tab
with tabs[6]:
    metrics_dashboard_page()

# Footer
st.markdown("---")
st.caption("Content Orchestrator v2.0 | Testing Interface | Built with Streamlit")
