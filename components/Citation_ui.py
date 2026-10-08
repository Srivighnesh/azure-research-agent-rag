import re
import streamlit as st

CITATION_PATTERN = re.compile(r"【([^】]*)】")


def extract_and_clean(answer: str):
    """Replace markers like 【12:1†source】 with [1], [2]... and return the sources."""
    markers = []
    for m in CITATION_PATTERN.findall(answer):
        if m not in markers:
            markers.append(m)

    def repl(match):
        return f"[{markers.index(match.group(1)) + 1}]"

    cleaned = CITATION_PATTERN.sub(repl, answer)
    return cleaned, markers


def display_citations(citations):
    if not citations:
        return

    st.subheader("📚 Sources")

    for i, citation in enumerate(citations, start=1):
        st.write(f"[{i}] {citation}")


def render_answer(answer: str):
    cleaned_answer, citations = extract_and_clean(answer)
    st.markdown(cleaned_answer)
    display_citations(citations)
