"""
context_compressor.py

Compresses long user inputs before sending them
to the main LLM.
"""

from backend.llm_service import llm


# ==========================================================
# BUILD COMPRESSION PROMPT
# ==========================================================

def build_compression_prompt(text: str) -> str:
    """
    Build a prompt for Gemini to summarize the input,
    identify the user's intent, and retain only the
    information needed to answer the question.
    """

    prompt = f"""
You are an AI Context Compression Assistant.

IMPORTANT:
Do NOT answer the user's question.

Instead perform ONLY these tasks:

1. Identify the user's actual question.
2. Identify the user's intent.
3. Remove unnecessary details.
4. Preserve:
   - important names
   - dates
   - numbers
   - technical terms
5. Keep only information required for answering.
6. Return a concise version of the input.

User Input:

{text}
"""

    return prompt


# ==========================================================
# COMPRESS CONTEXT
# ==========================================================

def compress_context(text: str) -> str:
    """
    Compress long user input before
    sending it to the main LLM.
    """

    compression_prompt = build_compression_prompt(text)

    compressed_text = llm.compress_context(
        compression_prompt
    )

    return compressed_text