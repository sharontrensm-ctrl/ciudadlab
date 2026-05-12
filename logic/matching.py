"""
matching.py — motor puro de matching entre proyectos y actores.
Sin I/O. Sin Streamlit. Sin base de datos.
Recibe DataFrames, devuelve DataFrame filtrado.
"""

import pandas as pd


def calcular_matches(proyecto: dict, actores: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra actores que pueden apoyar un proyecto dado.
    Criterios: tipo_apoyo_ofrecido coincide con tipo_apoyo_buscado,
               O sectores_interes contiene el sector del proyecto.
    Inputs:
        proyecto — dict con claves 'tipo_apoyo_buscado' y 'sector'.
        actores  — DataFrame completo de actores.
    Outputs: DataFrame de actores con al menos un criterio de match.
    Errores: ValueError si faltan claves en proyecto.
    """
    tipo_buscado = proyecto.get("tipo_apoyo_buscado")
    sector = proyecto.get("sector")

    if not tipo_buscado or not sector:
        raise ValueError(
            "El proyecto debe tener 'tipo_apoyo_buscado' y 'sector' definidos."
        )

    if actores.empty:
        return pd.DataFrame()

    match_por_apoyo = actores["tipo_apoyo_ofrecido"].str.contains(
        tipo_buscado, case=False, na=False
    )
    match_por_sector = actores["sectores_interes"].str.contains(
        sector, case=False, na=False
    )

    matches = actores[match_por_apoyo | match_por_sector].copy()
    return matches.reset_index(drop=True)


def puntaje_match(proyecto: dict, actor: dict) -> int:
    """
    Calcula un puntaje de afinidad entre 0 y 2.
    0 = sin match · 1 = un criterio · 2 = ambos criterios.
    Inputs: proyecto y actor como dicts.
    Outputs: entero 0-2.
    """
    puntaje = 0

    tipo_buscado = proyecto.get("tipo_apoyo_buscado", "")
    sector = proyecto.get("sector", "")
    tipo_ofrecido = actor.get("tipo_apoyo_ofrecido", "")
    sectores_actor = actor.get("sectores_interes", "")

    if tipo_buscado.lower() in tipo_ofrecido.lower():
        puntaje += 1
    if sector.lower() in sectores_actor.lower():
        puntaje += 1

    return puntaje
