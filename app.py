import os
import base64
import requests
import streamlit as st

NVIDIA_KEY = "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"
API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "meta/llama-3.1-8b-instruct"

SYSTEM = """Eres UNAB-Bot, el asistente virtual oficial del Centro de Competencias Digitales (CCD) de la Universidad Autónoma de Bucaramanga (UNAB), Bucaramanga, Colombia.

REGLAS ESTRICTAS:
- Responde SIEMPRE en español natural y conversacional
- Sé amable, claro y muy conciso
- NUNCA muestres código, SQL, JSON ni términos técnicos
- SOLO responde preguntas relacionadas con el CCD de la UNAB
- Si te preguntan algo que no es del CCD, di amablemente que solo puedes ayudar con temas del CCD
- NUNCA inventes información que no esté aquí

SOBRE EL CCD:
El Centro de Competencias Digitales (CCD) es un programa de la UNAB que certifica a los estudiantes en habilidades digitales esenciales para el mundo laboral actual.

RUTA CCD — 3 PILARES:
- Pilar 1 (OBLIGATORIO para todos): Interacción Digital
- Pilar 2 (ELIGE SOLO UNO): Narrativas Digitales / Visualización de Datos / Marca Personal Digital
- Pilar 3 (ELIGE SOLO UNO): IA Generativa / Legislación Digital / Bienestar Digital

IMPORTANTE: Solo el Pilar 1 es obligatorio. En el Pilar 2 el estudiante elige UN curso. En el Pilar 3 el estudiante elige UN curso. En total se toman 3 cursos.

INSIGNIA CCD:
- Se obtiene al completar los 3 pilares (un curso por pilar)
- Duración total del programa: 48 horas
- Es un certificado digital oficial reconocido por la UNAB
- Acredita competencias digitales para el mundo laboral

PRECIO:
- Valor total de la ruta: $374.000 pesos colombianos
- Incluye los 3 cursos (uno por pilar) y la insignia oficial
- Modalidades: Virtual y Presencial

CALENDARIO 2025:
- Apertura de inscripciones: 10 de marzo
- Prueba diagnóstica: 15 de marzo (obligatoria para inscribirse)
- Inicio de cursos: 25 de marzo
- Entrega de insignias: 30 de junio

PRUEBA DIAGNÓSTICA:
- Es obligatoria para poder inscribirse al programa
- Se realiza en línea
- Evalúa competencias digitales básicas del estudiante
- No tiene costo adicional

DESCRIPCIÓN DE LOS CURSOS:
Pilar 1:
- Interacción Digital: Fundamentos de comunicación y colaboración en entornos digitales

Pilar 2 (elige uno):
- Narrativas Digitales: Creación de contenido y storytelling digital
- Visualización de Datos: Análisis y presentación visual de información
- Marca Personal Digital: Construcción y gestión de identidad profesional en línea

Pilar 3 (elige uno):
- IA Generativa: Uso práctico de inteligencia artificial en el trabajo
- Legislación Digital: Marco legal del entorno digital colombiano
- Bienestar Digital: Salud mental y hábitos saludables en el mundo digital

CONTACTO:
- Universidad Autónoma de Bucaramanga (UNAB)
- Bucaramanga, Santander, Colombia
- Para más información visita el portal de la UNAB"""

def get_logo():
    for name in ["logopng", "logo.png", "unab.png", "logopng.png"]:
        try:
            with open(name, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except:
            continue
    return None

def call_nvidia(pregunta, estudiante_id, history):
    messages = [{"role": "system", "content": SYSTEM}]
    for h in history[-8:]:
        messages.append(h)
    content = pregunta
    if estudiante_id:
        content += f"\n\nNota: El estudiante proporcionó su ID: {estudiante_id}"
    messages.append({"role": "user", "content": content})

    r = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {NVIDIA_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL, "messages": messages, "max_tokens": 512, "temperature": 0.5},
        timeout=60
    )
    return r.json()["choices"][0]["message"]["content"]

