import streamlit as st

def show_camera():

    return st.camera_input(
        "Capture Image",
        key="camera_tool"
    )