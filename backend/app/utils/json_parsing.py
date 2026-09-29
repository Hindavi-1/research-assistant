"""Robust-ish JSON extraction from LLM text output (handles stray markdown fences)."""
import json
import re

from app.core.logging import logger


def extract_json_array(text: str) -> list[dict]:
    """Extract a JSON array from LLM output, tolerating ```json fences or leading/trailing prose."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict):
            return [parsed]
    except json.JSONDecodeError:
        pass

    # Fallback: find the first '[' ... last ']' span and try again.
    start, end = cleaned.find("["), cleaned.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON array from LLM output: {cleaned[:300]}")

    return []
