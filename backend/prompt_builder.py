"""
prompt_builder.py

Builds the final prompt that will be
sent to the LLM.
"""

# ==========================================================
# LOAD SYSTEM PROMPT
# ==========================================================

from pathlib import Path

SYSTEM_PROMPT = Path(
    "assets/system_prompt.txt"
).read_text(encoding="utf-8")


# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_prompt(
    history: list,
    current_input: str
) -> str:
    """
    Build the final prompt.
    """

    conversation = ""

    # ----------------------------------------------
    # Previous Conversation
    # ----------------------------------------------

    for message in history:

        role = message["role"].capitalize()

        conversation += (
            f"{role}: {message['content']}\n"
        )

    # ----------------------------------------------
    # Final Prompt
    # ----------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

Conversation History:

{conversation}

Current User Question:

{current_input}

Assistant:
"""

    return prompt