# -*- coding: utf-8 -*-
"""
Individual Service Testing Components
======================================

Streamlit components for testing each production service individually.
"""

import asyncio
import time
import streamlit as st
from typing import Dict, Any

from ui.utils import (
    get_clients,
    record_metric,
    format_response_time,
    display_error
)


def text_service_page():
    """Text & Table Builder Service Testing Page."""
    st.title("📝 Text & Table Builder Service")
    st.markdown("Test the Text & Table Builder v1.0 service with custom inputs.")

    # Get service mode and client
    mode = st.session_state.get('service_mode', 'Production')
    clients = get_clients(mode)
    text_client = clients['text']

    # Service info
    with st.expander("ℹ️ Service Information"):
        st.markdown(f"""
        **Service URL**: `{text_client.base_url}`
        **Model**: Gemini 2.5-flash
        **Timeout**: {text_client.timeout}s
        **Mode**: {mode}
        """)

    # Input fields
    st.subheader("Input Parameters")

    topics = st.text_area(
        "Topics",
        value="Q3 financial performance, Revenue growth, Market expansion",
        help="Comma-separated list of topics"
    )

    narrative = st.text_area(
        "Narrative",
        value="Strong quarterly performance with significant revenue growth driven by new market expansion and operational efficiency improvements.",
        height=100
    )

    context = st.text_area(
        "Context",
        value="Board presentation, Executive summary slide",
        help="Additional context for generation"
    )

    # Generate button
    if st.button("🚀 Generate Text", type="primary"):
        with st.spinner("Generating text..."):
            try:
                # Prepare request
                # Convert comma-separated topics to list
                topics_list = [t.strip() for t in topics.split(',') if t.strip()]

                request = {
                    "topics": topics_list,
                    "narrative": narrative,
                    "context": {
                        "presentation_context": context,
                        "slide_context": "Test slide",
                        "previous_slides": []
                    },
                    "constraints": {},
                    "slide_id": "test_slide_001"
                }

                # Time the request
                start_time = time.time()

                # Run async call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(text_client.generate(request))
                loop.close()

                elapsed = time.time() - start_time

                # Record metric
                record_metric('text', elapsed, True, {
                    'model': result.metadata.get('model_used'),
                    'word_count': len(result.content.split()) if result.content else 0
                })

                # Display results
                st.success(f"✅ Text Generated in {format_response_time(elapsed)}")

                # Content
                st.subheader("Generated Content")
                st.markdown(result.content, unsafe_allow_html=True)

                # Metadata
                with st.expander("📊 Metadata"):
                    st.json({
                        'generation_time': result.metadata.get('generation_time_ms'),
                        'model_used': result.metadata.get('model_used'),
                        'word_count': len(result.content.split()) if result.content else 0,
                        'session_id': result.metadata.get('session_id'),
                        'source': result.metadata.get('source')
                    })

            except Exception as e:
                record_metric('text', time.time() - start_time, False)
                display_error(e, "Text")


