"""
nuevo_proyecto.py — formulario de registro de proyecto.
UI llama a validators (lógica pura) y luego a repository (data).
"""

import streamlit as st
from logic.validators import validar_proyecto
from data.repository import insertar_proyecto
from config import SECTORES, LOCALIDADES, PERFILES, TIPOS_APOYO, PRESUPUESTOS


def render() -> None:
    """Renderiza el formulario de registro de proyecto con validación."""
    st.markdown("## ➕ Registrar proyecto")
    st.caption("Los campos marcados con * son obligatorios.")

    with st.form("form_proyecto", clear_on_submit=True):
        nombre = st.text_input("Nombre del proyecto *")
        descripcion = st.text_area("Descripción breve *", height=100)

        col1, col2 = st.columns(2)
        with col1:
            sector = st.selectbox("Sector principal *", SECTORES)
            localidad = st.selectbox("Localidad *", LOCALIDADES)
        with col2:
            presupuesto = st.selectbox("Presupuesto estimado *", PRESUPUESTOS)
            tipo_apoyo = st.selectbox("Tipo de apoyo buscado *", TIPOS_APOYO)

        zona_vulnerable = st.checkbox(
            "¿El proyecto está en zona de alta vulnerabilidad?"
        )
        perfil_creador = st.selectbox("Tu perfil *", PERFILES)

        col3, col4 = st.columns(2)
        with col3:
            contacto_nombre = st.text_input("Tu nombre *")
        with col4:
            contacto_email = st.text_input("Tu email *")

        enviado = st.form_submit_button(
            "Registrar proyecto", use_container_width=True
        )

    if not enviado:
        return

    datos = {
        "nombre": nombre,
        "descripcion": descripcion,
        "sector": sector,
        "localidad": localidad,
        "zona_vulnerable": int(zona_vulnerable),
        "presupuesto": presupuesto,
        "tipo_apoyo_buscado": tipo_apoyo,
        "perfil_creador": perfil_creador,
        "contacto_nombre": contacto_nombre,
        "contacto_email": contacto_email,
    }

    errores = validar_proyecto(datos)
    if errores:
        for error in errores:
            st.error(error)
        return

    try:
        insertar_proyecto(datos)
        st.success(f"✅ Proyecto **{nombre}** registrado correctamente.")
        st.balloons()
    except RuntimeError as e:
        st.error(str(e))
