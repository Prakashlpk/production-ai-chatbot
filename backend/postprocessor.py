
"""
postprocessor.py

Responsible for formatting and cleaning
LLM responses before displaying them.
"""

import re


# ==========================================================
# CLEAN RESPONSE
# ==========================================================

def clean_response(response: str) -> str:
    """
    Remove unnecessary spaces
    and blank lines.
    """

    response = response.strip()

    response = re.sub(r"\n{3,}", "\n\n", response)

    return response


# ==========================================================
# FORMAT RESPONSE
# ==========================================================

def format_response(response: str) -> str:
    """
    Future formatting.

    Version 1:
    Returns original response.
    """

    return response


# ==========================================================
# MAIN POSTPROCESSOR
# ==========================================================

def postprocess_response(response: str) -> str:
    """
    Complete response pipeline.
    """

    response = clean_response(response)

    response = format_response(response)

    return response