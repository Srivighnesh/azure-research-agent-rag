import streamlit as st
from config.settings import VECTOR_STORE_ID

def render_upload():
    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "docx", "txt","md", "pptx", "json", "py", "java", "html"],
        help="Upload a PDF, DOCX, or TXT file to index and ask questions about."
    )
    return uploaded_file

def render_upload_section(file_search, documents):
    if file_search:
        try:
            # Validate document
            documents.validate_file(file_search)
            st.success(f"✅ File selected: {file_search.name}")
            
            # st.write( f"Size: {documents.get_file_size_mb(uploaded_file):.2f} MB" )
            
            if st.button("📤 Upload to Knowledge Base"):
                with st.spinner( "Uploading and processing document..." ):
                    result = file_search.upload_file(
                        VECTOR_STORE_ID,
                        file_search
                    )
                st.success( f"✅ {file_search.name} uploaded successfully!")
                st.write( f"File ID: `{result.id}`")

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error("Failed to upload document.")
            st.exception(e)