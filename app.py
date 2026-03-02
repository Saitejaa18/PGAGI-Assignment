import streamlit as st
from chatbot import HiringAssistant

st.set_page_config(
    page_title="TalentScout · Hiring Assistant",
    page_icon="🚀",
    layout="centered",
)

# ── Session state ──────────────────────────────────────────────────────────────
if "assistant" not in st.session_state:
    st.session_state.assistant = HiringAssistant()
if "messages" not in st.session_state:
    st.session_state.messages = st.session_state.assistant.initialize_conversation()

assistant = st.session_state.assistant

# ── Minimal CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background */
.stApp { background: #0F1117; color: #E2E8F0; }

/* Hide chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Chat input */
[data-testid="stChatInput"] textarea {
    background: #1A1D2E !important;
    border: 1px solid #2D3148 !important;
    border-radius: 12px !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #6D28D9 !important;
    box-shadow: 0 0 0 2px rgba(109,40,217,0.2) !important;
}

/* Fade-in for messages */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessage"] { animation: fadeIn 0.25s ease; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #2D3148; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 32px 0 20px 0;">
    <div style="font-size:2.2rem">🚀</div>
    <h2 style="margin:8px 0 4px; font-weight:600; color:#E2E8F0;">TalentScout</h2>
    <p style="color:#64748B; font-size:0.88rem; margin:0;">AI-powered candidate screening</p>
</div>
<hr style="border:none; border-top:1px solid #1E2130; margin-bottom:8px;">
""", unsafe_allow_html=True)

# ── Messages ───────────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ── Input ──────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Type your response…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = assistant.handle_message(user_input, st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()