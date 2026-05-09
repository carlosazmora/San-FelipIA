# app.py
import streamlit as st
from catalogo import mostrar_catalogo
from chat import mostrar_chat_sanfelipia
from data_loader import get_places_df

# ===================== CONFIGURACIÓN =====================
st.set_page_config(
    page_title="San FelipIA",
    page_icon="⭐",
    layout="wide"
)

# ===================== SIDEBAR =====================
st.sidebar.title("🧭 San FelipIA")
st.sidebar.markdown("**Planificador Inteligente**  \nDistrito Creativo San Felipe")

seccion = st.sidebar.radio("Ir a:", [
    "🏠 Inicio",
    "💬 Chat Planificador",
    "🗂️ Catálogo Completo"
])

# ===================== CONTENIDO =====================
if seccion == "🏠 Inicio":
    st.title("⭐ Bienvenido a San FelipIA")
    st.header("Tu asistente inteligente para descubrir San Felipe")
    
    # Métricas rápidas
    df = get_places_df()
    total = len(df)
    
    # Contar centros de entretenimiento
    entretenimiento = len(df[df['Categoría'].str.contains("Entretenimiento", na=False)])
    galerias = len(df[df['Categoría'].str.contains("Galer", na=False)])
    restaurantes = len(df[df['Categoría'].str.contains("Donde Comer", na=False)])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Establecimientos Totales", f"{total}")
    col2.metric("🎵 Centros de Entretenimiento", f"{entretenimiento}")
    col3.metric("🎨 Galerías y Talleres", f"{galerias}")
    col4.metric("🍽️ Donde Comer", f"{restaurantes}")

    st.info("""
    **Cómo usar San FelipIA:**
    - Ve a **Chat Planificador** → Cuéntale tus preferencias (idioma, perfil, presupuesto...)
    - Explora el **Catálogo Completo**
    """)

elif seccion == "💬 Chat Planificador":
    mostrar_chat_sanfelipia()

elif seccion == "🗂️ Catálogo Completo":
    mostrar_catalogo()

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("San FelipIA v3 • Social Skin / UniMilitar, 2026-1")