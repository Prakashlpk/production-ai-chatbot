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

st.markdown("""
<style>

/* ==========================
   IMPORT FONT
========================== */

@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
}

/* ==========================
   MAIN BACKGROUND
========================== */

.stApp{

    background:
    linear-gradient(rgba(6,25,52,0.93),
    rgba(6,25,52,0.93)),
    url("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1800&q=80");

    background-size: cover;

    background-position: center;

    background-attachment: fixed;

}


/* ==========================
   SIDEBAR
========================== */

[data-testid="stSidebar"]{

    background:#FFFFFF;

    border-right:2px solid #D6E2F3;

    box-shadow:4px 0px 20px rgba(0,0,0,0.08);

}

/* ==========================
   SIDEBAR FONT
========================== */

[data-testid="stSidebar"] *{

    font-family:'Manrope', sans-serif !important;

}

/* Sidebar headings */

/* ==========================
   SIDEBAR HEADINGS
========================== */

[data-testid="stSidebar"] h1{

    color:#0B1F3A;

    font-size:28px;

    font-weight:800;

}

[data-testid="stSidebar"] h2{

    color:#0B1F3A;

    font-size:22px;

    font-weight:700;

}

[data-testid="stSidebar"] h3{

    color:#0B1F3A;

    font-size:16px;

    font-weight:700;

    text-transform:uppercase;

    letter-spacing:0.8px;

}


/* ==========================
   SIDEBAR TEXT
========================== */

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div{

    color:#243B55;

    font-family:'Manrope',sans-serif;

    font-size:15px;

    font-weight:600;
}

/* ==========================
   SIDEBAR CARDS
========================== */

[data-testid="stSidebar"] .stSelectbox,
[data-testid="stSidebar"] .stToggle,
[data-testid="stSidebar"] .stFileUploader{

    background:#FFFFFF;

    border:1px solid #D9E2EF;

    border-radius:16px;

    padding:15px;

    margin-bottom:18px;

    box-shadow:0px 4px 12px rgba(0,0,0,0.05);

}
/* ==========================
   MAIN TITLE
========================== */


h1{

    color:#FFFFFF !important;

    font-size:48px;

    font-weight:800;

    letter-spacing:1px;

    text-shadow:
        0px 0px 8px rgba(255,255,255,0.25),
        0px 0px 20px rgba(0,153,255,0.35);

}

/* ==========================
   HEADINGS
========================== */

h2,h3,h4{

    color:white;

}

/* ==========================
   NORMAL TEXT
========================== */

p,
li{

    color:#F8FAFC;

    font-size:18px;

    line-height:1.8;

}
/* ==========================
   CHAT INPUT
========================== */

.stChatInput{

    background:white;

    border-radius:16px;

    padding:8px;

}

/* ==========================
   INPUT BOX
========================== */

.stTextInput input{

    background:white;

    color:black;

    border-radius:12px;

}

/* ==========================
   BUTTONS
========================== */
/* ==========================
   NORMAL BUTTONS
========================== */

/* ==========================
   BUTTONS
========================== */

div.stButton > button{

    background:#061934;

    color:#FFFFFF !important;

    border:none;

    border-radius:12px;

    font-weight:600;

}

div.stButton > button *{

    color:#FFFFFF !important;

    fill:#FFFFFF !important;

}

div.stButton > button:hover{

    background:#0A2A57;

    color:#FFFFFF !important;

}

div.stButton > button:hover *{

    color:#FFFFFF !important;

}
/* ==========================
   CONTAINERS
========================== */

div[data-testid="stVerticalBlock"]{

    border-radius:20px;

}

/* ==========================
   FILE UPLOADER
========================== */

[data-testid="stFileUploader"]{

    background:rgba(255,255,255,0.08);

    border-radius:15px;

    padding:15px;

}

/* Hide the duplicate Upload text */

[data-testid="stFileUploader"] button p{

    display:none !important;

}
[data-testid="stFileUploader"] button::after{

    content:"Upload";

    color:#061934;

    font-weight:600;

    font-size:15px;

}

/* Fix Upload Button */

[data-testid="stFileUploader"] section button{

    background:#FFFFFF !important;

    color:#061934 !important;

    border:1px solid #D6E2F3 !important;

    border-radius:10px !important;

    font-size:15px !important;

    font-weight:600 !important;

    padding:8px 18px !important;

    width:auto !important;

}

/* ==========================
   CHAT MESSAGE
========================== */

[data-testid="stChatMessage"]{

    background:rgba(255,255,255,0.08);

    border-radius:18px;

    padding:12px;

    margin-bottom:10px;

}

</style>
""", unsafe_allow_html=True)


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

    st.markdown(
        """
        <style>
        [data-testid="stFileUploader"] button {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"],
        label_visibility="collapsed"
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

# st.caption(
#     "AI/ML Hiring Assignment"
# )

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
- 🎤 Voice Input
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