import streamlit as st


def render_chat_input():

    return st.text_area(
        "Ask a question",
        placeholder="Ask something about your documents..."
    )


def display_answer(answer: str):

    st.subheader("Answer")
    st.write(answer)