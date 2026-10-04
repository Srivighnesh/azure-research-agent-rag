import streamlit as st

def render_upload():
    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "docx", "txt","md", "pptx", "json", "py", "java", "html"],
        help="Upload a PDF, DOCX, or TXT file to index and ask questions about."
    )
    return uploaded_file