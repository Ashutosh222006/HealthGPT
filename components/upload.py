import streamlit as st

def upload_report():

    return st.file_uploader(
        "Upload Report",
        type=["pdf","png","jpg","jpeg"],
        key="upload_tool"
    )