import os
import base64
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CCD UNAB",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Logo en base64
def get_logo_b64():
    try:
        with open("unab.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_b64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:60px; margin-bottom:8px;">' if logo_b64 else ""

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&family=Open+Sans:wght@300;400;500&display=swap');

    * {{ font-family: 'Open Sans', sans-serif; }}

    [data-testid="stAppViewContainer"] {{
        background: #f5f5f5;
    }}

    [data-testid="stSidebar"] {{ display: none; }}

    .block-container {{
        max-width: 780px;
        padding-top: 0 !important;
        padding-bottom: 5rem;
    }}

    /* Header */
    .unab-header {{
        background: linear-gradient(135deg, #F47920 0%, #e06810 100%);
        padding: 24px 32px 20px;
        border-radius: 0 0 20px 20px;
        margin-bottom: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(244,121,32,0.3);
    }}

    .unab-header h1 {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 1.6rem;
        color: white;
        margin: 8px 0 4px;
        letter-spacing: -0.5px;
    }}

    .unab-header p {{
        color: rgba(255,255,255,0.88);
        font-size: 0.85rem;
        margin: 0;
        font-weight: 300;
    }}

    /* ID input */
    .id-section {{
        background: white;
        border: 2px solid #F47920;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}

    div[data-testid="stTextInput"] input {{
        border: 1.5px solid #e0e0e0 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
        background: #fafafa !important;
        transition: border 0.2s;
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: #F47920 !important;
        box-shadow: 0 0 0 3px rgba(244,121,32,0.12) !important;
    }}

    /* Chat messages */
    [data-testid="stChatMessage"] {{
        border-radius: 16px !important;
        margin-bottom: 8px !important;
        padding: 4px !important;
    }}

    [data-testid="stChatMessage"][data-testid*="user"] {{
        background: #fff3e8 !important;
    }}

    /* Chat input */
    [data-testid="stChatInput"] {{
        border: 2px solid #F47920 !important;
        border-radius: 14px !important;
    }}

    [data-testid="stChatInput"]:focus-within {{
        box-shadow: 0 0 0 3px rgba(244,121,32,0.15) !important;
    }}

    /* Send button */
    [data-testid="stChatInputSubmitButton"] {{
        background: #F47920 !important;
        border-radius: 10px !important;
    }}

    .id-label {{
        font-size: 0.82rem;
        color: #888;
        margin-bottom: 4px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}
</style>

<div class="unab-header">
    {logo_html}
    <h1>Centro de Competencias Digitales</h1>
    <p>Universidad Autónoma de Bucaramanga · Asistente Virtual</p>
</div>
""", unsafe_allow_html=True)

# ID estudiante
st.markdown('<p class="id-label">ID de estudiante (opcional)</p>', unsafe_allow_html=True)
estudiante_id = st.text_input(
    label="id",
    label_visibility="collapsed",
    placeholder="Ej: 20230004  —  Ingrésalo para consultar tu progreso personal",
    key="estudiante_id",
)

def call_n8n(pregunta: str, estudiante_id: str) -> str:
    webhook_url = os.getenv(
        "N8N_CHAT_WEBHOOK_URL",
        "https://unab-n8n.duckdns.org:5678/webhook/ccd-chat",
    ).strip()

    payload = {
        "pregunta": pregunta,
        "estudiante_id": estudiante_id,
        "message": pregunta,
        "source": "streamlit_chat",
    }

    response = requests.post(webhook_url, json=payload, timeout=120)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        return response.text

    if isinstance(data, str):
        return data

    return (
        data.get("respuesta")
        or data.get("output")
        or data.get("answer")
        or data.get("response")
        or data.get("text")
        or str(data)
    )

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "¡Hola! 👋 Soy el asistente virtual del CCD de la UNAB. Puedo ayudarte con información sobre cursos, la ruta de competencias, calendario e insignia. Si quieres consultar tu progreso personal, ingresa tu ID arriba.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Escribe tu pregunta sobre el CCD...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            try:
                answer = call_n8n(prompt, estudiante_id or "")
            except Exception as exc:
                answer = f"No pude conectarme en este momento: {exc}"
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    