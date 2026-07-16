import streamlit as st
import traceback
import tempfile
import os
import hashlib
import time

from components.upload import upload_report
from components.chat import show_chat
from components.sidebar import show_sidebar
from components.camera import show_camera
from components.custom_input import custom_chat_input
from components.speaker import speak_button
from services.rag import speech_to_text, get_answer
from services.database import (
    create_database,
    create_chat,
    save_message,
    load_messages,
    load_chat_sessions,
    update_chat_title
)
from services.image_analysis import (
    image_to_base64,
    analyze_image
)
from audio_recorder_streamlit import audio_recorder


def save_audio_file(audio_bytes):
    if audio_bytes is None:
        return None

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.write(audio_bytes)
    temp.close()

    return temp.name


# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🏥",
    layout="wide"
)

# ======================================
# LOAD CSS
# ======================================

def load_css():
    with open("styles/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ======================================
# PREMIUM SPLASH SCREEN / LOADER
# ======================================

if "app_loaded" not in st.session_state:
    splash_placeholder = st.empty()

    splash_html = """
    <style>
    .splash-screen {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: radial-gradient(circle at 50% 40%, #16213e 0%, #0f172a 70%);
        z-index: 9999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #10b981;
        font-family: 'Segoe UI', sans-serif;
    }
    .pulse-icon {
        font-size: 90px;
        animation: pulse 1.5s infinite ease-in-out;
        margin-bottom: 22px;
        filter: drop-shadow(0 0 18px rgba(16, 185, 129, 0.55));
    }
    @keyframes pulse {
        0% { transform: scale(0.85); opacity: 0.7; }
        50% { transform: scale(1.15); opacity: 1; }
        100% { transform: scale(0.85); opacity: 0.7; }
    }
    .loading-text {
        font-size: 22px;
        font-weight: 600;
        letter-spacing: 3px;
        color: #f8fafc;
        animation: blink 1.5s infinite;
    }
    .loading-bar {
        margin-top: 18px;
        width: 160px;
        height: 4px;
        border-radius: 4px;
        background: rgba(148, 163, 184, 0.25);
        overflow: hidden;
    }
    .loading-bar::after {
        content: "";
        display: block;
        width: 40%;
        height: 100%;
        background: #10b981;
        border-radius: 4px;
        animation: slide 1.2s infinite ease-in-out;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
    @keyframes slide {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(350%); }
    }
    </style>
    <div class="splash-screen">
        <div class="pulse-icon">🏥</div>
        <div class="loading-text">INITIALIZING AI...</div>
        <div class="loading-bar"></div>
    </div>
    """

    splash_placeholder.markdown(splash_html, unsafe_allow_html=True)
    time.sleep(2.5)
    splash_placeholder.empty()
    st.session_state.app_loaded = True
    st.rerun()

# ======================================
# DATABASE & MAIN APP
# ======================================

create_database()

# ======================================
# SESSION STATE
# ======================================

if "chat_id" not in st.session_state:
    st.session_state.chat_id = create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = load_messages(st.session_state.chat_id)

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "voice_question" not in st.session_state:
    st.session_state.voice_question = None

if "last_audio" not in st.session_state:
    st.session_state.last_audio = ""

if "processing_audio" not in st.session_state:
    st.session_state.processing_audio = False

if "voice_key" not in st.session_state:
    st.session_state.voice_key = 0

image_base64 = None

# ======================================
# SIDEBAR
# ======================================

language, profile = show_sidebar(st.session_state.messages)

# ======================================
# CHAT HISTORY
# ======================================

st.sidebar.divider()
st.sidebar.subheader("💬 Chat History")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    # Agar current chat khaali hai to naya chat mat banao
    if len(st.session_state.messages) > 0:
        st.session_state.chat_id = create_chat("New Chat")

    st.session_state.messages = []
    st.rerun()

sessions = [
    s for s in load_chat_sessions()
    if load_messages(s[0])   # sirf wahi chats jisme messages hain
]

for chat_id, title in sessions:
    label = "🟢 " + title if chat_id == st.session_state.chat_id else "💬 " + title

    if st.sidebar.button(label, key=f"chat_{chat_id}", use_container_width=True):
        st.session_state.chat_id = chat_id
        st.session_state.messages = load_messages(chat_id)
        st.rerun()

# ======================================
# CHAT
# ======================================

show_chat(st.session_state.messages)

audio_path = None

# ======================================
# VOICE INPUT
# ======================================

audio_bytes = audio_recorder(
    text="🎤 Speak",
    recording_color="#ff4b4b",
    neutral_color="#6c63ff",
    icon_name="microphone",
    icon_size="2x",
    key="voice_recorder"
)

if audio_bytes:
    audio_hash = hashlib.md5(audio_bytes).hexdigest()

    if audio_hash != st.session_state.last_audio:
        st.session_state.last_audio = audio_hash
        audio_path = save_audio_file(audio_bytes)

        with st.spinner("🎤 Converting..."):
            text = speech_to_text(audio_path)

        if os.path.exists(audio_path):
            os.remove(audio_path)

        if text:
            st.session_state.voice_question = text

# ======================================
# INPUT + TOOLS
# ======================================

tools_col, speak_col, input_col = st.columns([1, 1, 10])

# ======================================
# TOOLS
# ======================================

with tools_col:
    with st.popover("🛠"):
        st.markdown("## 🛠 Tools")

        # -----------------------------
        # CAMERA TOGGLE
        # -----------------------------

        if "camera_open" not in st.session_state:
            st.session_state.camera_open = False

        if st.button(
            "📷 Open Camera" if not st.session_state.camera_open else "❌ Close Camera",
            key="camera_toggle"
        ):
            st.session_state.camera_open = not st.session_state.camera_open
            st.rerun()

        # -----------------------------
        # CAMERA
        # -----------------------------

        if st.session_state.camera_open:
            image = show_camera()

            if image is not None:
                st.image(image, use_container_width=True)
                image_base64, _ = image_to_base64(image)

                if st.button("🔍 Analyze Camera", key="camera_analysis"):
                    with st.spinner("Analyzing Camera Image..."):
                        result = analyze_image(
                            image,
                            question="Analyze this medical image in detail."
                        )

                    st.success("Analysis Complete")
                    st.markdown(result)

        st.divider()

        # -----------------------------
        # UPLOAD
        # -----------------------------

        uploaded_file = upload_report()

        if uploaded_file is not None:
            st.image(uploaded_file, use_container_width=True)
            image_base64, _ = image_to_base64(uploaded_file)

            if st.button("🔍 Analyze Upload", key="upload_analysis"):
                with st.spinner("Analyzing Uploaded Image..."):
                    result = analyze_image(
                        uploaded_file,
                        question="Analyze this medical image in detail."
                    )

                st.success("Analysis Complete")
                st.markdown(result)

# ======================================
# INPUT
# ======================================

with input_col:
    question = custom_chat_input()

# ======================================
# VOICE -> TEXT
# ======================================

if st.session_state.voice_question:
    question = st.session_state.voice_question
    st.session_state.voice_question = None

# ======================================
# SPEAKER
# ======================================

with speak_col:
    if st.button("🔊", key="speak_btn", use_container_width=True):
        st.session_state["play_voice"] = True

if audio_path and os.path.exists(audio_path):
    try:
        os.remove(audio_path)
    except:
        pass

# ======================================
# AI CHAT
# ======================================

if question:
    if len(st.session_state.messages) == 0:
        title = question.strip()

        if len(title) > 30:
            title = title[:30] + "..."

        update_chat_title(st.session_state.chat_id, title)

    st.session_state.messages.append({"role": "user", "content": question})
    save_message(st.session_state.chat_id, "user", question)

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Thinking..."):
            try:
                answer = get_answer(
                    question=question,
                    language=language,
                    profile=profile,
                    image_base64=image_base64
                )
            except Exception as e:
                answer = f"""
❌ Error

{str(e)}

{traceback.format_exc()}
"""

        st.markdown(answer)

    st.session_state.last_answer = answer
    st.session_state.messages.append({"role": "assistant", "content": answer})
    save_message(st.session_state.chat_id, "assistant", answer)

st.session_state.processing_audio = False

# ======================================
# PLAY VOICE (LAST)
# ======================================

if st.session_state.get("play_voice", False):
    speak_button(st.session_state.last_answer)
    st.session_state["play_voice"] = False