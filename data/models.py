"""
models.py — define el schema SQLite e inicializa la base de datos.
Solo crea tablas. No inserta ni consulta datos.
"""

import sqlite3
from config import DB_PATH


def init_db() -> None:
    """
    Crea las tablas necesarias si no existen.
    Inputs: ninguno.
    Outputs: ninguno.
    Errores: RuntimeError si no puede escribir en DB_PATH.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS proyectos (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre              TEXT    NOT NULL,
                descripcion         TEXT    NOT NULL,
                sector              TEXT    NOT NULL,
                localidad           TEXT    NOT NULL,
                zona_vulnerable     INTEGER NOT NULL DEFAULT 0,
                presupuesto         TEXT    NOT NULL,
                tipo_apoyo_buscado  TEXT    NOT NULL,
                perfil_creador      TEXT    NOT NULL,
                contacto_nombre     TEXT    NOT NULL,
                contacto_email      TEXT    NOT NULL,
                estado              TEXT    NOT NULL DEFAULT 'activo',
                fecha_creacion      TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS actores (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre               TEXT    NOT NULL,
                organizacion         TEXT,
                perfil               TEXT    NOT NULL,
                sectores_interes     TEXT    NOT NULL,
                localidades_interes  TEXT,
                tipo_apoyo_ofrecido  TEXT    NOT NULL,
                email                TEXT    NOT NULL,
                fecha_registro       TEXT    NOT NULL
            );
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"No se pudo inicializar la base de datos: {e}")
