# chat.py
import streamlit as st
from anthropic import Anthropic
from data_loader import get_contexto_datos
from database import save_chat, load_chat

@st.cache_resource
def get_claude_client():
    return Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def generar_respuesta_stream(messages):
    client = get_claude_client()
    contexto = get_contexto_datos()

    system_prompt = f"""
    Eres San FelipIA, guía turístico experto, amable y entusiasta del Distrito Creativo San Felipe en Bogotá.

    **Datos actualizados de los establecimientos:**
    {contexto}

    Reglas importantes:
    - El usuario puede escribir en cualquier idioma (español, inglés, francés, portugués, etc.).
    - Detecta automáticamente el idioma del mensaje del usuario y responde siempre en el mismo idioma.
    - Sé cercano, claro y útil.
    - Recomienda rutas realistas según perfil, presupuesto y preferencias.
    - **NO uses emojis de banderas** (🇵🇪, 🇨🇴, 🇺🇸, etc.).
    """

    try:
        with client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            temperature=0.7,
            system=system_prompt,
            messages=messages
        ) as stream:
            texto_completo = ""
            placeholder = st.empty()
            
            for delta in stream.text_stream:
                texto_completo += delta
                placeholder.markdown(texto_completo + "▌")
            
            placeholder.markdown(texto_completo)
            return texto_completo

    except Exception as e:
        return f"Lo siento, ocurrió un error técnico: {str(e)}"


def reiniciar_chat():
    if "messages" in st.session_state:
        del st.session_state.messages
    if "user_id" in st.session_state:
        save_chat(st.session_state.user_id, [])
    st.rerun()


def mostrar_chat_sanfelipia():
    st.subheader("💬 San FelipIA - Planificador de Rutas")
    st.caption("Multilingüe • Puedes escribir en cualquier idioma")

    if "user_id" not in st.session_state:
        st.session_state.user_id = "hackathon_user"

    # Mensaje inicial
    if "messages" not in st.session_state:
        historial = load_chat(st.session_state.user_id)
        if historial:
            st.session_state.messages = historial
        else:
            st.session_state.messages = [
                {"role": "assistant", "content": """¡Hola! 🌟 Soy **San FelipIA**, tu guía inteligente del Distrito Creativo San Felipe.

Puedes escribirme **en cualquier idioma** (español, inglés, francés, portugués, etc.) y yo te responderé en el mismo idioma.

¿En qué te ayudo hoy? Cuéntame qué tipo de plan buscas (en pareja, familiar, amigos, solo), tu presupuesto aproximado o tus preferencias."""}
            ]

    # Mostrar historial
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input del usuario
    if prompt := st.chat_input("Escribe tu mensaje aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            respuesta = generar_respuesta_stream(st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        save_chat(st.session_state.user_id, st.session_state.messages)
        st.rerun()

    # Botón de reinicio
    st.markdown("---")
    col1, col2, col3 = st.columns([3, 2, 3])
    with col2:
        if st.button("🔄 Reiniciar Conversación", 
                     type="secondary", 
                     use_container_width=True,
                     help="Borra el historial y comienza una nueva conversación"):
            reiniciar_chat()