"""
repository.py — todas las operaciones de lectura y escritura a SQLite.
Ningún otro módulo toca la base de datos directamente.
"""

import sqlite3
from datetime import datetime
from typing import Optional
import pandas as pd
from config import DB_PATH, ESTADO_ACTIVO


def _connect() -> sqlite3.Connection:
    """Abre y devuelve una conexión SQLite."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ── Proyectos ────────────────────────────────────────────────────────────────

def insertar_proyecto(datos: dict) -> None:
    """
    Inserta un proyecto nuevo en la base de datos.
    Inputs: datos — dict con claves definidas en models.proyectos.
    Outputs: ninguno.
    Errores: RuntimeError si falla la escritura.
    """
    try:
        conn = _connect()
        conn.execute("""
            INSERT INTO proyectos
                (nombre, descripcion, sector, localidad, zona_vulnerable,
                 presupuesto, tipo_apoyo_buscado, perfil_creador,
                 contacto_nombre, contacto_email, fecha_creacion)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            datos["nombre"], datos["descripcion"], datos["sector"],
            datos["localidad"], datos["zona_vulnerable"],
            datos["presupuesto"], datos["tipo_apoyo_buscado"],
            datos["perfil_creador"], datos["contacto_nombre"],
            datos["contacto_email"], datetime.now().isoformat(),
        ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error al guardar proyecto: {e}")


def obtener_proyectos(
    sector: Optional[str] = None,
    localidad: Optional[str] = None,
    solo_vulnerables: bool = False,
) -> pd.DataFrame:
    """
    Devuelve proyectos activos con filtros opcionales.
    Inputs: sector, localidad — strings o None; solo_vulnerables — bool.
    Outputs: DataFrame con columnas de la tabla proyectos.
    Errores: RuntimeError si falla la consulta.
    """
    try:
        conn = _connect()
        query = "SELECT * FROM proyectos WHERE estado = ?"
        params: list = [ESTADO_ACTIVO]

        if sector and sector != "Todos":
            query += " AND sector = ?"
            params.append(sector)
        if localidad and localidad != "Todas":
            query += " AND localidad = ?"
            params.append(localidad)
        if solo_vulnerables:
            query += " AND zona_vulnerable = 1"

        query += " ORDER BY fecha_creacion DESC"
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener proyectos: {e}")


def obtener_proyecto_por_id(proyecto_id: int) -> Optional[dict]:
    """
    Devuelve un proyecto como dict, o None si no existe.
    Inputs: proyecto_id — entero.
    Outputs: dict con columnas del proyecto o None.
    Errores: RuntimeError si falla la consulta.
    """
    try:
        conn = _connect()
        cursor = conn.execute(
            "SELECT * FROM proyectos WHERE id = ?", (proyecto_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    except sqlite3.Error as e:
        raise RuntimeError(f"Error al obtener proyecto {proyecto_id}: {e}")


# ── Actores ──────────────────────────────────────────────────────────────────

def insertar_actor(datos: dict) -> None:
    """
    Inserta un actor nuevo en la base de datos.
    Inputs: datos — dict con claves definidas en models.actores.
    Outputs: ninguno.
    Errores: RuntimeError si falla la escritura.
    """
    try:
        conn = _connect()
        conn.execute("""
            INSERT INTO actores
                (nombre, organizacion, perfil, sectores_interes,
                 localidades_interes, tipo_apoyo_ofrecido, email, fecha_registro)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            datos["nombre"], datos["organizacion"], datos["perfil"],
            datos["sectores_interes"], datos["localidades_interes"],
            datos["tipo_apoyo_ofrecido"], datos["email"],
            datetime.now().isoformat(),
        ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"Error al guardar actor: {e}")


def obtener_actores(
    perfil: Optional[str] = None,
    sector: Optional[str] = None,
) -> pd.DataFrame:
    """
    Devuelve actores con filtros opcionales.
    Inputs: perfil, sector — strings o None.
    Outputs: DataFrame con columnas de la tabla actores.
    Errores: RuntimeError si falla la consulta.
    """
    try:
        conn = _connect()
        query = "SELECT * FROM actores WHERE 1=1"
        params: list = []

        if perfil and perfil != "Todos":
            query += " AND perfil = ?"
            params.append(perfil)
        if sector and sector != "Todos":
            query += " AND sectores_interes LIKE ?"
            params.append(f"%{sector}%")

        query += " ORDER BY fecha_registro DESC"
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener actores: {e}")


def obtener_todos_actores() -> pd.DataFrame:
    """
    Devuelve todos los actores sin filtro. Usado por el motor de matching.
    Outputs: DataFrame completo de actores.
    Errores: RuntimeError si falla la consulta.
    """
    try:
        conn = _connect()
        df = pd.read_sql_query(
            "SELECT * FROM actores ORDER BY fecha_registro DESC", conn
        )
        conn.close()
        return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener actores para matching: {e}")
