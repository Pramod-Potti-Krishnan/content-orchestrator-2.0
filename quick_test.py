"""Quick test for v2 orchestrator - bypasses path issues"""
import sys
import asyncio
from pathlib import Path
import importlib.util

# Get paths
v2_dir = Path(__file__).parent
v1_dir = v2_dir.parent / "v1.0"

# Add BOTH v2 and v1.0 to path
sys.path.insert(0, str(v2_dir))  # v2 first for services
sys.path.insert(0, str(v1_dir))  # v1.0 for models

# Direct import using importlib
def import_from_file(name, filepath):
    spec = importlib.util.spec_from_file_location(name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import v2 orchestrator directly
orch_mod = import_from_file("v2_orchestrator", v2_dir / "core" / "orchestrator.py")
text_mod = import_from_file("v2_text_client", v2_dir / "clients" / "mock_text_client.py")
chart_mod = import_from_file("v2_chart_client", v2_dir / "clients" / "mock_chart_client.py")
image_mod = import_from_file("v2_image_client", v2_dir / "clients" / "mock_image_client.py")
diagram_mod = import_from_file("v2_diagram_client", v2_dir / "clients" / "mock_diagram_client.py")

ContentOrchestratorV2 = orch_mod.ContentOrchestratorV2
MockTextClient = text_mod.MockTextClient
MockChartClient = chart_mod.MockChartClient
MockImageClient = image_mod.MockImageClient
MockDiagramClient = diagram_mod.MockDiagramClient

# Import models
from models.agents import PresentationStrawman, Slide


async def quick_test():
    print("="*70)
    print("QUICK TEST - Content Orchestrator v2.0")
    print("="*70 + "\n")

    # Create clients
    text_client = MockTextClient(delay_ms=100)
    chart_client = MockChartClient(delay_ms=100)
    image_client = MockImageClient(delay_ms=100)
    diagram_client = MockDiagramClient(delay_ms=100)

    print("✅ Created mock API clients")

    # Create orchestrator
    orchestrator = ContentOrchestratorV2(
        text_client=text_client,
        chart_client=chart_client,
        image_client=image_client,
        diagram_client=diagram_client
    )

    print("✅ Initialized v2.0 orchestrator\n")

    # Create simple test slide
    slide = Slide(
        slide_number=0,
        slide_id="slide_000",
        title="Q3 Revenue Performance",
        slide_type="data_driven",
        narrative="Strong revenue growth in Q3",
        key_points=["Q3 revenue growth", "EBITDA margin improvement", "Cost reduction"],
        analytics_needed="Goal: Show trend, Content: Revenue data, Style: Line chart",
        visuals_needed=None,
        diagrams_needed=None,
        tables_needed=None,
        structure_preference="two-column"
    )

    strawman = PresentationStrawman(
        main_title="Q3 Results",
        overall_theme="Financial performance",
        target_audience="Board",
        design_suggestions="Modern",
        presentation_duration=10,
        slides=[slide]
    )

    print("✅ Created test presentation\n")
    print("⚡ Running v2.0 orchestration...\n")

    import time
    start = time.time()

    result = await orchestrator.enrich_presentation(strawman)

    elapsed = time.time() - start

    print(f"\n✅ Complete in {elapsed:.3f}s\n")
    print("="*70)
    print("RESULTS")
    print("="*70)
    print(f"Slides: {result.validation_report.total_slides}")
    print(f"Compliant: {result.validation_report.compliant_slides}")
    print(f"Successful items: {result.generation_metadata['successful_items']}")
    print(f"Version: {result.generation_metadata['orchestrator_version']}")
    print(f"Architecture: {result.generation_metadata['architecture']}")
    print(f"\nv1.0 would take: ~11s")
    print(f"v2.0 took: {elapsed:.3f}s")
    print(f"Speedup: {11/elapsed:.1f}x faster! 🚀")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(quick_test())
