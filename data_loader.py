# datos.py
import streamlit as st

import pandas as pd
import os

@st.cache_data
def cargar_establecimientos():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                       "establecimientos_san_felipe_pet_friendly_imagenes.xlsx")
    
    if not os.path.exists(ruta):
        st.error("❌ No se encontró el archivo Excel")
        return pd.DataFrame()
    
    df = pd.read_excel(ruta, sheet_name="Establecimientos")
    
    # Limpiar nombres de columnas
    df.columns = [col.strip() for col in df.columns]
    
    # Convertir costo a numérico
    if 'Costo promedio estimado por persona (COP)' in df.columns:
        df['costo'] = pd.to_numeric(df['Costo promedio estimado por persona (COP)'], errors='coerce').fillna(15000)
    else:
        df['costo'] = 15000
    
    return df

def get_places_df():
    return cargar_establecimientos()

def get_contexto_datos():
    """Devuelve texto para Claude"""
    df = get_places_df()
    return df.to_string(index=False)

def buscar_lugares(texto: str, max_results=10):
    """Búsqueda simple para rutas"""
    df = get_places_df()
    if df.empty:
        return pd.DataFrame()
    
    texto = texto.lower()
    mask = (
        df['Nombre'].astype(str).str.lower().str.contains(texto, na=False) |
        df['Categoría'].astype(str).str.lower().str.contains(texto, na=False) |
        df['Tipo de establecimiento'].astype(str).str.lower().str.contains(texto, na=False) |
        df['Plan sugerido'].astype(str).str.lower().str.contains(texto, na=False)
    )
    return df[mask].head(max_results)