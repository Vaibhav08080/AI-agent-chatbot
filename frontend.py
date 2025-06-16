import streamlit as st

st.set_page_config(page_title="LangGraph AI Chatbot", layout="wide", page_icon="🤖")

# --- Custom CSS for background, cards, and fonts ---
st.markdown('''
    <style>
    body {
        background-color: #f4f7fa;
    }
    .main {
        background-color: #f4f7fa !important;
    }
    .stTextArea textarea::placeholder {
        color: #888 !important;
        opacity: 1 !important;
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        font-size: 1.1em;
        background: #fff;
        color: #222;
    }
    .stButton > button {
        color: white;
        background: linear-gradient(90deg, #2e86de 0%, #48c6ef 100%);
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1em;
        padding: 0.6em 2em;
        margin-top: 1em;
    }
    .chat-card {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 12px #0001;
        padding: 1.5em 2em;
        margin-bottom: 2em;
    }
    .chat-bubble-user {
        background: #e3f2fd;
        border-radius: 12px 12px 4px 12px;
        padding: 0.8em 1.2em;
        margin-bottom: 0.5em;
        color: #1565c0;
        font-size: 1.08em;
        display: inline-block;
        max-width: 80%;
    }
    .chat-bubble-agent {
        background: #e8f5e9;
        border-radius: 12px 12px 12px 4px;
        padding: 0.8em 1.2em;
        margin-bottom: 0.5em;
        color: #388e3c;
        font-size: 1.08em;
        display: inline-block;
        max-width: 80%;
    }
    .card-title {
        font-size: 1.5em;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.5em;
    }
    </style>
''', unsafe_allow_html=True)

# --- Beautiful Header ---
st.markdown("""
<div style='text-align:center; font-size:2em; font-weight:700; color:#1b263b; margin-bottom:0.2em;'>🤖 LangGraph AI Chatbot Playground</div>
<div style='text-align:center; font-size:1.2em; color:#555; margin-bottom:2em;'>Create and interact with powerful AI agents!</div>
""", unsafe_allow_html=True)

# --- Agent Setup Card ---
cols = st.columns([1,1,1])
with cols[0]:
    provider = st.radio("Provider", ("Groq", "OpenAI"), key="provider_radio")
with cols[1]:
    MODEL_NAMES_GROQ = ["llama3-70b-8192", "mixtral-8x7b-32768"]
    MODEL_NAMES_OPENAI = ["gpt-4o-mini"]
    if provider == "Groq":
        selected_model = st.selectbox("Groq Model", MODEL_NAMES_GROQ, key="groq_model")
    else:
        selected_model = st.selectbox("OpenAI Model", MODEL_NAMES_OPENAI, key="openai_model")
with cols[2]:
    allow_web_search = st.checkbox("🔍 Allow Web Search", key="web_search")
system_prompt = st.text_area("System Prompt", height=70, placeholder="Type your system prompt here...", key="system_prompt")

# --- Chat Section ---
st.markdown("<div class='card-title'>💬 Chat with your Agent</div>", unsafe_allow_html=True)
user_query = st.text_area("Your Message", height=100, placeholder="Ask anything!", key="user_query")
send_col, _ = st.columns([1,3])
with send_col:
    send = st.button("🚀 Ask Agent!", use_container_width=True)

# --- Show chat bubbles ---
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_URL = os.getenv("RENDER_BACKEND_URL", "https://ai-agent-chatbot-8f5k.onrender.com/chat")

if send and user_query.strip():
    import requests
    payload = {
        "model_name": selected_model,
        "model_provider": provider,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search
    }
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                user_bubble = f"<div class='chat-bubble-user'>🧑‍💻 {user_query}</div>"
                if isinstance(response_data, str):
                    ai_text = response_data
                elif isinstance(response_data, dict):
                    ai_text = response_data.get("response") or response_data.get("result") or str(response_data)
                else:
                    ai_text = str(response_data)
                agent_bubble = f"<div class='chat-bubble-agent'>🤖 {ai_text}</div>"
                st.markdown(user_bubble, unsafe_allow_html=True)
                st.markdown(agent_bubble, unsafe_allow_html=True)
                st.markdown("<hr style='margin:1.5em 0;' />", unsafe_allow_html=True)
                st.markdown("<div style='color:#888; font-size:0.95em;'>Final Response above ⬆️</div>", unsafe_allow_html=True)
        else:
            st.error(f"Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                user_bubble = f"<div class='chat-bubble-user'>🧑‍💻 {user_query}</div>"
                # Display only the text response if it's a string, else try common keys
                if isinstance(response_data, str):
                    ai_text = response_data
                elif isinstance(response_data, dict):
                    ai_text = response_data.get("response") or response_data.get("result") or str(response_data)
                else:
                    ai_text = str(response_data)
                agent_bubble = f"<div class='chat-bubble-agent'>🤖 {ai_text}</div>"
                st.markdown(user_bubble, unsafe_allow_html=True)
                st.markdown(agent_bubble, unsafe_allow_html=True)
                st.markdown("<hr style='margin:1.5em 0;' />", unsafe_allow_html=True)
                st.markdown("<div style='color:#888; font-size:0.95em;'>Final Response above ⬆️</div>", unsafe_allow_html=True)
        else:
            st.error(f"Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
