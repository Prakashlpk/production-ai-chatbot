from backend.conversation_manager import process_request
import streamlit as st
from database.mongo_service import mongo
from backend.memory_service import memory
from database.postgres_service import postgres
from streamlit_mic_recorder import mic_recorder
# from backend.speech_service import speech_to_text
from backend.document_service import document_service
print(type(postgres))
import tempfile
import os
import hashlib
from backend.speech_service import speech_to_text


print(dir(postgres))

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Production AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
    


if "mongo_connected" not in st.session_state:

    mongo.connect()
    postgres.connect()
    postgres.create_tables()    
    st.session_state.mongo_connected = True

# if "mongo_connected" not in st.session_state:

#     mongo_status = mongo.connect()

#     print(f"Mongo Connect Status: {mongo_status}")

#     st.write(f"Mongo Connect Status: {mongo_status}")  # Temporary

#     postgres.connect()
#     postgres.create_tables()

#     st.session_state.mongo_connected = mongo_status    

# ==========================================================
# SESSION STATE
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("⚙️ Settings")

    selected_model = st.selectbox(
        "Select LLM",
        ["Gemini", "OpenAI"]
    )

    enable_memory = st.toggle(
        "Conversation Memory",
        value=True
    )

    enable_streaming = st.toggle(
        "Streaming Response",
        value=False
    )

    st.divider()

    st.subheader("📄 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"]
    )
    document_text = ""

    if uploaded_file:

        document_text = document_service.read_document(
            uploaded_file
        )

        st.success("✅ Document uploaded successfully.")

        st.info(
            f"Characters extracted: {len(document_text)}"
        )

        if document_text:

            st.text_area(
                "Document Preview",
                document_text[:2000],
                height=250
            )


    st.divider()

    st.subheader("💬 Conversation")

    recent_sessions = memory.get_recent_sessions()

    if st.button(
        "💬 New Chat",
        use_container_width=True,
        key="new_chat"
    ):
        memory.clear_chat()

        st.session_state.messages = []

        st.rerun()

    st.markdown("### 📜 Recent Conversations")

    recent_sessions = memory.get_recent_sessions()

    if recent_sessions:

        for session in recent_sessions:

            col1, col2 = st.columns([8, 1])

            with col1:

                if st.button(
                    session["title"],
                    key=f"open_{session['session_id']}",
                    use_container_width=True
                ):

                    # Switch to the selected session
                    memory.set_current_session(
                        session["session_id"]
                    )

                    # Load the selected conversation into the UI
                    st.session_state.messages = memory.load_chat(
                        session["session_id"]
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{session['session_id']}"
                ):

                    memory.clear_session(
                        session["session_id"]
                    )

                    st.rerun()

    else:

        st.caption("No previous conversations.")
    st.divider()

    st.subheader("📊 System Status")

    st.write(f"**Model:** {selected_model}")

    st.write(
        f"**Memory:** {'Enabled' if enable_memory else 'Disabled'}"
    )

    st.write(
        f"**Streaming:** {'Enabled' if enable_streaming else 'Disabled'}"
    )

    st.write("**Voice:** Ready")

    st.write("**LLM:** Gemini Connected")

    st.write("**Database:** MongoDB Connected")

# ==========================================================
# HEADER
# ==========================================================

st.title("🤖 Production AI Chatbot")

st.caption(
    "AI/ML Hiring Assignment"
)

st.divider()

# ==========================================================
# WELCOME MESSAGE
# ==========================================================

if len(st.session_state.messages) == 0:

    st.info(
        """
### 👋 Welcome

This chatbot is designed with a production-oriented architecture.

Current capabilities:

- 💬 Text Chat
- 🎤 Voice Input (Coming Next)
- 📄 Document Upload
- 🧠 Conversation Memory
- 🛡️ Guardrails
- 📚 Long Context Handling
- ⚡ Streaming Responses
- 🗄️ MongoDB + PostgreSQL Support

Ask your first question below.
"""
    )

# ==========================================================
# DISPLAY CHAT HISTORY
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================================
# INPUT SECTION
# ==========================================================

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

user_input = None

col1, col2 = st.columns([1,8])

with col1:

    audio = mic_recorder(
    start_prompt="🎤",
    stop_prompt="⏹",
    key="voice"
)
    if audio:
        

        if audio:

            current_audio_hash = hashlib.md5(
                audio["bytes"]
            ).hexdigest()

            if current_audio_hash != st.session_state.last_audio_hash:

                st.session_state.last_audio_hash = current_audio_hash

                try:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".webm"
                    ) as temp_audio:

                        temp_audio.write(audio["bytes"])

                        temp_audio_path = temp_audio.name

                    with st.spinner("Listening..."):

                        recognized_text = speech_to_text(
                            temp_audio_path
                        )

                    os.remove(temp_audio_path)

                    if recognized_text and recognized_text.strip():

                        user_input = recognized_text.strip()

                    else:

                        st.warning("Couldn't understand the audio.")



                except Exception as error:

                    st.error(
                        f"Speech Recognition Error: {error}"
                    )

                finally:

                    if os.path.exists(temp_audio_path):
                        os.remove(temp_audio_path)    

                # with open("voice.wav", "wb") as f:

        #     f.write(audio["bytes"])

        # voice_input = speech_to_text("voice.wav")

        # st.success(voice_input)

with col2:

    typed_input = st.chat_input(
        "Ask me anything..."
    )

if typed_input:

    user_input = typed_input
# If voice input is available, use it as the chatbot input
# if "voice_input" in locals() and voice_input:

#     user_input = voice_input    

# ==========================================================
# VOICE PLACEHOLDER
# ==========================================================

# ==========================================================
# USER MESSAGE
# ==========================================================

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Generate response
    response = process_request(

    user_input,

    document_text

)

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Refresh the page so the conversation is rendered
    st.rerun()