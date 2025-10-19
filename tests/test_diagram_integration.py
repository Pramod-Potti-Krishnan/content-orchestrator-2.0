# -*- coding: utf-8 -*-
"""
Diagram Service Integration Test
=================================

Simple integration test for Diagram Generator v3.0 Railway service.

Tests:
- Service connectivity
- Diagram generation with async job polling
- SVG/Mermaid generation
- URL retrieval from Supabase
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.real_diagram_client import RealDiagramClient


async def test_diagram_generation():
    """Test diagram generation with production service."""

    print("\n" + "="*80)
    print("DIAGRAM SERVICE INTEGRATION TEST")
    print("="*80)

    # Initialize client
    client = RealDiagramClient()

    print("\n✅ Client initialized")
    print(f"   URL: {client.base_url}")
    print(f"   Timeout: {client.timeout}s")
    print(f"   Poll interval: {client.poll_interval}s")

    # Create test request
    request = {
        "content": """
        A simple software development workflow showing:
        - Requirements gathering
        - Design phase
        - Implementation
        - Testing
        - Deployment
        """,
        "diagram_type": "flowchart",
        "theme": {
            "primary_color": "#3B82F6",
            "style": "modern"
        }
    }

    print("\n📤 Sending diagram generation request...")
    print(f"   Content: {request['content'][:60].strip()}...")
    print(f"   Diagram type: {request['diagram_type']}")
    print(f"   Theme: {request['theme']}")

    # Generate diagram
    try:
        result = await client.generate(request)

        print("\n✅ DIAGRAM GENERATION SUCCESSFUL")
        print(f"   URL: {result.url[:80]}...")
        print(f"   Type: {result.type}")
        print(f"   Generation method: {result.metadata.get('generation_method')}")
        print(f"   Generation time: {result.metadata.get('generation_time_ms')}ms")
        print(f"   Quality score: {result.metadata.get('quality_score')}")
        print(f"   Source: {result.metadata.get('source')}")

        # Validate response
        assert result.url, "Diagram URL is missing"
        assert result.url.startswith("http"), "Diagram URL should be a valid HTTP URL"
        assert result.type, "Diagram type is missing"
        assert result.metadata.get('source') == 'diagram_service_v3.0', "Source mismatch"

        print("\n✅ ALL VALIDATIONS PASSED")

    except Exception as e:
        print(f"\n❌ DIAGRAM GENERATION FAILED: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(test_diagram_generation())
    print("\n" + "="*80)
    print("✅ DIAGRAM SERVICE INTEGRATION TEST COMPLETE")
    print("="*80 + "\n")
