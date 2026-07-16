import streamlit as st

from services.database import (
    create_chat,
    delete_chat
)


def show_sidebar(messages):

    with st.sidebar:

        st.title("🏥 AI Health Assistant")

        st.markdown("---")

        st.metric("🤖 Model", "Llama 3.3 70B")

        st.metric("📚 Database", "ChromaDB")

        st.markdown("---")

        # ==========================
        # NEW CHAT
        # ==========================

        if st.button("🆕 New Chat"):

            st.session_state.chat_id = create_chat("New Chat")

            st.session_state.messages = []

            st.rerun()

        # ==========================
        # DELETE CHAT
        # ==========================

        if st.button("🗑 Delete Current Chat"):

            delete_chat(st.session_state.chat_id)

            st.session_state.chat_id = create_chat()

            st.session_state.messages = []

            st.rerun()

        st.markdown("---")

        # ==========================
        # LANGUAGE
        # ==========================

        language = st.radio(
            "🌐 Language",
            ["English", "Hindi"],
            index=0 if st.session_state.language == "English" else 1,
            horizontal=True
        )

        st.session_state.language = language

        st.markdown("---")

        # ==========================
        # EXPORT CHAT
        # ==========================

        chat_text = ""

        for msg in messages:

            chat_text += f"\n========== {msg['role'].upper()} ==========\n"

            chat_text += msg["content"]

            chat_text += "\n\n"

        st.download_button(
            "📥 Export Chat",
            data=chat_text,
            file_name="AI_Health_Chat.txt",
            mime="text/plain"
        )

        st.markdown("---")

        # ==========================
        # HEALTH PROFILE
        # ==========================

        st.subheader("👤 Health Profile")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=25
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        height = st.number_input(
            "Height (cm)",
            min_value=50,
            max_value=250,
            value=170
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=1,
            max_value=300,
            value=70
        )

        medical_condition = st.text_input(
            "Medical Condition",
            placeholder="Diabetes, BP, Asthma..."
        )

        allergies = st.text_input(
            "Allergies",
            placeholder="Penicillin, Dust..."
        )

        health_goal = st.selectbox(
            "Health Goal",
            [
                "General Health",
                "Weight Loss",
                "Weight Gain",
                "Muscle Gain",
                "Heart Health",
                "Diabetes Management"
            ]
        )

        st.markdown("---")

        st.caption("Made with ❤️ using Groq + ChromaDB")

        profile = {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "medical_condition": medical_condition,
            "allergies": allergies,
            "health_goal": health_goal
        }

        return language, profile