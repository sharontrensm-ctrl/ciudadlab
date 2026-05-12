"""
matching_ui.py — interfaz del motor de matching.
UI llama a repository para datos y a logic.matching para el cálculo.
"""

import streamlit as st
from data.repository import obtener_proyectos, obtener_todos_actores
from logic.matching import calcular_matches, puntaje_match


def render() -> None:
    """Renderiza la página de matching proyecto–actores."""
    st.markdown("## 🔗 Motor de matching")
    st.caption(
        "Selecciona un proyecto para encontrar actores que pueden apoyarlo."
    )

    try:
        df_proyectos = obtener_proyectos()
    except RuntimeError as e:
        st.error(str(e))
        return

    if df_proyectos.empty:
        st.warning("Primero registra al menos un proyecto.")
        return

    opciones = {
        f"{fila['nombre']} ({fila['sector']})": fila["id"]
        for _, fila in df_proyectos.iterrows()
    }
    seleccion = st.selectbox("Selecciona proyecto", list(opciones.keys()))
    proyecto_id = opciones[seleccion]

    if not st.button("🔍 Buscar matches", use_container_width=True):
        return

    try:
        fila_proyecto = df_proyectos[
            df_proyectos["id"] == proyecto_id
        ].iloc[0].to_dict()
        df_actores = obtener_todos_actores()
    except RuntimeError as e:
        st.error(str(e))
        return

    try:
        matches = calcular_matches(fila_proyecto, df_actores)
    except ValueError as e:
        st.error(str(e))
        return

    if matches.empty:
        st.info(
            "No se encontraron actores con match directo. "
            "Registra más actores para ampliar el ecosistema."
        )
        return

    matches["puntaje"] = matches.apply(
        lambda fila: puntaje_match(fila_proyecto, fila.to_dict()), axis=1
    )
    matches = matches.sort_values("puntaje", ascending=False)

    st.success(f"✅ {len(matches)} actor(es) con potencial de colaboración")

    for _, fila in matches.iterrows():
        estrellas = "★" * int(fila["puntaje"]) + "☆" * (2 - int(fila["puntaje"]))
        st.markdown(f"""
        <div class="match-card">
            <strong>{fila['nombre']}</strong> · {fila['perfil']}
            &nbsp;<span style="color:#E8A100">{estrellas}</span><br>
            <span style="color:#27AE60">▶ {fila['tipo_apoyo_ofrecido']}</span>
            &nbsp;·&nbsp; {fila['organizacion'] or '—'}<br>
            <small>{fila['email']}</small>
        </div>
        """, unsafe_allow_html=True)
