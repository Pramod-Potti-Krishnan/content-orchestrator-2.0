# -*- coding: utf-8 -*-
"""
Simple Integration Test for Text Service
==========================================

Tests RealTextClient integration with Text & Table Builder v1.0 Railway service.

Run with: python tests/test_text_integration.py
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from clients.real_text_client import RealTextClient


async def test_text_generation():
    """Test text generation with production service."""
    print("=" * 80)
    print("TEXT SERVICE INTEGRATION TEST")
    print("=" * 80)
    print()

    # Initialize client
    client = RealTextClient()
    print(f" Client initialized")
    print(f"   URL: {client.base_url}")
    print(f"   Timeout: {client.timeout}s")
    print()

    # Prepare test request
    request = {
        "slide_id": "test_slide_1",
        "slide_number": 1,
        "topics": ["AI Innovation", "Future of Technology"],
        "narrative": "Discuss emerging AI trends and their impact on business",
        "presentation_id": "test_pres_001",
        "context": {
            "presentation_context": "Tech conference keynote",
            "slide_context": "Introduction slide",
            "previous_slides": []
        },
        "constraints": {
            "word_count": 100,
            "tone": "professional",
            "format": "paragraph"
        }
    }

    print("=� Sending request to Text service...")
    print(f"   Topics: {request['topics']}")
    print(f"   Word count limit: {request['constraints']['word_count']}")
    print()

    try:
        # Generate text
        result = await client.generate(request)

        # Validate result
        assert hasattr(result, 'content'), "Result missing 'content' attribute"
        assert hasattr(result, 'metadata'), "Result missing 'metadata' attribute"
        assert isinstance(result.content, str), "Content should be string"
        assert len(result.content) > 0, "Content should not be empty"

        # Display results
        print("=" * 80)
        print(" TEXT GENERATION SUCCESSFUL")
        print("=" * 80)
        print()
        print(f"=� Metadata:")
        print(f"   Word count: {result.metadata.get('word_count', 'N/A')}")
        print(f"   Generation time: {result.metadata.get('generation_time_ms', 'N/A')}ms")
        print(f"   Model used: {result.metadata.get('model_used', 'N/A')}")
        print(f"   Session ID: {result.metadata.get('session_id', 'N/A')}")
        print()
        print(f"=� Generated Content:")
        print("-" * 80)
        print(result.content)
        print("-" * 80)
        print()
        print("=" * 80)
        print(" ALL TESTS PASSED")
        print("=" * 80)

        return True

    except Exception as e:
        print("=" * 80)
        print("L TEST FAILED")
        print("=" * 80)
        print(f"Error: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        print()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_text_generation())
    sys.exit(0 if success else 1)
