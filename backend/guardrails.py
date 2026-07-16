"""
guardrails.py

Responsible for validating user input before sending it to the LLM.
"""

# ==========================================================
# BLOCKED PHRASES
# ==========================================================

BLOCKED_PATTERNS = [

    "ignore previous instructions",

    "ignore all instructions",

    "reveal system prompt",

    "show system prompt",

    "developer prompt",

    "bypass",

    "jailbreak",

    "hack",

    "disable guardrails",

    "forget previous instructions"

]

# ==========================================================
# PROMPT INJECTION
# ==========================================================

def detect_prompt_injection(text: str) -> bool:
    """
    Detect prompt injection attempts.
    """

    text = text.lower()

    for pattern in BLOCKED_PATTERNS:

        if pattern in text:

            return True

    return False


# ==========================================================
# VALIDATION
# ==========================================================

def validate_input(text: str):
    """
    Validate user prompt.

    Returns

    -------
    (bool, str)

    True  -> Safe

    False -> Unsafe
    """

    if detect_prompt_injection(text):

        return (

            False,

            "Sorry, I cannot process requests that attempt to manipulate the system."

        )

    return (

        True,

        "Safe"

    )