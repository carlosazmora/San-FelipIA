# catalogo.py
import streamlit as st
import pandas as pd
from data_loader import get_places_df

def mostrar_catalogo():
    st.subheader("🗂️ Catálogo de Establecimientos - San Felipe")
    st.caption("65 lugares • Distrito Creativo San Felipe")
    
    df = get_places_df()
    if df.empty:
        st.error("No se pudieron cargar los datos del Excel")
        return

    # Filtros
    col1, col2 = st.columns([3, 1])
    with col1:
        busqueda = st.text_input("🔎 Buscar por nombre, tipo, plan o dirección", "")
    with col2:
        categoria = st.selectbox(
            "Categoría", 
            ["Todas"] + sorted(df['Categoría'].dropna().unique().tolist())
        )

    # Filtrado
    df_filtrado = df.copy()
    
    if busqueda:
        mask = df_filtrado.apply(
            lambda x: busqueda.lower() in str(x).lower(), axis=1
        )
        df_filtrado = df_filtrado[mask]
    
    if categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria]

    st.write(f"**{len(df_filtrado)} establecimientos encontrados**")

    # Mostrar cada establecimiento como expander con imagen
    for _, row in df_filtrado.iterrows():
        nombre = row.get('Nombre', 'Sin nombre')
        categoria_row = row.get('Categoría', '')
        
        with st.expander(f"**{nombre}** • {categoria_row}"):
            col_img, col_info = st.columns([1, 3])
            
            with col_img:
                # Mostrar imagen desde URL (columna 'Link imagen principal')
                link_imagen = row.get('Link imagen principal')
                if pd.notna(link_imagen) and str(link_imagen).strip() != "":
                    try:
                        st.image(str(link_imagen).strip(), width=120)
                    except:
                        st.markdown("🖼️")
                else:
                    st.markdown("🖼️")
            
            with col_info:
                st.write(f"**Tipo:** {row.get('Tipo de establecimiento', '')}")
                st.write(f"**Dirección:** {row.get('Dirección', 'Sin información')}")
                st.write(f"**Perfil ideal:** {row.get('Perfil ideal', '')}")
                
                costo = row.get('costo', row.get('Costo promedio estimado por persona (COP)', 0))
                st.write(f"**Costo aproximado:** ${float(costo):,.0f} COP por persona")
                
                st.write(f"**Plan sugerido:** {row.get('Plan sugerido', '')}")

    if len(df_filtrado) == 0:
        st.warning("No se encontraron resultados con los filtros aplicados.")