def image_service_page():
    """Image Builder Service Testing Page."""
    st.title("🎨 Image Builder Service")
    st.markdown("Test the Image Builder v2.0 service with custom prompts.")

    # Get service mode and client
    mode = st.session_state.get('service_mode', 'Production')
    clients = get_clients(mode)
    image_client = clients['image']

    # Service info
    with st.expander("ℹ️ Service Information"):
        st.markdown(f"""
        **Service URL**: `{image_client.base_url}/api/v2`
        **Model**: Imagen 3.0 Fast
        **Timeout**: {image_client.timeout}s
        **Mode**: {mode}
        """)

    # Input fields
    st.subheader("Input Parameters")

    prompt = st.text_area(
        "Image Prompt",
        value="A modern minimalist spot illustration of a rocket launching into space with vibrant colors and clean lines",
        height=100
    )

    col1, col2 = st.columns(2)
    with col1:
        aspect_ratio = st.selectbox(
            "Aspect Ratio",
            ["16:9", "4:3", "1:1", "9:16", "21:9"],
            index=0
        )
    with col2:
        style = st.selectbox(
            "Style/Archetype",
            ["spot_illustration", "photograph", "vector_art", "3d_render"],
            index=0
        )

    # Generate button
    if st.button("🚀 Generate Image", type="primary"):
        with st.spinner("Generating image..."):
            try:
                # Prepare request
                request = {
                    "goal": prompt,
                    "content": prompt,
                    "style": style,
                    "dimensions": {
                        "aspect_ratio": aspect_ratio
                    }
                }

                # Time the request
                start_time = time.time()

                # Run async call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(image_client.generate(request))
                loop.close()

                elapsed = time.time() - start_time

                # Record metric
                record_metric('image', elapsed, True, {
                    'model': result.metadata.get('model'),
                    'aspect_ratio': result.metadata.get('aspect_ratio')
                })

                # Display results
                st.success(f"✅ Image Generated in {format_response_time(elapsed)}")

                # Image
                st.subheader("Generated Image")
                if result.url:
                    st.image(result.url, caption=result.caption, use_container_width=True)
                else:
                    st.warning("No image URL returned")

                # Metadata
                with st.expander("📊 Metadata"):
                    st.json({
                        'generation_time': result.metadata.get('generation_time_ms'),
                        'model': result.metadata.get('model'),
                        'aspect_ratio': result.metadata.get('aspect_ratio'),
                        'image_id': result.metadata.get('image_id'),
                        'all_urls': result.metadata.get('all_urls'),
                        'source': result.metadata.get('source')
                    })

            except Exception as e:
                record_metric('image', time.time() - start_time, False)
                display_error(e, "Image")


def diagram_service_page():
    """Diagram Generator Service Testing Page."""
    st.title("📊 Diagram Generator Service")
    st.markdown("Test the Diagram Generator v3.0 service with custom content.")

    # Get service mode and client
    mode = st.session_state.get('service_mode', 'Production')
    clients = get_clients(mode)
    diagram_client = clients['diagram']

    # Service info
    with st.expander("ℹ️ Service Information"):
        st.markdown(f"""
        **Service URL**: `{diagram_client.base_url}`
        **Status**: ✅ Operational
        **Methods**: 21 SVG Templates, 7 Mermaid types, 6 Python charts
        **Generation Speed**: <2s for SVG, <500ms for Mermaid
        **Timeout**: {diagram_client.timeout}s
        **Poll Interval**: {diagram_client.poll_interval}s
        **Mode**: {mode}

        **Recent Fixes**: Diagram generation fully operational. SVG content validated (3943 bytes typical).
        """)

    # Input fields
    st.subheader("Input Parameters")

    content = st.text_area(
        "Diagram Content",
        value="""Software Development Process:
1. Requirements Gathering
2. Design & Architecture
3. Implementation
4. Testing & QA
5. Deployment
6. Maintenance""",
        height=150
    )

    diagram_type = st.selectbox(
        "Diagram Type",
        [
            "flowchart",
            "cycle_3_step",
            "cycle_4_step",
            "pyramid_3_level",
            "venn_2_circle",
            "timeline",
            "funnel",
            "sequence",
            "state"
        ]
    )

    col1, col2 = st.columns(2)
    with col1:
        primary_color = st.color_picker("Primary Color", "#3B82F6")
    with col2:
        style = st.selectbox("Style", ["modern", "professional", "minimal"])

    # Generate button
    if st.button("🚀 Generate Diagram", type="primary"):
        with st.spinner("Generating diagram..."):
            try:
                # Prepare request
                request = {
                    "content": content,
                    "diagram_type": diagram_type,
                    "theme": {
                        "primary_color": primary_color,
                        "style": style
                    }
                }

                # Time the request
                start_time = time.time()

                # Run async call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(diagram_client.generate(request))
                loop.close()

                elapsed = time.time() - start_time

                # Record metric
                record_metric('diagram', elapsed, True, {
                    'diagram_type': result.type,
                    'method': result.metadata.get('generation_method')
                })

                # Display results
                st.success(f"✅ Diagram Generated in {format_response_time(elapsed)}")

                # Diagram
                st.subheader("Generated Diagram")
                if result.url:
                    # Display SVG diagram
                    st.image(result.url, caption=f"{result.type} diagram", use_container_width=True)

                    # Show URL and download link
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.caption(f"🔗 URL: {result.url}")
                    with col2:
                        st.link_button("Open in New Tab", result.url, type="secondary")
                else:
                    st.warning("No diagram URL returned")

                # Metadata
                with st.expander("📊 Metadata"):
                    st.json({
                        'diagram_type': result.type,
                        'generation_method': result.metadata.get('generation_method'),
                        'generation_time': result.metadata.get('generation_time_ms'),
                        'dimensions': result.metadata.get('dimensions'),
                        'source': result.metadata.get('source')
                    })

            except Exception as e:
                record_metric('diagram', time.time() - start_time, False)
                display_error(e, "Diagram")


