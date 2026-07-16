# Production AI Chatbot

A production-style AI chatbot built using **Python**, **Streamlit**, **Google Gemini**, **MongoDB**, and **PostgreSQL**. The chatbot supports conversation memory, document upload, context compression, guardrails, and structured chat logging.

---

## Features

- AI-powered conversational chatbot using Google Gemini
- Conversation memory using MongoDB
- Session management with recent conversation history
- PostgreSQL chat logging for analytics and auditing
- Context compression for long user inputs
- Prompt building with conversation history
- Input guardrails to filter unsafe or restricted prompts
- Document upload support (PDF, DOCX, TXT)
- Document-aware responses using uploaded document content
- Clean and modular production-style architecture
- Streamlit-based interactive user interface

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Model
- Google Gemini

### Databases
- MongoDB
- PostgreSQL

### Libraries
- google-generativeai
- pymongo
- psycopg2
- python-dotenv
- PyPDF2
- python-docx

---

## Project Structure

```
AI_CHATBOT/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
│
├── backend/
│   ├── conversation_manager.py
│   ├── llm_service.py
│   ├── prompt_builder.py
│   ├── preprocessor.py
│   ├── postprocessor.py
│   ├── guardrails.py
│   ├── context_compressor.py
│   └── document_service.py
│
├── database/
│   ├── mongo_service.py
│   └── postgres_service.py
│
└── uploads/
```

---

## Architecture

```
User
   │
   ▼
Streamlit UI
   │
   ▼
Conversation Manager
   │
   ├── Preprocessor
   ├── Guardrails
   ├── Context Compression
   ├── Prompt Builder
   └── Conversation Memory
            │
            ▼
       Google Gemini
            │
            ▼
     Post Processor
            │
      ┌─────┴─────┐
      ▼           ▼
 MongoDB     PostgreSQL
```

---

## Workflow

1. User submits a question through the Streamlit interface.
2. User input is preprocessed and token count is calculated.
3. Long inputs are compressed using context compression.
4. Guardrails validate the input.
5. Previous conversation history is retrieved from MongoDB.
6. Prompt Builder combines:
   - Conversation history
   - User question
   - Uploaded document (if available)
7. Gemini generates the response.
8. Response is postprocessed.
9. Conversation is stored in MongoDB.
10. Chat logs are stored in PostgreSQL.

---

## Context Compression

Long user inputs are automatically compressed before sending them to the language model. This helps reduce token usage while preserving the important context.

---

## Conversation Memory

Conversation history is stored in MongoDB, enabling:

- Recent conversations
- Session switching
- Conversation continuity

---

## Document Upload

Supported file types:

- PDF
- DOCX
- TXT

Uploaded documents are processed and their extracted text is included in the prompt, allowing the chatbot to answer questions based on the uploaded content.

---

## PostgreSQL Logging

Every conversation is logged with:

- Session ID
- User message
- Assistant response
- Model name
- Timestamp

This provides structured storage for reporting and future analytics.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/production-ai-chatbot.git
```

Navigate to the project folder:

```bash
cd production-ai-chatbot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and configure:

```text
GEMINI_API_KEY=

MONGODB_URI=

POSTGRES_HOST=

POSTGRES_PORT=

POSTGRES_DATABASE=

POSTGRES_USER=

POSTGRES_PASSWORD=
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Enhancements

- Retrieval-Augmented Generation (RAG)
- Vector Database Integration
- Streaming Responses
- Whisper-based Voice Input
- FastAPI Backend
- Redis Caching
- Deployment on Render or Vercel

---

## Author

**Prakash Kumar**

Production AI Chatbot Project