# ── UI ────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="CCD UNAB", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

logo_b64 = get_logo()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:58px; margin-bottom:8px; filter:brightness(0) invert(1);">' if logo_b64 else '<span style="font-family:Montserrat,sans-serif;font-size:1.8rem;font-weight:800;color:white;letter-spacing:-1px;">UNAB</span>'

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Open+Sans:wght@400;500;600&display=swap');
* {{ font-family: 'Open Sans', sans-serif; }}
[data-testid="stAppViewContainer"] {{ background: #f0f0f0; }}
[data-testid="stSidebar"] {{ display: none; }}
.block-container {{ max-width: 740px; padding-top: 0 !important; padding-bottom: 5rem; }}

.unab-header {{
    background: #F47920;
    padding: 24px 28px 20px;
    border-radius: 0 0 24px 24px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 6px 24px rgba(244,121,32,0.35);
}}
.unab-header h1 {{
    font-family: 'Montserrat', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    color: white;
    margin: 6px 0 3px;
    letter-spacing: -0.3px;
}}
.unab-header p {{
    color: rgba(255,255,255,0.88);
    font-size: 0.82rem;
    margin: 0;
}}

.info-cards {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 18px;
}}

.info-card {{
    background: white;
    border-radius: 14px;
    padding: 14px 12px;
    text-align: center;
    border-top: 3px solid #F47920;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}}

.info-card .ic-val {{
    font-family: 'Montserrat', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #F47920;
    margin-bottom: 3px;
}}

.info-card .ic-label {{
    font-size: 0.72rem;
    color: #888;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}}

.id-section {{
    background: white;
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 16px;
    border: 1.5px solid #ffe0c8;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.id-icon {{ font-size: 1.2rem; }}
.id-label {{ font-size: 0.8rem; color: #888; font-weight: 500; text-transform: uppercase; letter-spacing: 0.4px; margin-bottom: 3px; }}

div[data-testid="stTextInput"] input {{
    border: 1.5px solid #e8e8e8 !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
    background: #fafafa !important;
    padding: 9px 14px !important;
}}
div[data-testid="stTextInput"] input:focus {{
    border-color: #F47920 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(244,121,32,0.1) !important;
}}

[data-testid="stChatMessage"] {{
    border-radius: 16px !important;
}}

[data-testid="stChatInput"] textarea {{
    border-radius: 16px !important;
    border: 1.5px solid #e0e0e0 !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: #F47920 !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>

<div class="unab-header">
    {logo_html}
    <h1>Centro de Competencias Digitales</h1>
    <p>Universidad Autónoma de Bucaramanga · Asistente Virtual CCD</p>
</div>

<div class="info-cards">
    <div class="info-card">
        <div class="ic-val">$374.000</div>
        <div class="ic-label">Valor ruta</div>
    </div>
    <div class="info-card">
        <div class="ic-val">48 horas</div>
        <div class="ic-label">Duración</div>
    </div>
    <div class="info-card">
        <div class="ic-val">10 marzo</div>
        <div class="ic-label">Inscripciones</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="id-label">🎓 ID de estudiante (opcional)</p>', unsafe_allow_html=True)
estudiante_id = st.text_input(
    "id", label_visibility="collapsed",
    placeholder="Ej: 20230004 — ingrésalo para personalizar tu consulta",
    key="eid"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.history = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "¡Hola! 👋 Soy el asistente del **CCD de la UNAB**. Estoy aquí para ayudarte con todo sobre la ruta de Competencias Digitales: cursos, inscripciones, precios, insignia y más.\n\n¿En qué te puedo ayudar hoy?"
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Pregúntame sobre el CCD...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            try:
                answer = call_nvidia(prompt, estudiante_id or "", st.session_state.history)
            except Exception as e:
                answer = f"Lo siento, tuve un problema al conectarme. Por favor intenta de nuevo."
        st.markdown(answer)

    st.session_state.history.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "assistant", "content": answer})
    st.session_state.messages.append({"role": "assistant", "content": answer})