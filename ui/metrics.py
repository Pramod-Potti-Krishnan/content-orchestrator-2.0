# -*- coding: utf-8 -*-
"""
Metrics Dashboard Component
============================

Streamlit component for displaying service metrics and performance analytics.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, List

from ui.utils import (
    get_service_stats,
    format_response_time,
    format_timestamp,
    export_metrics_to_dict,
    clear_metrics
)


def metrics_dashboard_page():
    """Metrics Dashboard Page."""
    st.title("📊 Metrics Dashboard")
    st.markdown("Monitor performance and service health across all 4 services.")

    # Mode indicator
    mode = st.session_state.get('service_mode', 'Production')
    if mode == 'Production':
        st.success("📡 Monitoring Production Services")
    else:
        st.info("🧪 Monitoring Mock Services")

    # Overall stats
    st.subheader("🎯 Overall Statistics")

    # Get stats for all services
    text_stats = get_service_stats('text')
    image_stats = get_service_stats('image')
    diagram_stats = get_service_stats('diagram')
    chart_stats = get_service_stats('chart')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Text Service",
                 text_stats['total_calls'],
                 delta=f"{text_stats['success_rate']:.0f}% success")
    with col2:
        st.metric("Image Service",
                 image_stats['total_calls'],
                 delta=f"{image_stats['success_rate']:.0f}% success")
    with col3:
        st.metric("Diagram Service",
                 diagram_stats['total_calls'],
                 delta=f"{diagram_stats['success_rate']:.0f}% success")
    with col4:
        st.metric("Chart Service",
                 chart_stats['total_calls'],
                 delta=f"{chart_stats['success_rate']:.0f}% success")

    # Response time comparison
    st.subheader("⏱️ Average Response Times")

    if any([text_stats['total_calls'], image_stats['total_calls'],
            diagram_stats['total_calls'], chart_stats['total_calls']]):

        # Bar chart of response times
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Text', 'Image', 'Diagram', 'Chart'],
            y=[
                text_stats['avg_response_time'],
                image_stats['avg_response_time'],
                diagram_stats['avg_response_time'],
                chart_stats['avg_response_time']
            ],
            marker_color=['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
        ))

        fig.update_layout(
            title="Average Response Time by Service",
            xaxis_title="Service",
            yaxis_title="Time (seconds)",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No data yet. Run some tests to see metrics!")

    # Individual service metrics
    st.subheader("📈 Service Details")

    tabs = st.tabs(["Text", "Image", "Diagram", "Chart"])

    # Text service tab
    with tabs[0]:
        display_service_metrics('text', 'Text & Table Builder')

    # Image service tab
    with tabs[1]:
        display_service_metrics('image', 'Image Builder')

    # Diagram service tab
    with tabs[2]:
        display_service_metrics('diagram', 'Diagram Generator')

    # Chart service tab
    with tabs[3]:
        display_service_metrics('chart', 'Analytics/Chart')

    # Export and clear
    st.subheader("🔧 Management")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("📥 Export All Metrics"):
            data = export_metrics_to_dict()
            st.download_button(
                label="Download JSON",
                data=str(data),
                file_name=f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    with col2:
        if st.button("🗑️ Clear All Metrics"):
            clear_metrics()
            st.success("Metrics cleared!")
            st.rerun()

    with col3:
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")


def display_service_metrics(service: str, service_name: str):
    """Display detailed metrics for a specific service."""
    stats = get_service_stats(service)

    if stats['total_calls'] == 0:
        st.info(f"No metrics for {service_name} yet.")
        return

    # Summary stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Calls", stats['total_calls'])
    with col2:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
    with col3:
        st.metric("Avg Response", format_response_time(stats['avg_response_time']))

    # Get metrics list
    metrics = st.session_state.metrics.get(service, [])

    if not metrics:
        return

    # Response time chart
    fig = go.Figure()

    timestamps = [m['timestamp'] for m in metrics]
    response_times = [m['response_time'] for m in metrics]
    success = [m['success'] for m in metrics]

    # Color by success/failure
    colors = ['green' if s else 'red' for s in success]

    fig.add_trace(go.Scatter(
        x=timestamps,
        y=response_times,
        mode='lines+markers',
        name='Response Time',
        marker=dict(color=colors, size=8),
        line=dict(color='lightblue', width=2)
    ))

    fig.update_layout(
        title=f"{service_name} Response Times",
        xaxis_title="Time",
        yaxis_title="Response Time (seconds)",
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

    # Recent calls table
    with st.expander("📋 Recent Calls"):
        for i, m in enumerate(reversed(metrics[-10:])):  # Last 10 calls
            status = "✅" if m['success'] else "❌"
            st.text(f"{status} {format_timestamp(m['timestamp'])} - {format_response_time(m['response_time'])}")

    # Clear service metrics
    if st.button(f"Clear {service_name} Metrics", key=f"clear_{service}"):
        clear_metrics(service)
        st.success(f"{service_name} metrics cleared!")
        st.rerun()
