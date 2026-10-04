import streamlit as st


def display_citations(citations):

    if not citations:
        return

    st.subheader("📚 Sources")

    for citation in citations:
        st.write(citation)