def chart_service_page():
    """Analytics/Chart Service Testing Page."""
    st.title("📈 Analytics/Chart Service")
    st.markdown("Test the Analytics Microservice v3 with LLM-enhanced data synthesis.")

    # Get service mode and client
    mode = st.session_state.get('service_mode', 'Production')
    clients = get_clients(mode)
    chart_client = clients['chart']

    # Service info
    with st.expander("ℹ️ Service Information"):
        st.markdown(f"""
        **Service URL**: `{chart_client.base_url}`
        **LLM**: OpenAI GPT-4o-mini
        **Chart Types**: 20+ types
        **Timeout**: {chart_client.timeout}s
        **Poll Interval**: {chart_client.poll_interval}s
        **Mode**: {mode}
        """)

    # Input fields
    st.subheader("Input Parameters")

    content = st.text_area(
        "Chart Content/Data Description",
        value="Show quarterly revenue growth for 2024: Q1=$25k, Q2=$35k, Q3=$30k, Q4=$40k",
        height=100
    )

    title = st.text_input("Chart Title", value="2024 Quarterly Revenue Growth")

    chart_type = st.selectbox(
        "Chart Type",
        [
            "bar_vertical",
            "bar_horizontal",
            "line",
            "pie",
            "donut",
            "area",
            "scatter",
            "heatmap",
            "radar"
        ]
    )

    theme = st.selectbox(
        "Theme",
        ["professional", "default", "dark", "colorful", "minimal"]
    )

    # Generate button
    if st.button("🚀 Generate Chart", type="primary"):
        with st.spinner("Generating chart..."):
            try:
                # Prepare request
                request = {
                    "content": content,
                    "title": title,
                    "chart_type": chart_type,
                    "theme": theme,
                    "data": None  # Let LLM synthesize
                }

                # Time the request
                start_time = time.time()

                # Run async call
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(chart_client.generate(request))
                loop.close()

                elapsed = time.time() - start_time

                # Record metric
                record_metric('chart', elapsed, True, {
                    'chart_type': result.type,
                    'data_points': result.metadata.get('data_points')
                })

                # Display results
                st.success(f"✅ Chart Generated in {format_response_time(elapsed)}")

                # Chart
                st.subheader("Generated Chart")
                if result.url:
                    st.image(result.url, caption=title, use_container_width=True)
                    st.caption(f"URL: {result.url}")
                else:
                    st.warning("No chart URL returned")

                # Chart Data
                if result.data:
                    with st.expander("📊 Chart Data"):
                        st.json(result.data)

                # Metadata
                with st.expander("📋 Metadata"):
                    st.json({
                        'chart_type': result.type,
                        'theme': result.metadata.get('theme'),
                        'data_points': result.metadata.get('data_points'),
                        'generated_at': result.metadata.get('generated_at'),
                        'source': result.metadata.get('source')
                    })

            except Exception as e:
                record_metric('chart', time.time() - start_time, False)
                display_error(e, "Chart")
