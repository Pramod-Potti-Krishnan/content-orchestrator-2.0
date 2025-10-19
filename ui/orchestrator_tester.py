# -*- coding: utf-8 -*-
"""
Full Orchestrator Testing Component
====================================

Streamlit component for testing the complete presentation enrichment workflow.
"""

import asyncio
import time
import streamlit as st
from typing import Dict, Any

from core.orchestrator import ContentOrchestratorV2
from models.agents import PresentationStrawman, Slide
from ui.utils import (
    get_clients,
    record_metric,
    format_response_time,
    display_error
)


def create_test_presentation(num_slides: int) -> PresentationStrawman:
    """Create a test presentation with specified number of slides."""
    slides = []

    for i in range(num_slides):
        slide = Slide(
            slide_number=i,
            slide_id=f"slide_{i:03d}",
            title=f"Slide {i+1}: Test Slide",
            slide_type="data_driven" if i % 2 == 0 else "visual_heavy",
            narrative=f"Narrative for slide {i+1}",
            key_points=[
                "Revenue growth exceeded targets",
                "Market share expansion",
                "Operational efficiency gains"
            ],
            analytics_needed="Goal: Show Q3 trend, Content: Revenue data, Style: Line chart" if i % 2 == 0 else None,
            visuals_needed="Goal: Team photo, Content: Leadership team, Style: Professional" if i % 2 == 1 else None,
            diagrams_needed="Goal: Process flow, Content: Sales workflow, Style: Flowchart" if i == 0 else None,
            tables_needed=None,
            structure_preference="two-column"
        )
        slides.append(slide)

    return PresentationStrawman(
        main_title="Test Presentation",
        overall_theme="Business performance",
        target_audience="Executives",
        design_suggestions="Modern professional",
        presentation_duration=num_slides * 2,
        slides=slides
    )


def orchestrator_testing_page():
    """Full Orchestrator Testing Page."""
    st.title("🎯 Full Orchestrator Testing")
    st.markdown("Test the complete presentation enrichment workflow with all 4 services working together.")

    # Get service mode
    mode = st.session_state.get('service_mode', 'Production')

    # Configuration
    st.subheader("Test Configuration")

    col1, col2 = st.columns(2)
    with col1:
        num_slides = st.slider("Number of Slides", min_value=1, max_value=10, value=3)
    with col2:
        st.info(f"**Service Mode**: {mode}")

    # Service info
    with st.expander("ℹ️ About This Test"):
        st.markdown(f"""
        This test will:
        1. Create a test presentation with **{num_slides} slides**
        2. Run the complete enrichment workflow
        3. Generate content using all 4 services:
           - Text & Table Builder
           - Image Builder
           - Diagram Generator
           - Analytics/Chart Service
        4. Validate and report results

        **Estimated Time**: ~{num_slides * 5}-{num_slides * 10}s ({mode} mode)
        """)

    # Run test button
    if st.button("🚀 Run Full Enrichment Test", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Get clients
            clients = get_clients(mode)

            # Create orchestrator
            orchestrator = ContentOrchestratorV2(
                text_client=clients['text'],
                chart_client=clients['chart'],
                image_client=clients['image'],
                diagram_client=clients['diagram']
            )

            status_text.text("Creating test presentation...")

            # Create test presentation
            strawman = create_test_presentation(num_slides)

            status_text.text("Running enrichment workflow...")
            progress_bar.progress(20)

            # Progress callback
            progress_updates = []

            def progress_callback(message, current, total):
                progress_updates.append(f"[{current}/{total}] {message}")
                progress = int((current / total) * 80) + 20  # 20-100%
                progress_bar.progress(min(progress, 100))
                status_text.text(f"{message} ({current}/{total})")

            # Run enrichment
            start_time = time.time()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                orchestrator.enrich_presentation(
                    strawman=strawman,
                    progress_callback=progress_callback
                )
            )
            loop.close()

            elapsed = time.time() - start_time

            progress_bar.progress(100)
            status_text.text("✅ Enrichment complete!")

            # Record overall metric
            record_metric('orchestrator', elapsed, True, {
                'num_slides': num_slides,
                'compliant_slides': result.validation_report.compliant_slides,
                'total_violations': result.validation_report.total_violations
            })

            # Display results
            st.success(f"🎉 Enrichment Complete in {format_response_time(elapsed)}")

            # Summary metrics
            st.subheader("📊 Summary")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Time", format_response_time(elapsed))
            with col2:
                st.metric("Time/Slide", format_response_time(elapsed / num_slides))
            with col3:
                st.metric("Compliant Slides",
                         f"{result.validation_report.compliant_slides}/{result.validation_report.total_slides}")
            with col4:
                st.metric("Success Rate",
                         f"{(result.validation_report.compliant_slides / result.validation_report.total_slides * 100):.0f}%")

            # Generation metadata
            with st.expander("📋 Generation Metadata"):
                st.json({
                    'orchestrator_version': result.generation_metadata['orchestrator_version'],
                    'architecture': result.generation_metadata['architecture'],
                    'successful_items': result.generation_metadata['successful_items'],
                    'failed_items': result.generation_metadata['failed_items'],
                    'total_api_requests': result.generation_metadata['total_api_requests']
                })

            # Validation report
            with st.expander("✅ Validation Report"):
                st.json({
                    'total_slides': result.validation_report.total_slides,
                    'compliant_slides': result.validation_report.compliant_slides,
                    'total_violations': result.validation_report.total_violations,
                    'critical_violations': result.validation_report.critical_violations
                })

            # Progress log
            with st.expander("📝 Progress Log"):
                for update in progress_updates:
                    st.text(update)

            # Enriched slides
            st.subheader(f"📄 Enriched Slides ({len(result.enriched_slides)})")

            for slide in result.enriched_slides:
                with st.expander(f"Slide {slide.original_slide.slide_number + 1}: {slide.slide_id}"):
                    col1, col2 = st.columns([2, 1])

                    with col1:
                        st.markdown(f"**Layout**: {slide.layout_id}")
                        compliant = "✅ Compliant" if slide.validation_status.compliant else "❌ Not Compliant"
                        st.markdown(f"**Status**: {compliant}")

                    with col2:
                        if slide.validation_status.violations:
                            st.warning(f"⚠️ {len(slide.validation_status.violations)} violations")

                    # Generated content
                    if slide.generated_content:
                        st.markdown("**Generated Content:**")
                        for key, value in slide.generated_content.items():
                            if value and value != [] and value != {}:
                                st.markdown(f"- **{key}**: {str(value)[:100]}...")

            # Performance comparison
            st.subheader("⚡ Performance Comparison")
            v1_time = num_slides * 11  # v1.0 averaged ~11s/slide
            speedup = v1_time / elapsed if elapsed > 0 else 0

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("v1.0 Estimated", f"{v1_time:.1f}s", delta=None)
            with col2:
                st.metric("v2.0 Actual", format_response_time(elapsed), delta=None)
            with col3:
                st.metric("Speedup", f"{speedup:.1f}x faster", delta=f"+{((speedup-1)*100):.0f}%")

        except Exception as e:
            record_metric('orchestrator', time.time() - start_time, False)
            status_text.text("❌ Enrichment failed")
            progress_bar.empty()
            display_error(e, "Orchestrator")
