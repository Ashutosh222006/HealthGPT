import streamlit as st

# ======================================
# SHOW CHAT
# ======================================

def show_chat(messages):

    st.title("🏥 AI Health Assistant")

    st.caption(
        "AI-powered Medical Assistant using Groq + RAG + ChromaDB"
    )

    # ======================================
    # WELCOME MESSAGE
    # ======================================

    if len(messages) == 0:

        st.info(
            """
👋 Welcome to AI Health Assistant

You can ask about:

• Diseases

• Symptoms

• Medicines

• Diet Plans

• Exercise

• First Aid

• Medical Reports

• General Health

The assistant uses AI + RAG + your medical PDFs for better answers.
"""
        )

    # ======================================
    # DISPLAY CHAT
    # ======================================

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# ======================================
# USER INPUT
# ======================================

def get_user_input():

    return st.chat_input(
        "Ask your health question...",
        key="text_chat"
    )