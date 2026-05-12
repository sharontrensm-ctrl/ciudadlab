import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# ── Config ──────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quito Ciudad Lab",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DB helpers ───────────────────────────────────────────────────────────────
DB = "ciudad_lab.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            sector TEXT,
            localidad TEXT,
            zona_vulnerabilidad INTEGER DEFAULT 0,
            presupuesto_estimado TEXT,
            tipo_apoyo_buscado TEXT,
            contacto_nombre TEXT,
            contacto_email TEXT,
            perfil_creador TEXT,
            estado TEXT DEFAULT 'activo',
            fecha_creacion TEXT
        );

        CREATE TABLE IF NOT EXISTS actores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            organizacion TEXT,
            perfil TEXT,
            sectores_interes TEXT,
            localidades_interes TEXT,
            tipo_apoyo_ofrecido TEXT,
            email TEXT,
            fecha_registro TEXT
        );
    """)
    conn.commit()
    conn.close()

def insertar_proyecto(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT INTO proyectos
        (nombre, descripcion, sector, localidad, zona_vulnerabilidad,
         presupuesto_estimado, tipo_apoyo_buscado, contacto_nombre,
         contacto_email, perfil_creador, fecha_creacion)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data["nombre"], data["descripcion"], data["sector"],
        data["localidad"], data["zona_vulnerabilidad"],
        data["presupuesto_estimado"], data["tipo_apoyo_buscado"],
        data["contacto_nombre"], data["contacto_email"],
        data["perfil_creador"], datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def insertar_actor(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT INTO actores
        (nombre, organizacion, perfil, sectores_interes,
         localidades_interes, tipo_apoyo_ofrecido, email, fecha_registro)
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        data["nombre"], data["organizacion"], data["perfil"],
        data["sectores_interes"], data["localidades_interes"],
        data["tipo_apoyo_ofrecido"], data["email"],
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_proyectos(sector=None, localidad=None, solo_vulnerables=False):
    conn = get_conn()
    q = "SELECT * FROM proyectos WHERE estado='activo'"
    params = []
    if sector and sector != "Todos":
        q += " AND sector=?"
        params.append(sector)
    if localidad and localidad != "Todas":
        q += " AND localidad=?"
        params.append(localidad)
    if solo_vulnerables:
        q += " AND zona_vulnerabilidad=1"
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df

def get_actores(perfil=None, sector=None):
    conn = get_conn()
    q = "SELECT * FROM actores WHERE 1=1"
    params = []
    if perfil and perfil != "Todos":
        q += " AND perfil=?"
        params.append(perfil)
    if sector and sector != "Todos":
        q += " AND sectores_interes LIKE ?"
        params.append(f"%{sector}%")
    df = pd.read_sql_query(q, conn, params=params)
    conn.close()
    return df

def matching(proyecto_id: int):
    """Devuelve actores cuyo tipo_apoyo_ofrecido coincide con tipo_apoyo_buscado del proyecto."""
    conn = get_conn()
    proyecto = pd.read_sql_query(
        "SELECT * FROM proyectos WHERE id=?", conn, params=[proyecto_id]
    )
    if proyecto.empty:
        conn.close()
        return pd.DataFrame()
    apoyo = proyecto.iloc[0]["tipo_apoyo_buscado"]
    sector = proyecto.iloc[0]["sector"]
    actores = pd.read_sql_query("""
        SELECT * FROM actores
        WHERE tipo_apoyo_ofrecido LIKE ?
           OR sectores_interes LIKE ?
    """, conn, params=[f"%{apoyo}%", f"%{sector}%"])
    conn.close()
    return actores

# ── Constantes ───────────────────────────────────────────────────────────────
SECTORES = [
    "Movilidad urbana", "Seguridad ciudadana", "Medio ambiente",
    "Vivienda", "Espacio público", "Educación", "Salud",
    "Cultura y patrimonio", "Economía local", "Otro"
]
LOCALIDADES = [
    "Norte", "Centro histórico", "Sur", "Valle de los Chillos",
    "Tumbaco", "Calderón", "La Delicia", "Otro"
]
PERFILES = ["Ciudadano/a", "Sociedad civil", "Academia", "Sector privado", "Gobierno"]
TIPOS_APOYO = ["Financiamiento", "Co-ejecución", "Expertise técnico", "Redes / conexiones", "Visibilidad"]

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}
code, pre, .mono { font-family: 'Space Mono', monospace; }

/* Header */
.header-band {
    background: #0B1F2E;
    padding: 2rem 2.5rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}
.header-band h1 {
    color: #E8FF4A;
    font-size: 2.4rem;
    font-weight: 800;
    margin: 0 0 .3rem 0;
    letter-spacing: -1px;
}
.header-band p {
    color: #8BAFC2;
    font-size: .95rem;
    margin: 0;
}

/* Cards */
.card {
    background: #F5F7F2;
    border-left: 4px solid #E8FF4A;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.card h3 { margin: 0 0 .4rem 0; color: #0B1F2E; font-size: 1.05rem; font-weight: 700; }
.card p  { margin: 0; color: #4A5568; font-size: .88rem; }
.tag {
    display: inline-block;
    background: #0B1F2E;
    color: #E8FF4A;
    font-size: .72rem;
    font-weight: 700;
    padding: .2rem .55rem;
    border-radius: 4px;
    margin: .3rem .2rem 0 0;
    font-family: 'Space Mono', monospace;
}
.tag-vulnerable { background: #C0392B; color: #fff; }

/* Metric strip */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-box {
    flex: 1;
    background: #0B1F2E;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    text-align: center;
}
.metric-box .num { color: #E8FF4A; font-size: 2rem; font-weight: 800; }
.metric-box .lbl { color: #8BAFC2; font-size: .78rem; margin-top: .2rem; }

/* Match result */
.match-card {
    background: #EAF9F1;
    border-left: 4px solid #27AE60;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: .8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Init ─────────────────────────────────────────────────────────────────────
init_db()

if "page" not in st.session_state:
    st.session_state.page = "inicio"

# ── Sidebar nav ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏙️ Ciudad Lab")
    st.markdown("---")
    opciones = {
        "🏠 Inicio": "inicio",
        "📋 Proyectos": "proyectos",
        "➕ Registrar proyecto": "nuevo_proyecto",
        "🤝 Actores": "actores",
        "➕ Registrar actor": "nuevo_actor",
        "🔗 Matching": "matching",
    }
    for label, key in opciones.items():
        if st.button(label, use_container_width=True):
            st.session_state.page = key

# ── PÁGINA: INICIO ────────────────────────────────────────────────────────────
if st.session_state.page == "inicio":
    st.markdown("""
    <div class="header-band">
        <h1>Quito Ciudad Lab</h1>
        <p>Territorio donde trabajo, vida y propósito se encuentran — conectando actores para construir ciudad.</p>
    </div>
    """, unsafe_allow_html=True)

    df_p = get_proyectos()
    df_a = get_actores()
    n_vuln = len(df_p[df_p["zona_vulnerabilidad"] == 1]) if not df_p.empty else 0

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box"><div class="num">{len(df_p)}</div><div class="lbl">Proyectos activos</div></div>
        <div class="metric-box"><div class="num">{len(df_a)}</div><div class="lbl">Actores registrados</div></div>
        <div class="metric-box"><div class="num">{n_vuln}</div><div class="lbl">Zonas vulnerables</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Últimos proyectos")
        if df_p.empty:
            st.info("Aún no hay proyectos. ¡Registra el primero!")
        else:
            for _, r in df_p.tail(3).iterrows():
                vuln_tag = '<span class="tag tag-vulnerable">⚠ ZONA VULNERABLE</span>' if r["zona_vulnerabilidad"] else ""
                st.markdown(f"""
                <div class="card">
                    <h3>{r['nombre']}</h3>
                    <p>{str(r['descripcion'])[:120]}…</p>
                    <span class="tag">{r['sector']}</span>
                    <span class="tag">{r['localidad']}</span>
                    {vuln_tag}
                </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### Últimos actores")
        if df_a.empty:
            st.info("Aún no hay actores. ¡Regístrate!")
        else:
            for _, r in df_a.tail(3).iterrows():
                st.markdown(f"""
                <div class="card">
                    <h3>{r['nombre']} · <small>{r['perfil']}</small></h3>
                    <p>{r['organizacion']}</p>
                    <span class="tag">{r['tipo_apoyo_ofrecido']}</span>
                </div>""", unsafe_allow_html=True)

