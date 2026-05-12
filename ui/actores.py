"""
actores.py — directorio de actores con filtros.
Solo UI. Sin lógica de negocio.
"""

import streamlit as st
from data.repository import obtener_actores
from config import PERFILES, SECTORES


def render() -> None:
    """Renderiza el directorio de actores con filtros por perfil y sector."""
    st.markdown("## 🤝 Actores del ecosistema")

    col1, col2 = st.columns(2)
    with col1:
        perfil = st.selectbox("Perfil", ["Todos"] + PERFILES)
    with col2:
        sector = st.selectbox("Sector de interés", ["Todos"] + SECTORES)

    try:
        df = obtener_actores(perfil, sector)
    except RuntimeError as e:
        st.error(str(e))
        return

    if df.empty:
        st.warning("No hay actores con esos filtros.")
        return

    st.markdown(f"**{len(df)} actor(es) encontrado(s)**")

    for _, fila in df.iterrows():
        st.markdown(f"""
        <div class="card">
            <h3>{fila['nombre']} · <small>{fila['perfil']}</small></h3>
            <p>{fila['organizacion'] or '—'}</p>
            <span class="tag">{fila['tipo_apoyo_ofrecido']}</span>
            <span class="tag">{fila['sectores_interes']}</span>
            <br><small style="color:#999">{fila['email']}</small>
        </div>
        """, unsafe_allow_html=True)
