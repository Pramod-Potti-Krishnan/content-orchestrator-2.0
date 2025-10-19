"""
Test script for Content Orchestrator v2.0
==========================================

Tests the v2.0 lightweight architecture with mock API clients.
"""

import sys
import asyncio
import time
from pathlib import Path

# Add directories to path for imports
current_dir = Path(__file__).parent
v1_dir = current_dir.parent / "v1.0"

# Add v2 directory first (higher priority)
sys.path.insert(0, str(current_dir))
# Add v1.0 directory for models
sys.path.insert(0, str(v1_dir))

# Import v2 components (will import from v2 directory)
from core.orchestrator import ContentOrchestratorV2
from clients.mock_text_client import MockTextClient
from clients.mock_chart_client import MockChartClient
from clients.mock_image_client import MockImageClient
from clients.mock_diagram_client import MockDiagramClient

# Import models from v1.0 (reused)
from models.agents import PresentationStrawman, Slide


def create_test_presentation(num_slides: int = 3) -> PresentationStrawman:
    """Create a test presentation with multiple slides."""
    slides = []

    for i in range(num_slides):
        slide = Slide(
            slide_number=i,
            slide_id=f"slide_{i:03d}",
            title=f"Slide {i}: Test Title",
            slide_type="data_driven" if i % 2 == 0 else "visual_heavy",
            narrative=f"This is the narrative for slide {i}",
            key_points=[
                "Q3 revenue growth exceeded expectations",
                "EBITDA margin improved significantly",
                "Operating costs reduced through efficiency"
            ],
            analytics_needed="Goal: Show revenue trend, Content: Q3 revenue data, Style: Line chart" if i % 2 == 0 else None,
            visuals_needed="Goal: Executive team photo, Content: Leadership, Style: Professional" if i % 2 == 1 else None,
            diagrams_needed="Goal: Show process flow, Content: Sales workflow, Style: Flowchart" if i == 2 else None,
            tables_needed=None,
            structure_preference="two-column"
        )
        slides.append(slide)

    strawman = PresentationStrawman(
        main_title="Q3 Financial Results",
        overall_theme="Strong quarterly performance with revenue growth",
        target_audience="Board of Directors",
        design_suggestions="Modern professional with clean layout",
        presentation_duration=15,
        slides=slides
    )

    return strawman


async def test_v2_orchestrator(num_slides: int = 3):
    """Test v2.0 orchestrator with specified number of slides."""
    print(f"\n{'='*70}")
    print(f"Testing Content Orchestrator v2.0 with {num_slides} slides")
    print(f"{'='*70}\n")

    # Create mock API clients with minimal delays
    text_client = MockTextClient(delay_ms=100)
    chart_client = MockChartClient(delay_ms=150)
    image_client = MockImageClient(delay_ms=200)
    diagram_client = MockDiagramClient(delay_ms=150)

    print("✅ Created mock API clients")

    # Initialize v2.0 orchestrator
    orchestrator = ContentOrchestratorV2(
        text_client=text_client,
        chart_client=chart_client,
        image_client=image_client,
        diagram_client=diagram_client
    )

    print("✅ Initialized v2.0 orchestrator\n")

    # Create test presentation
    strawman = create_test_presentation(num_slides)
    print(f"✅ Created test presentation with {num_slides} slides\n")

    # Progress callback
    def progress_callback(message, current, total):
        print(f"   [{current}/{total}] {message}")

    # Run orchestration
    print("⚡ Starting v2.0 orchestration...\n")
    start_time = time.time()

    result = await orchestrator.enrich_presentation(
        strawman=strawman,
        progress_callback=progress_callback
    )

    elapsed_time = time.time() - start_time

    print(f"\n✅ v2.0 Orchestration Complete!\n")

    # Display results
    print(f"{'='*70}")
    print("RESULTS")
    print(f"{'='*70}\n")

    print(f"Processing Time: {elapsed_time:.3f}s")
    print(f"Time per Slide: {elapsed_time / num_slides:.3f}s\n")

    print(f"Total Slides: {result.validation_report.total_slides}")
    print(f"Compliant Slides: {result.validation_report.compliant_slides}")
    print(f"Total Violations: {result.validation_report.total_violations}")
    print(f"Critical Violations: {result.validation_report.critical_violations}\n")

    print(f"Successful Items: {result.generation_metadata['successful_items']}")
    print(f"Failed Items: {result.generation_metadata['failed_items']}")
    print(f"Total API Requests: {result.generation_metadata['total_api_requests']}\n")

    print(f"Orchestrator Version: {result.generation_metadata['orchestrator_version']}")
    print(f"Architecture: {result.generation_metadata['architecture']}\n")

    # Performance comparison with v1.0
    v1_estimated_time = num_slides * 11  # v1.0 averages ~11s/slide
    speedup = v1_estimated_time / elapsed_time if elapsed_time > 0 else 0

    print(f"{'='*70}")
    print("PERFORMANCE COMPARISON")
    print(f"{'='*70}\n")

    print(f"v1.0 Estimated Time: {v1_estimated_time:.1f}s (~11s/slide)")
    print(f"v2.0 Actual Time: {elapsed_time:.3f}s")
    print(f"Speedup: {speedup:.1f}x faster! 🚀\n")

    # Show sample enriched slide
    if result.enriched_slides:
        print(f"{'='*70}")
        print("SAMPLE ENRICHED SLIDE")
        print(f"{'='*70}\n")

        sample = result.enriched_slides[0]
        print(f"Slide ID: {sample.slide_id}")
        print(f"Layout ID: {sample.layout_id}")
        print(f"Compliant: {'✅ Yes' if sample.validation_status.compliant else '❌ No'}")
        print(f"\nGenerated Content Fields:")
        for field, value in sample.generated_content.items():
            if value is not None and value != [] and value != {}:
                value_str = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                print(f"  - {field}: {value_str}")

    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    # Test with different slide counts
    test_counts = [1, 3, 10]

    for count in test_counts:
        asyncio.run(test_v2_orchestrator(count))
        print("\n")