# ── PÁGINA: PROYECTOS ─────────────────────────────────────────────────────────
elif st.session_state.page == "proyectos":
    st.markdown("## 📋 Proyectos registrados")

    c1, c2, c3 = st.columns(3)
    with c1:
        f_sector = st.selectbox("Sector", ["Todos"] + SECTORES)
    with c2:
        f_localidad = st.selectbox("Localidad", ["Todas"] + LOCALIDADES)
    with c3:
        f_vuln = st.checkbox("Solo zonas vulnerables")

    df = get_proyectos(f_sector, f_localidad, f_vuln)

    if df.empty:
        st.warning("No hay proyectos con esos filtros.")
    else:
        st.markdown(f"**{len(df)} proyecto(s) encontrado(s)**")
        for _, r in df.iterrows():
            vuln_tag = '<span class="tag tag-vulnerable">⚠ ZONA VULNERABLE</span>' if r["zona_vulnerabilidad"] else ""
            st.markdown(f"""
            <div class="card">
                <h3>{r['nombre']}</h3>
                <p>{r['descripcion']}</p>
                <span class="tag">{r['sector']}</span>
                <span class="tag">{r['localidad']}</span>
                <span class="tag">{r['tipo_apoyo_buscado']}</span>
                {vuln_tag}
                <br><small style="color:#999">Contacto: {r['contacto_nombre']} · {r['contacto_email']}</small>
            </div>""", unsafe_allow_html=True)

