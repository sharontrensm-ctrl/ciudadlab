"""
inicio.py — página de bienvenida con métricas y últimas entradas.
Solo UI. Llama a repository para leer datos. Sin lógica de negocio.
"""

import streamlit as st
from data.repository import obtener_proyectos, obtener_actores


def render() -> None:
    """Renderiza la página de inicio con métricas y últimas entradas."""
    st.markdown("""
    <div class="header-band">
        <h1>Quito Ciudad Lab</h1>
        <p>Conectando actores para construir ciudad — desde la mitad del mundo.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        df_proyectos = obtener_proyectos()
        df_actores = obtener_actores()
    except RuntimeError as e:
        st.error(str(e))
        return

    total_proyectos = len(df_proyectos)
    total_actores = len(df_actores)
    total_vulnerables = (
        int(df_proyectos["zona_vulnerable"].sum())
        if not df_proyectos.empty
        else 0
    )

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="num">{total_proyectos}</div>
            <div class="lbl">Proyectos activos</div>
        </div>
        <div class="metric-box">
            <div class="num">{total_actores}</div>
            <div class="lbl">Actores registrados</div>
        </div>
        <div class="metric-box">
            <div class="num">{total_vulnerables}</div>
            <div class="lbl">Zonas vulnerables</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown("#### Últimos proyectos")
        if df_proyectos.empty:
            st.info("Aún no hay proyectos. ¡Registra el primero!")
        else:
            for _, fila in df_proyectos.head(3).iterrows():
                _tarjeta_proyecto(fila)

    with col_der:
        st.markdown("#### Últimos actores")
        if df_actores.empty:
            st.info("Aún no hay actores. ¡Regístrate!")
        else:
            for _, fila in df_actores.head(3).iterrows():
                _tarjeta_actor(fila)


def _tarjeta_proyecto(fila) -> None:
    """Renderiza una tarjeta resumida de proyecto."""
    vuln = (
        '<span class="tag tag-vulnerable">⚠ ZONA VULNERABLE</span>'
        if fila["zona_vulnerable"]
        else ""
    )
    descripcion_corta = str(fila["descripcion"])[:100] + "…"
    st.markdown(f"""
    <div class="card">
        <h3>{fila['nombre']}</h3>
        <p>{descripcion_corta}</p>
        <span class="tag">{fila['sector']}</span>
        <span class="tag">{fila['localidad']}</span>
        {vuln}
    </div>
    """, unsafe_allow_html=True)


def _tarjeta_actor(fila) -> None:
    """Renderiza una tarjeta resumida de actor."""
    st.markdown(f"""
    <div class="card">
        <h3>{fila['nombre']} · <small>{fila['perfil']}</small></h3>
        <p>{fila['organizacion'] or '—'}</p>
        <span class="tag">{fila['tipo_apoyo_ofrecido']}</span>
    </div>
    """, unsafe_allow_html=True)
