"""
preprocessor.py

Responsible for preparing user input before it is sent to the LLM.
"""


import re

import tiktoken

from spellchecker import SpellChecker

SUMMARIZATION_THRESHOLD = 1000

MAX_INPUT_TOKENS = 8000

# ==========================================================
# INITIALIZE
# ==========================================================

spell = SpellChecker()

encoding = tiktoken.get_encoding("cl100k_base")


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text: str) -> str:
    """
    Remove extra spaces.
    """

    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    return text


# ==========================================================
# SPELL CORRECTION
# ==========================================================

def correct_spelling(text: str) -> str:
    """
    Correct spelling mistakes.
    """

    corrected_words = []

    for word in text.split():

        corrected_words.append(

            spell.correction(word) or word

        )

    return " ".join(corrected_words)


# ==========================================================
# TOKEN COUNT
# ==========================================================

def count_tokens(text: str) -> int:
    """
    Count the number of tokens.
    """

    return len(

        encoding.encode(text)

    )


# ==========================================================
# SUMMARIZATION PLACEHOLDER
# ==========================================================

def summarize_if_needed(
    text: str,
    max_tokens: int = 1000
) -> str:
    """
    Summarize long prompts.

    Version 1:
    Returns original text.

    Later:
    Calls LLM summarizer.
    """

    tokens = count_tokens(text)

    if tokens <= max_tokens:

        return text

    return text


# ==========================================================
# MAIN PREPROCESSOR
# ==========================================================
MAX_INPUT_TOKENS = 1000

def preprocess_input(text: str) -> dict:
    """
    Complete preprocessing pipeline.
    """

    # Clean text
    text = clean_text(text)

    # Spell correction
    # text = correct_spelling(text)

    # Count tokens
    token_count = count_tokens(text)

    print(f"Token Count: {token_count}")

    # Reject extremely large input
    if token_count > MAX_INPUT_TOKENS:

        raise ValueError(
            "Your input is too large to process directly. "
            "Please upload it as a PDF, DOCX, or TXT file."
        )

    return {

        "text": text,

        "token_count": token_count,

        "needs_context_compression":
            token_count > SUMMARIZATION_THRESHOLD
    }