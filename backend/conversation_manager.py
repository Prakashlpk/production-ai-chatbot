"""
conversation_manager.py

This module coordinates the complete chatbot workflow.
It acts as the orchestrator between the UI and backend services.
"""

# ==========================================================
# IMPORTS
# ==========================================================

# These modules will be implemented one by one.

from backend.preprocessor import preprocess_input
from backend.guardrails import validate_input
from backend.prompt_builder import build_prompt
from backend.llm_service import llm
# from backend.memory_service import save_chat, load_chat
from backend.postprocessor import postprocess_response
from backend.context_compressor import compress_context
from backend.memory_service import memory
from database.postgres_service import postgres
# ==========================================================
# MAIN FUNCTION
# ==========================================================

def process_request(
    user_input: str,
    document_text: str = ""
) -> dict:
    """
    Main workflow for processing a user request.

    Parameters
    ----------
    user_input : str
        User message from the UI.

    Returns
    -------
    str
        AI response.
    """

    # ------------------------------------------------------
    # STEP 1
    # Preprocess
    # ------------------------------------------------------

    # ------------------------------------------------------
# STEP 1
# Preprocess
# ------------------------------------------------------

    try:

        processed_data = preprocess_input(user_input)

    except ValueError as error:

        return str(error)

# Extract values from the dictionary

    processed_input = processed_data["text"]

    token_count = processed_data["token_count"]

    needs_context_compression = processed_data[
    "needs_context_compression"
]

# Temporary debugging

    print(f"Token Count: {token_count}")

    print(
    f"Needs Context Compression: {needs_context_compression}"
)
    
# ------------------------------------------------------
# STEP 1A
# Context Compression
# ------------------------------------------------------

    if needs_context_compression:

        print("Compressing long input...")

        processed_input = compress_context(
        processed_input
    )
    # ------------------------------------------------------
    # STEP 2
    # Guardrails
    # ------------------------------------------------------

    # is_safe = validate_input(processed_input)

    is_safe, message = validate_input(processed_input)

    if not is_safe:

        return message
    # ------------------------------------------------------
    # STEP 3
    # Load conversation history
    # ------------------------------------------------------

    # history = load_chat()

    history = memory.load_chat()

    # ------------------------------------------------------
    # STEP 4
    # Build prompt
    # ------------------------------------------------------

    # ------------------------------------------------------
# STEP 4
# Build prompt
# ------------------------------------------------------

    prompt = build_prompt(
        history,
        processed_input
    )

    # Add uploaded document context if available
    if document_text:

        prompt += f"""

    ==========================
    UPLOADED DOCUMENT
    ==========================

    {document_text}

    ==========================
    INSTRUCTION
    ==========================

    Answer the user's question using the uploaded document whenever relevant.
"""
    # ------------------------------------------------------
    # STEP 5
    # Generate response
    # ------------------------------------------------------

    # response = generate_response(prompt)

    response = llm.generate_response(prompt)
    response = postprocess_response(response)

    # ------------------------------------------------------
    # STEP 6
    # Postprocess
    # ------------------------------------------------------

    # response = postprocess_response(response)

    # ------------------------------------------------------
    # STEP 7
    # Save conversation
    # ------------------------------------------------------

    memory.save_chat(
        processed_input,
        response
)
    postgres.save_chat_log(

        memory.session_id,

        user_input,

        response,

        "Gemini"

)
    # ------------------------------------------------------
    # Return response
    # ------------------------------------------------------

    return response