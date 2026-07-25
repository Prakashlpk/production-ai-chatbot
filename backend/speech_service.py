"""
speech_service.py

Speech-to-Text using Hugging Face Whisper.
"""

from transformers import pipeline

print("Loading Whisper Tiny...")

speech_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny"
)

print("Whisper Loaded")


def speech_to_text(audio_path):

    result = speech_pipeline(
        audio_path,
        generate_kwargs={
            "language": "english",
            "task": "transcribe"
        }
    )

    return result["text"]