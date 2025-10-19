# -*- coding: utf-8 -*-
"""
Chart/Analytics Service Integration Test
==========================================

Simple integration test for Analytics Microservice v3 Railway service.

Tests:
- Service connectivity
- Chart generation with async job polling
- LLM-enhanced data synthesis
- URL retrieval from Supabase
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.real_chart_client import RealChartClient


async def test_chart_generation():
    """Test chart generation with production service."""

    print("\n" + "="*80)
    print("CHART/ANALYTICS SERVICE INTEGRATION TEST")
    print("="*80)

    # Initialize client
    client = RealChartClient()

    print("\n✅ Client initialized")
    print(f"   URL: {client.base_url}")
    print(f"   Timeout: {client.timeout}s")
    print(f"   Poll interval: {client.poll_interval}s")

    # Create test request
    request = {
        "content": "Show quarterly revenue growth for 2024: Q1=$25k, Q2=$35k, Q3=$30k, Q4=$40k",
        "title": "2024 Quarterly Revenue",
        "chart_type": "bar_vertical",  # Use valid chart type
        "data": None,  # Let LLM synthesize from content
        "theme": {
            "primary_color": "#3B82F6",
            "background_color": "#FFFFFF"
        }
    }

    print("\n📤 Sending chart generation request...")
    print(f"   Content: {request['content'][:60]}...")
    print(f"   Title: {request['title']}")
    print(f"   Chart type: {request['chart_type']}")
    print(f"   Theme: {request['theme']}")

    # Generate chart
    try:
        result = await client.generate(request)

        print("\n✅ CHART GENERATION SUCCESSFUL")
        print(f"   URL: {result.url[:80]}...")
        print(f"   Type: {result.type}")
        print(f"   Data points: {result.metadata.get('data_points')}")
        print(f"   Theme: {result.metadata.get('theme')}")
        print(f"   Generated at: {result.metadata.get('generated_at')}")
        print(f"   Source: {result.metadata.get('source')}")

        # Print chart data if available
        if result.data:
            print(f"   Chart data: {len(result.data)} keys")

        # Validate response
        assert result.url, "Chart URL is missing"
        assert result.url.startswith("http"), "Chart URL should be a valid HTTP URL"
        assert result.type, "Chart type is missing"
        assert result.metadata.get('source') == 'analytics_service_v3', "Source mismatch"

        print("\n✅ ALL VALIDATIONS PASSED")

    except Exception as e:
        print(f"\n❌ CHART GENERATION FAILED: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(test_chart_generation())
    print("\n" + "="*80)
    print("✅ CHART/ANALYTICS SERVICE INTEGRATION TEST COMPLETE")
    print("="*80 + "\n")