# ── PÁGINA: NUEVO PROYECTO ────────────────────────────────────────────────────
elif st.session_state.page == "nuevo_proyecto":
    st.markdown("## ➕ Registrar proyecto")
    st.caption("Completa los campos. Todos los marcados con * son obligatorios.")

    with st.form("form_proyecto", clear_on_submit=True):
        nombre = st.text_input("Nombre del proyecto *")
        descripcion = st.text_area("Descripción breve *", height=100)
        col1, col2 = st.columns(2)
        with col1:
            sector = st.selectbox("Sector principal *", SECTORES)
            localidad = st.selectbox("Localidad *", LOCALIDADES)
        with col2:
            presupuesto = st.selectbox("Presupuesto estimado *", [
                "< $10.000", "$10.000 – $50.000",
                "$50.000 – $200.000", "> $200.000", "Por definir"
            ])
            tipo_apoyo = st.selectbox("¿Qué tipo de apoyo buscas? *", TIPOS_APOYO)
        zona_vuln = st.checkbox("¿El proyecto está en zona de alta vulnerabilidad?")
        perfil_creador = st.selectbox("Tu perfil *", PERFILES)
        col3, col4 = st.columns(2)
        with col3:
            contacto_nombre = st.text_input("Tu nombre *")
        with col4:
            contacto_email = st.text_input("Tu email *")

        submitted = st.form_submit_button("Registrar proyecto", use_container_width=True)

    if submitted:
        if not all([nombre, descripcion, contacto_nombre, contacto_email]):
            st.error("Completa todos los campos obligatorios.")
        else:
            insertar_proyecto({
                "nombre": nombre, "descripcion": descripcion,
                "sector": sector, "localidad": localidad,
                "zona_vulnerabilidad": int(zona_vuln),
                "presupuesto_estimado": presupuesto,
                "tipo_apoyo_buscado": tipo_apoyo,
                "contacto_nombre": contacto_nombre,
                "contacto_email": contacto_email,
                "perfil_creador": perfil_creador,
            })
            st.success(f"✅ Proyecto **{nombre}** registrado correctamente.")
            st.balloons()

