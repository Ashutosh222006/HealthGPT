# components/voice.py

import streamlit.components.v1 as components
import os

_component = components.declare_component(
    "voice_component",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def voice_component(key="voice"):
    """
    Returns recognized text from browser speech recognition.
    """
    return _component(key=key, default="")