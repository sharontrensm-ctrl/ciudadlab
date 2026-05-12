"""
proyectos.py — listado de proyectos con filtros.
Solo UI. Sin lógica de negocio.
"""

import streamlit as st
from data.repository import obtener_proyectos
from config import SECTORES, LOCALIDADES


def render() -> None:
    """Renderiza el listado de proyectos con filtros por sector, localidad y vulnerabilidad."""
    st.markdown("## 📋 Proyectos registrados")

    col1, col2, col3 = st.columns(3)
    with col1:
        sector = st.selectbox("Sector", ["Todos"] + SECTORES)
    with col2:
        localidad = st.selectbox("Localidad", ["Todas"] + LOCALIDADES)
    with col3:
        solo_vulnerables = st.checkbox("Solo zonas vulnerables")

    try:
        df = obtener_proyectos(sector, localidad, solo_vulnerables)
    except RuntimeError as e:
        st.error(str(e))
        return

    if df.empty:
        st.warning("No hay proyectos con esos filtros.")
        return

    st.markdown(f"**{len(df)} proyecto(s) encontrado(s)**")

    for _, fila in df.iterrows():
        vuln = (
            '<span class="tag tag-vulnerable">⚠ ZONA VULNERABLE</span>'
            if fila["zona_vulnerable"]
            else ""
        )
        st.markdown(f"""
        <div class="card">
            <h3>{fila['nombre']}</h3>
            <p>{fila['descripcion']}</p>
            <span class="tag">{fila['sector']}</span>
            <span class="tag">{fila['localidad']}</span>
            <span class="tag">{fila['tipo_apoyo_buscado']}</span>
            {vuln}
            <br><small style="color:#999">
                Contacto: {fila['contacto_nombre']} · {fila['contacto_email']}
            </small>
        </div>
        """, unsafe_allow_html=True)