# ── PÁGINA: ACTORES ───────────────────────────────────────────────────────────
elif st.session_state.page == "actores":
    st.markdown("## 🤝 Actores del ecosistema")

    c1, c2 = st.columns(2)
    with c1:
        f_perfil = st.selectbox("Perfil", ["Todos"] + PERFILES)
    with c2:
        f_sector = st.selectbox("Sector de interés", ["Todos"] + SECTORES)

    df = get_actores(f_perfil, f_sector)

    if df.empty:
        st.warning("No hay actores con esos filtros.")
    else:
        st.markdown(f"**{len(df)} actor(es) encontrado(s)**")
        for _, r in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <h3>{r['nombre']} · <small>{r['perfil']}</small></h3>
                <p>{r['organizacion']}</p>
                <span class="tag">{r['tipo_apoyo_ofrecido']}</span>
                <span class="tag">{r['sectores_interes']}</span>
                <br><small style="color:#999">{r['email']}</small>
            </div>""", unsafe_allow_html=True)

# ── PÁGINA: NUEVO ACTOR ───────────────────────────────────────────────────────
elif st.session_state.page == "nuevo_actor":
    st.markdown("## ➕ Registrar actor")

    with st.form("form_actor", clear_on_submit=True):
        nombre = st.text_input("Nombre completo *")
        organizacion = st.text_input("Organización o institución")
        col1, col2 = st.columns(2)
        with col1:
            perfil = st.selectbox("Tu perfil *", PERFILES)
            tipo_apoyo = st.selectbox("¿Qué tipo de apoyo puedes ofrecer? *", TIPOS_APOYO)
        with col2:
            sectores = st.multiselect("Sectores de interés *", SECTORES)
            localidades = st.multiselect("Localidades de interés", LOCALIDADES)
        email = st.text_input("Email de contacto *")

        submitted = st.form_submit_button("Registrar actor", use_container_width=True)

    if submitted:
        if not all([nombre, perfil, email, sectores]):
            st.error("Completa todos los campos obligatorios.")
        else:
            insertar_actor({
                "nombre": nombre, "organizacion": organizacion,
                "perfil": perfil,
                "sectores_interes": ", ".join(sectores),
                "localidades_interes": ", ".join(localidades),
                "tipo_apoyo_ofrecido": tipo_apoyo,
                "email": email,
            })
            st.success(f"✅ Actor **{nombre}** registrado correctamente.")

# ── PÁGINA: MATCHING ──────────────────────────────────────────────────────────
elif st.session_state.page == "matching":
    st.markdown("## 🔗 Motor de matching")
    st.caption("Selecciona un proyecto para encontrar actores que pueden apoyarlo.")

    df_p = get_proyectos()
    if df_p.empty:
        st.warning("Primero registra al menos un proyecto.")
    else:
        opciones_p = {f"{r['nombre']} ({r['sector']})": r["id"] for _, r in df_p.iterrows()}
        seleccion = st.selectbox("Selecciona proyecto", list(opciones_p.keys()))
        pid = opciones_p[seleccion]

        if st.button("🔍 Buscar matches", use_container_width=True):
            matches = matching(pid)
            if matches.empty:
                st.info("No se encontraron actores con match directo. Registra más actores.")
            else:
                st.success(f"✅ {len(matches)} actor(es) con potencial de colaboración")
                for _, r in matches.iterrows():
                    st.markdown(f"""
                    <div class="match-card">
                        <strong>{r['nombre']}</strong> · {r['perfil']}<br>
                        <span style="color:#27AE60">▶ {r['tipo_apoyo_ofrecido']}</span>
                        &nbsp;·&nbsp; {r['organizacion']}<br>
                        <small>{r['email']}</small>
                    </div>""", unsafe_allow_html=True)
