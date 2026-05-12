"""
validators.py — funciones puras de validación de inputs.
Sin I/O. Sin Streamlit. Sin base de datos.
Devuelven listas de errores (vacía = válido).
"""

from config import MAX_NOMBRE, MAX_DESCRIPCION


def validar_proyecto(datos: dict) -> list[str]:
    """
    Valida los campos de un formulario de proyecto.
    Inputs: datos — dict con campos del formulario.
    Outputs: lista de strings con mensajes de error (vacía si todo es válido).
    """
    errores = []

    nombre = datos.get("nombre", "").strip()
    if not nombre:
        errores.append("El nombre del proyecto es obligatorio.")
    elif len(nombre) > MAX_NOMBRE:
        errores.append(f"El nombre no puede superar {MAX_NOMBRE} caracteres.")

    descripcion = datos.get("descripcion", "").strip()
    if not descripcion:
        errores.append("La descripción es obligatoria.")
    elif len(descripcion) > MAX_DESCRIPCION:
        errores.append(f"La descripción no puede superar {MAX_DESCRIPCION} caracteres.")

    if not datos.get("contacto_nombre", "").strip():
        errores.append("El nombre de contacto es obligatorio.")

    email = datos.get("contacto_email", "").strip()
    if not email:
        errores.append("El email de contacto es obligatorio.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El email no tiene un formato válido.")

    return errores


def validar_actor(datos: dict) -> list[str]:
    """
    Valida los campos de un formulario de actor.
    Inputs: datos — dict con campos del formulario.
    Outputs: lista de strings con mensajes de error (vacía si todo es válido).
    """
    errores = []

    if not datos.get("nombre", "").strip():
        errores.append("El nombre es obligatorio.")

    if not datos.get("sectores_interes"):
        errores.append("Selecciona al menos un sector de interés.")

    email = datos.get("email", "").strip()
    if not email:
        errores.append("El email es obligatorio.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El email no tiene un formato válido.")

    return errores
