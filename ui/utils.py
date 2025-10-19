# -*- coding: utf-8 -*-
"""
UI Utility Functions for Streamlit Interface
=============================================

Helper functions for the Content Orchestrator v2.0 Streamlit UI.
"""

import time
from typing import Dict, Any, Optional, Tuple
import streamlit as st
from datetime import datetime

# Import clients
from clients.real_text_client import RealTextClient
from clients.real_image_client import RealImageClient
from clients.real_diagram_client import RealDiagramClient
from clients.real_chart_client import RealChartClient
from clients.mock_text_client import MockTextClient
from clients.mock_image_client import MockImageClient
from clients.mock_diagram_client import MockDiagramClient
from clients.mock_chart_client import MockChartClient


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {
            'text': [],
            'image': [],
            'diagram': [],
            'chart': [],
            'orchestrator': []  # Added for full orchestrator testing
        }
    if 'service_mode' not in st.session_state:
        st.session_state.service_mode = 'Production'
    if 'last_generation' not in st.session_state:
        st.session_state.last_generation = {}


def get_clients(mode: str = 'Production') -> Dict[str, Any]:
    """
    Get API clients based on selected mode.

    Args:
        mode: 'Production' or 'Mock'

    Returns:
        Dictionary of initialized clients
    """
    if mode == 'Production':
        return {
            'text': RealTextClient(),
            'image': RealImageClient(),
            'diagram': RealDiagramClient(),
            'chart': RealChartClient()
        }
    else:
        return {
            'text': MockTextClient(delay_ms=100),
            'image': MockImageClient(delay_ms=150),
            'diagram': MockDiagramClient(delay_ms=150),
            'chart': MockChartClient(delay_ms=150)
        }


def record_metric(service: str, response_time: float, success: bool, metadata: Dict = None):
    """
    Record a service call metric.

    Args:
        service: Service name ('text', 'image', 'diagram', 'chart')
        response_time: Response time in seconds
        success: Whether the call succeeded
        metadata: Additional metadata
    """
    if 'metrics' not in st.session_state:
        initialize_session_state()

    # Ensure service key exists in metrics dict
    if service not in st.session_state.metrics:
        st.session_state.metrics[service] = []

    metric_entry = {
        'timestamp': datetime.now(),
        'response_time': response_time,
        'success': success,
        'metadata': metadata or {}
    }

    st.session_state.metrics[service].append(metric_entry)


def format_response_time(seconds: float) -> str:
    """Format response time for display."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.2f}s"


def get_service_stats(service: str) -> Dict[str, Any]:
    """
    Get statistics for a service.

    Args:
        service: Service name

    Returns:
        Dictionary with stats
    """
    if service not in st.session_state.metrics:
        return {
            'total_calls': 0,
            'success_rate': 0,
            'avg_response_time': 0,
            'last_call': None
        }

    metrics = st.session_state.metrics[service]
    if not metrics:
        return {
            'total_calls': 0,
            'success_rate': 0,
            'avg_response_time': 0,
            'last_call': None
        }

    total_calls = len(metrics)
    successful = sum(1 for m in metrics if m['success'])
    success_rate = (successful / total_calls * 100) if total_calls > 0 else 0
    avg_time = sum(m['response_time'] for m in metrics) / total_calls if total_calls > 0 else 0

    return {
        'total_calls': total_calls,
        'success_rate': success_rate,
        'avg_response_time': avg_time,
        'last_call': metrics[-1]['timestamp'] if metrics else None
    }


def display_service_status(mode: str):
    """Display service status in sidebar."""
    st.sidebar.markdown("### 📊 Service Status")

    if mode == 'Production':
        st.sidebar.success("✅ Using Production Services")
        st.sidebar.caption("Railway deployment endpoints")
    else:
        st.sidebar.info("🧪 Using Mock Services")
        st.sidebar.caption("Local mock clients")

    # Display per-service stats
    for service in ['text', 'image', 'diagram', 'chart']:
        stats = get_service_stats(service)
        if stats['total_calls'] > 0:
            with st.sidebar.expander(f"{service.title()} Service"):
                st.metric("Total Calls", stats['total_calls'])
                st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
                st.metric("Avg Response", format_response_time(stats['avg_response_time']))


def display_error(error: Exception, service: str = ""):
    """Display error message in user-friendly format."""
    service_text = f" ({service} Service)" if service else ""
    st.error(f"❌ Error{service_text}")
    with st.expander("Error Details"):
        st.code(str(error))


def create_test_slide_data() -> Dict[str, Any]:
    """Create sample slide data for testing."""
    return {
        "slide_id": "test_slide_001",
        "slide_number": 1,
        "title": "Q3 Financial Performance",
        "narrative": "Strong revenue growth driven by increased market share",
        "key_points": [
            "Q3 revenue up 25% YoY",
            "EBITDA margin improved to 32%",
            "Customer acquisition cost down 15%"
        ]
    }


def validate_url(url: str) -> bool:
    """Validate that a URL is properly formed."""
    if not url:
        return False
    return url.startswith('http://') or url.startswith('https://')


def format_timestamp(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def export_metrics_to_dict() -> Dict[str, Any]:
    """Export all metrics to dictionary format."""
    if 'metrics' not in st.session_state:
        return {}

    export_data = {}
    for service, metrics_list in st.session_state.metrics.items():
        export_data[service] = [
            {
                'timestamp': format_timestamp(m['timestamp']),
                'response_time': m['response_time'],
                'success': m['success'],
                'metadata': m.get('metadata', {})
            }
            for m in metrics_list
        ]

    return export_data


def clear_metrics(service: Optional[str] = None):
    """
    Clear metrics for a service or all services.

    Args:
        service: Service name, or None to clear all
    """
    if 'metrics' not in st.session_state:
        return

    if service:
        st.session_state.metrics[service] = []
    else:
        for s in st.session_state.metrics:
            st.session_state.metrics[s] = []
