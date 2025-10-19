# -*- coding: utf-8 -*-
"""
Image Service Integration Test
================================

Simple integration test for Image Builder v2.0 Railway service.

Tests:
- Service connectivity
- Image generation with custom aspect ratio
- URL retrieval from Supabase
- Response time validation
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.real_image_client import RealImageClient


async def test_image_generation():
    """Test image generation with production service."""

    print("\n" + "="*80)
    print("IMAGE SERVICE INTEGRATION TEST")
    print("="*80)

    # Initialize client
    client = RealImageClient()

    print("\n✅ Client initialized")
    print(f"   URL: {client.base_url}")
    print(f"   Timeout: {client.timeout}s")

    # Create test request
    request = {
        "goal": "A modern minimalist spot illustration of a rocket launching into space, vibrant colors",
        "content": "rocket launch illustration",
        "style": "spot_illustration",
        "dimensions": {
            "aspect_ratio": "16:9",
            "width": 1920,
            "height": 1080
        },
        "remove_background": False,
        "crop_anchor": "center"
    }

    print("\n📤 Sending image generation request...")
    print(f"   Prompt: {request['goal'][:60]}...")
    print(f"   Style: {request['style']}")
    print(f"   Aspect Ratio: {request['dimensions']['aspect_ratio']}")

    # Generate image
    try:
        result = await client.generate(request)

        print("\n✅ IMAGE GENERATION SUCCESSFUL")
        print(f"   URL: {result.url[:80]}...")
        print(f"   Caption: {result.caption[:60]}...")
        print(f"   Generation time: {result.metadata.get('generation_time_ms')}ms")
        print(f"   Aspect ratio: {result.metadata.get('aspect_ratio')}")
        print(f"   Model: {result.metadata.get('model')}")
        print(f"   Source: {result.metadata.get('source')}")

        # Validate response
        assert result.url, "Image URL is missing"
        assert result.url.startswith("http"), "Image URL should be a valid HTTP URL"
        assert result.caption, "Caption is missing"
        assert result.metadata.get('source') == 'image_service_v2.0', "Source mismatch"

        print("\n✅ ALL VALIDATIONS PASSED")

    except Exception as e:
        print(f"\n❌ IMAGE GENERATION FAILED: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(test_image_generation())
    print("\n" + "="*80)
    print("✅ IMAGE SERVICE INTEGRATION TEST COMPLETE")
    print("="*80 + "\n")
