"""
Guidance Parser
===============

Parses guidance strings from the Director in Goal/Content/Style format.

Example input:
"Goal: Show revenue trend over time, Content: Q1-Q4 2024 revenue data, Style: Line chart with growth indicators"

Parsed output:
{
    "goal": "Show revenue trend over time",
    "content": "Q1-Q4 2024 revenue data",
    "style": "Line chart with growth indicators"
}
"""

import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def parse_guidance(guidance_text: Optional[str]) -> Dict[str, str]:
    """
    Parse Director guidance string in Goal/Content/Style format.

    Args:
        guidance_text: String like "Goal: X, Content: Y, Style: Z"

    Returns:
        Dictionary with 'goal', 'content', 'style' keys (empty strings if not found)
    """
    if not guidance_text:
        return {"goal": "", "content": "", "style": ""}

    result = {
        "goal": "",
        "content": "",
        "style": ""
    }

    try:
        # Pattern to match "Key: Value" pairs
        # Handles cases like "Goal: text, Content: text, Style: text"
        pattern = r'(Goal|Content|Style):\s*([^,]+?)(?=(?:,\s*(?:Goal|Content|Style):|$))'

        matches = re.findall(pattern, guidance_text, re.IGNORECASE)

        for key, value in matches:
            key_lower = key.lower()
            result[key_lower] = value.strip()

        logger.debug(f"Parsed guidance: {result}")

    except Exception as e:
        logger.warning(f"Failed to parse guidance '{guidance_text}': {e}")
        # Return empty dict on parse failure
        return {"goal": "", "content": "", "style": ""}

    return result


def extract_goal(guidance_text: Optional[str]) -> str:
    """Extract just the Goal portion of guidance."""
    parsed = parse_guidance(guidance_text)
    return parsed.get("goal", "")


def extract_content(guidance_text: Optional[str]) -> str:
    """Extract just the Content portion of guidance."""
    parsed = parse_guidance(guidance_text)
    return parsed.get("content", "")


def extract_style(guidance_text: Optional[str]) -> str:
    """Extract just the Style portion of guidance."""
    parsed = parse_guidance(guidance_text)
    return parsed.get("style", "")


def has_valid_guidance(guidance_text: Optional[str]) -> bool:
    """
    Check if guidance text has at least one valid component.
    """
    if not guidance_text:
        return False

    parsed = parse_guidance(guidance_text)
    return any(v.strip() for v in parsed.values())
