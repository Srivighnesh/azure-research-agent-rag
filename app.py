import streamlit as st
from services.foundry_service import FoundryService
from utils.helpers import validate_question

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Research FAQ Bot",
    page_icon="🔎",
    layout="centered",
)

# Edit these to match the documents your agent works with
FAQS = [
    "What are the main topics covered in the documents?",
    "what is AI engeneering",
    "How to print a single envelope?"
    "Are there any risks or issues mentioned?",
]

WELCOME_MESSAGE = (
    "👋 Hi! I'm your Research Assistant. Ask me anything about your "
    "documents, or pick one of the common questions below."
)

# --------------------------------------------------
# FOUNDRY SERVICE
# --------------------------------------------------
@st.cache_resource
def get_foundry_service():
    return FoundryService()


try:
    foundry = get_foundry_service()
except Exception as e:
    st.error("Unable to initialize Foundry service.")
    st.exception(e)
    st.stop()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []      # [{"role", "content", "sources"}]
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


def queue_question(q: str):
    """Callback for FAQ buttons: stores the question to be asked on rerun."""
    st.session_state.pending_question = q


def clear_chat():
    st.session_state.messages = []
    st.session_state.pending_question = None


def render_sources(sources):
    if sources:
        unique_sources = list(dict.fromkeys(sources))
        with st.expander(f"📚 Sources ({len(unique_sources)})"):
            for s in unique_sources:
                st.write(f"📄 {s}")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("🔎 Research FAQ Bot")
    st.caption("Powered by Microsoft Foundry")
    st.divider()

    st.subheader("💡 Common Questions")
    for i, faq in enumerate(FAQS):
        st.button(
            faq,
            key=f"sidebar_faq_{i}",
            on_click=queue_question,
            args=(faq,),
            use_container_width=True,
        )

    st.divider()
    st.button("🗑️ Clear chat", on_click=clear_chat, use_container_width=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🔎 Research FAQ Bot")
st.caption("Ask questions and get answers from your documents, with sources.")

# --------------------------------------------------
# WELCOME + QUICK QUESTIONS (only before first message)
# --------------------------------------------------
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(WELCOME_MESSAGE)

    cols = st.columns(2)
    for i, faq in enumerate(FAQS):
        with cols[i % 2]:
            st.button(
                faq,
                key=f"main_faq_{i}",
                on_click=queue_question,
                args=(faq,),
                use_container_width=True,
            )

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_sources(msg.get("sources"))

# --------------------------------------------------
# INPUT HANDLING
# --------------------------------------------------
typed = st.chat_input("Type your question here...")
question = typed or st.session_state.pending_question
st.session_state.pending_question = None

if question:
    if not validate_question(question):
        st.warning("Please enter a valid question.")
    else:
        # Show + store the user's message
        st.session_state.messages.append(
            {"role": "user", "content": question, "sources": None}
        )
        with st.chat_message("user", avatar="🧑"):
            st.markdown(question)

        # Get + show the assistant's reply
        with st.chat_message("assistant", avatar="🤖"):
            try:
                with st.spinner("Researching..."):
                    answer, sources = foundry.ask_question(question)
                st.markdown(answer)
                render_sources(sources)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
            except Exception as e:
                error_text = "⚠️ Sorry, I couldn't get a response. Please try again."
                st.error(error_text)
                st.exception(e)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_text, "sources": None}
                )