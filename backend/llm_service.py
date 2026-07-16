"""
llm_service.py

Handles all communication with
Large Language Models.
"""

import os

from dotenv import load_dotenv

import google.generativeai as genai

# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DEFAULT_MODEL = os.getenv(
    "DEFAULT_MODEL",
    "gemini-2.5-flash"
)

# =====================================================
# CONFIGURE GEMINI
# =====================================================

if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

genai.configure(
    api_key=GEMINI_API_KEY
)

# =====================================================
# LLM CLASS
# =====================================================

class LLMService:

    """
    Responsible for interacting
    with the selected LLM.
    """

    def __init__(self):

        self.model = genai.GenerativeModel(
            DEFAULT_MODEL
        )

    def generate_response(
        self,
        prompt: str
    ) -> str:

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as error:

            return f"LLM Error: {error}"

    def compress_context(
        self,
        compression_prompt: str
    ) -> str:
        """
        Uses Gemini to compress long inputs.
        """

        try:

            response = self.model.generate_content(
                compression_prompt
            )

            return response.text

        except Exception as error:

            return f"Compression Error: {error}"
# =====================================================
# GLOBAL INSTANCE
# =====================================================

llm = LLMService()