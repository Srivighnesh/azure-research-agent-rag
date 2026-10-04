import streamlit as st

from services.foundry_service import FoundryService
from services.document_service import DocumentService
from services.file_service import FileSearchService

from components.chart_ui import (
    render_chat_input,
    display_answer
)

from components.upload_ui import render_upload
from utils.helpers import validate_question
from config.settings import VECTOR_STORE_ID

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="centered"
)

st.title("🔎 Research Agent")
st.write("Research your documents using Microsoft Foundry.")
st.write("VECTOR STORE:", VECTOR_STORE_ID)

@st.cache_resource
def get_foundry_service():
    return FoundryService()

@st.cache_resource
def get_file_search_service():
    return FileSearchService()

@st.cache_resource
def get_document_service():
    return DocumentService()

# Initialize services
try:
    foundry = get_foundry_service()
    file_search = get_file_search_service()
    documents = get_document_service()

except Exception as e:
    st.error("Unable to initialize services.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# DOCUMENT UPLOAD
# --------------------------------------------------

uploaded_file = render_upload()

if uploaded_file:

    try:
        # Validate document
        documents.validate_file(uploaded_file)
        st.success(f"✅ File selected: {uploaded_file.name}")
        
        # st.write( f"Size: {documents.get_file_size_mb(uploaded_file):.2f} MB" )
        
        if st.button("📤 Upload to Knowledge Base"):
            with st.spinner( "Uploading and processing document..." ):
                result = file_search.upload_file(
                    VECTOR_STORE_ID,
                    uploaded_file
                )
            st.success( f"✅ {uploaded_file.name} uploaded successfully!")
            st.write( f"File ID: `{result.id}`")

    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error("Failed to upload document.")
        st.exception(e)
# -------------------------------------------------
#   DELETE THE FILE
#--------------------------------------------------

st.subheader("📃 Manage Documents")
files = file_search.list_files(VECTOR_STORE_ID)

if files is None or len(files.data) == 0:
    st.info("No documents found in the knowledge base. Upload a document to get started.")

for file in files.data:
    
    name = file_search.file_names.get(file.id, file.id)
    filename = getattr(file, "filename", file.id)
    col1, col2 = st.columns([4,1])

    with col1:
        st.write(f"📄 {name}")
    with col2:
        if st.button("Delete", key=file.id):
            file_search.delete_file(
                vector_store_id=VECTOR_STORE_ID,
                file_id=file.id
            )
            st.success(f"File removed: {name}")
            st.rerun()
# --------------------------------------------------
# QUESTION
# --------------------------------------------------

st.subheader("💬 Ask a Question")
question = render_chat_input()
if st.button("🔍 Research"):
    if not validate_question(question):
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Researching..."):
                answer, sources = foundry.ask_question(question)
            display_answer(answer)
            if sources:
                st.subheader("📁 Sources")
                for source in set(sources):
                    st.write(f"📃 {source}")
        except Exception as e:
            st.error("Failed to get a response.")
            st.exception(e)