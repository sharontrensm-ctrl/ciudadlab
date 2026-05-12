"""
nuevo_actor.py — formulario de registro de actor.
UI llama a validators y luego a repository.
"""

import streamlit as st
from logic.validators import validar_actor
from data.repository import insertar_actor
from config import PERFILES, SECTORES, LOCALIDADES, TIPOS_APOYO


def render() -> None:
    """Renderiza el formulario de registro de actor con validación."""
    st.markdown("## ➕ Registrar actor")
    st.caption("Los campos marcados con * son obligatorios.")

    with st.form("form_actor", clear_on_submit=True):
        nombre = st.text_input("Nombre completo *")
        organizacion = st.text_input("Organización o institución")

        col1, col2 = st.columns(2)
        with col1:
            perfil = st.selectbox("Tu perfil *", PERFILES)
            tipo_apoyo = st.selectbox("¿Qué apoyo puedes ofrecer? *", TIPOS_APOYO)
        with col2:
            sectores = st.multiselect("Sectores de interés *", SECTORES)
            localidades = st.multiselect("Localidades de interés", LOCALIDADES)

        email = st.text_input("Email de contacto *")

        enviado = st.form_submit_button(
            "Registrar actor", use_container_width=True
        )

    if not enviado:
        return

    datos = {
        "nombre": nombre,
        "organizacion": organizacion or "",
        "perfil": perfil,
        "sectores_interes": ", ".join(sectores),
        "localidades_interes": ", ".join(localidades),
        "tipo_apoyo_ofrecido": tipo_apoyo,
        "email": email,
    }

    errores = validar_actor(datos)
    if errores:
        for error in errores:
            st.error(error)
        return

    try:
        insertar_actor(datos)
        st.success(f"✅ Actor **{nombre}** registrado correctamente.")
    except RuntimeError as e:
        st.error(str(e))
