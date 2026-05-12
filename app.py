import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ── Constantes ────────────────────────────────────────────────────────────────
DB_PATH = "/tmp/ciudad_lab.db"

SECTORES = [
    "Movilidad urbana", "Seguridad ciudadana", "Medio ambiente",
    "Vivienda", "Espacio público", "Educación", "Salud",
    "Cultura y patrimonio", "Economía local", "Otro",
]
LOCALIDADES = [
    "Norte", "Centro histórico", "Sur", "Valle de los Chillos",
    "Tumbaco", "Calderón", "La Delicia", "Otro",
]
PERFILES = ["Ciudadano/a", "Sociedad civil", "Academia", "Sector privado", "Gobierno"]
TIPOS_APOYO = ["Financiamiento", "Co-ejecución", "Expertise técnico", "Redes / conexiones", "Visibilidad"]
PRESUPUESTOS = ["< $10.000", "$10.000 – $50.000", "$50.000 – $200.000", "> $200.000", "Por definir"]
MAX_NOMBRE = 120
MAX_DESCRIPCION = 600

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quito Ciudad Lab",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.header-band {
    background: #0B1F2E; padding: 2rem 2.5rem 1.5rem;
    border-radius: 12px; margin-bottom: 2rem;
}
.header-band h1 {
    color: #E8FF4A; font-size: 2.4rem; font-weight: 800;
    margin: 0 0 .3rem 0; letter-spacing: -1px;
}
.header-band p { color: #8BAFC2; font-size: .95rem; margin: 0; }
.card {
    background: #F5F7F2; border-left: 4px solid #E8FF4A;
    border-radius: 8px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.card h3 { margin: 0 0 .4rem 0; color: #0B1F2E; font-size: 1.05rem; font-weight: 700; }
.card p  { margin: 0; color: #4A5568; font-size: .88rem; }
.tag {
    display: inline-block; background: #0B1F2E; color: #E8FF4A;
    font-size: .72rem; font-weight: 700; padding: .2rem .55rem;
    border-radius: 4px; margin: .3rem .2rem 0 0;
    font-family: 'Space Mono', monospace;
}
.tag-vulnerable { background: #C0392B !important; color: #fff !important; }
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-box {
    flex: 1; min-width: 120px; background: #0B1F2E;
    border-radius: 10px; padding: 1.1rem 1.4rem; text-align: center;
}
.metric-box .num { color: #E8FF4A; font-size: 2rem; font-weight: 800; }
.metric-box .lbl { color: #8BAFC2; font-size: .78rem; margin-top: .2rem; }
.match-card {
    background: #EAF9F1; border-left: 4px solid #27AE60;
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: .8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Base de datos ─────────────────────────────────────────────────────────────

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.executescript("""
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
        st.error(f"Error al iniciar la base de datos: {e}")
        st.stop()

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def insertar_proyecto(d):
    try:
        conn = get_conn()
        conn.execute("""
            INSERT INTO proyectos
                (nombre, descripcion, sector, localidad, zona_vulnerable,
                 presupuesto, tipo_apoyo_buscado, perfil_creador,
                 contacto_nombre, contacto_email, fecha_creacion)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (d["nombre"], d["descripcion"], d["sector"], d["localidad"],
              d["zona_vulnerable"], d["presupuesto"], d["tipo_apoyo_buscado"],
              d["perfil_creador"], d["contacto_nombre"], d["contacto_email"],
              datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"No se pudo guardar el proyecto: {e}")

def insertar_actor(d):
    try:
        conn = get_conn()
        conn.execute("""
            INSERT INTO actores
                (nombre, organizacion, perfil, sectores_interes,
                 localidades_interes, tipo_apoyo_ofrecido, email, fecha_registro)
            VALUES (?,?,?,?,?,?,?,?)
        """, (d["nombre"], d["organizacion"], d["perfil"], d["sectores_interes"],
              d["localidades_interes"], d["tipo_apoyo_ofrecido"], d["email"],
              datetime.now().isoformat()))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"No se pudo guardar el actor: {e}")

def obtener_proyectos(sector=None, localidad=None, solo_vulnerables=False):
    try:
        conn = get_conn()
        q = "SELECT * FROM proyectos WHERE estado='activo'"
        params = []
        if sector and sector != "Todos":
            q += " AND sector=?"; params.append(sector)
        if localidad and localidad != "Todas":
            q += " AND localidad=?"; params.append(localidad)
        if solo_vulnerables:
            q += " AND zona_vulnerable=1"
        q += " ORDER BY fecha_creacion DESC"
        df = pd.read_sql_query(q, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener proyectos: {e}")

def obtener_actores(perfil=None, sector=None):
    try:
        conn = get_conn()
        q = "SELECT * FROM actores WHERE 1=1"
        params = []
        if perfil and perfil != "Todos":
            q += " AND perfil=?"; params.append(perfil)
        if sector and sector != "Todos":
            q += " AND sectores_interes LIKE ?"; params.append(f"%{sector}%")
        q += " ORDER BY fecha_registro DESC"
        df = pd.read_sql_query(q, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener actores: {e}")

def calcular_matches(proyecto, df_actores):
    if df_actores.empty:
        return pd.DataFrame()
    tipo = proyecto.get("tipo_apoyo_buscado", "")
    sector = proyecto.get("sector", "")
    m_apoyo  = df_actores["tipo_apoyo_ofrecido"].str.contains(tipo, case=False, na=False)
    m_sector = df_actores["sectores_interes"].str.contains(sector, case=False, na=False)
    result = df_actores[m_apoyo | m_sector].copy()
    result["puntaje"] = result.apply(
        lambda r: (1 if tipo.lower() in r["tipo_apoyo_ofrecido"].lower() else 0) +
                  (1 if sector.lower() in r["sectores_interes"].lower() else 0), axis=1)
    return result.sort_values("puntaje", ascending=False).reset_index(drop=True)

# ── Validadores ───────────────────────────────────────────────────────────────

def validar_proyecto(d):
    errores = []
    if not d.get("nombre", "").strip():
        errores.append("El nombre del proyecto es obligatorio.")
    elif len(d["nombre"]) > MAX_NOMBRE:
        errores.append(f"El nombre no puede superar {MAX_NOMBRE} caracteres.")
    if not d.get("descripcion", "").strip():
        errores.append("La descripción es obligatoria.")
    elif len(d["descripcion"]) > MAX_DESCRIPCION:
        errores.append(f"La descripción no puede superar {MAX_DESCRIPCION} caracteres.")
    if not d.get("contacto_nombre", "").strip():
        errores.append("El nombre de contacto es obligatorio.")
    email = d.get("contacto_email", "").strip()
    if not email:
        errores.append("El email de contacto es obligatorio.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El email no tiene un formato válido (ejemplo: nombre@dominio.com).")
    return errores

def validar_actor(d):
    errores = []
    if not d.get("nombre", "").strip():
        errores.append("El nombre es obligatorio.")
    if not d.get("sectores_interes"):
        errores.append("Selecciona al menos un sector de interés.")
    email = d.get("email", "").strip()
    if not email:
        errores.append("El email es obligatorio.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El email no tiene un formato válido (ejemplo: nombre@dominio.com).")
    return errores

# ── Init ──────────────────────────────────────────────────────────────────────
init_db()

if "page" not in st.session_state:
    st.session_state.page = "inicio"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏙️ Ciudad Lab")
    st.markdown("---")
    nav = {
        "🏠 Inicio":               "inicio",
        "📋 Proyectos":            "proyectos",
        "➕ Registrar proyecto":   "nuevo_proyecto",
        "🤝 Actores":              "actores",
        "➕ Registrar actor":      "nuevo_actor",
        "🔗 Matching":             "matching",
    }
    for etiqueta, clave in nav.items():
        if st.button(etiqueta, use_container_width=True):
            st.session_state.page = clave

# ── Páginas ───────────────────────────────────────────────────────────────────
page = st.session_state.page

# ── INICIO ────────────────────────────────────────────────────────────────────
if page == "inicio":
    st.markdown("""
    <div class="header-band">
        <h1>Quito Ciudad Lab</h1>
        <p>Conectando actores para construir ciudad — desde la mitad del mundo.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        df_p = obtener_proyectos()
        df_a = obtener_actores()
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

    n_vuln = int(df_p["zona_vulnerable"].sum()) if not df_p.empty else 0

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
            st.info("Aún no hay proyectos. ¡Registra el primero desde el menú!")
        else:
            for _, r in df_p.head(3).iterrows():
                vuln = '<span class="tag tag-vulnerable">⚠ ZONA VULNERABLE</span>' if r["zona_vulnerable"] else ""
                st.markdown(f"""
                <div class="card">
                    <h3>{r['nombre']}</h3>
                    <p>{str(r['descripcion'])[:100]}…</p>
                    <span class="tag">{r['sector']}</span>
                    <span class="tag">{r['localidad']}</span>
                    {vuln}
                </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### Últimos actores")
        if df_a.empty:
            st.info("Aún no hay actores registrados. ¡Sé el primero!")
        else:
            for _, r in df_a.head(3).iterrows():
                st.markdown(f"""
                <div class="card">
                    <h3>{r['nombre']} · <small>{r['perfil']}</small></h3>
                    <p>{r['organizacion'] or '—'}</p>
                    <span class="tag">{r['tipo_apoyo_ofrecido']}</span>
                </div>""", unsafe_allow_html=True)

# ── PROYECTOS ─────────────────────────────────────────────────────────────────
elif page == "proyectos":
    st.markdown("## 📋 Proyectos registrados")
    st.caption("Filtra por sector, localidad o prioridad de vulnerabilidad.")

    c1, c2, c3 = st.columns(3)
    with c1: sector = st.selectbox("Sector", ["Todos"] + SECTORES)
    with c2: localidad = st.selectbox("Localidad", ["Todas"] + LOCALIDADES)
    with c3: solo_vuln = st.checkbox("Solo zonas vulnerables")

    try:
        df = obtener_proyectos(sector, localidad, solo_vuln)
    except RuntimeError as e:
        st.error(str(e)); st.stop()

    if df.empty:
        st.warning("No hay proyectos con esos filtros. Prueba ampliar la búsqueda.")
    else:
        st.markdown(f"**{len(df)} proyecto(s) encontrado(s)**")
        for _, r in df.iterrows():
            vuln = '<span class="tag tag-vulnerable">⚠ ZONA VULNERABLE</span>' if r["zona_vulnerable"] else ""
            st.markdown(f"""
            <div class="card">
                <h3>{r['nombre']}</h3>
                <p>{r['descripcion']}</p>
                <span class="tag">{r['sector']}</span>
                <span class="tag">{r['localidad']}</span>
                <span class="tag">{r['tipo_apoyo_buscado']}</span>
                {vuln}
                <br><small style="color:#999">Contacto: {r['contacto_nombre']} · {r['contacto_email']}</small>
            </div>""", unsafe_allow_html=True)

# ── NUEVO PROYECTO ────────────────────────────────────────────────────────────
elif page == "nuevo_proyecto":
    st.markdown("## ➕ Registrar proyecto")
    st.caption("Cuéntanos sobre tu proyecto. Lo conectaremos con actores que pueden apoyarlo.")

    with st.form("form_proyecto", clear_on_submit=True):
        nombre = st.text_input("Nombre del proyecto *", help="Máx. 120 caracteres")
        descripcion = st.text_area("Descripción breve *", height=100,
                                   help="¿Qué problema resuelve y cómo? Máx. 600 caracteres")
        c1, c2 = st.columns(2)
        with c1:
            sector = st.selectbox("Sector principal *", SECTORES)
            localidad = st.selectbox("Localidad *", LOCALIDADES)
        with c2:
            presupuesto = st.selectbox("Presupuesto estimado *", PRESUPUESTOS)
            tipo_apoyo = st.selectbox("¿Qué tipo de apoyo buscas? *", TIPOS_APOYO)
        zona_vulnerable = st.checkbox(
            "El proyecto está en zona de alta vulnerabilidad",
            help="Marca si el área tiene necesidades críticas de intervención urbana"
        )
        perfil_creador = st.selectbox("Tu perfil *", PERFILES)
        c3, c4 = st.columns(2)
        with c3: contacto_nombre = st.text_input("Tu nombre *")
        with c4: contacto_email  = st.text_input("Tu email *", help="ejemplo@dominio.com")

        enviado = st.form_submit_button("Registrar proyecto", use_container_width=True)

    if enviado:
        datos = {
            "nombre": nombre, "descripcion": descripcion,
            "sector": sector, "localidad": localidad,
            "zona_vulnerable": int(zona_vulnerable),
            "presupuesto": presupuesto, "tipo_apoyo_buscado": tipo_apoyo,
            "perfil_creador": perfil_creador,
            "contacto_nombre": contacto_nombre, "contacto_email": contacto_email,
        }
        errores = validar_proyecto(datos)
        if errores:
            for e in errores: st.error(e)
        else:
            with st.spinner("Guardando proyecto…"):
                try:
                    insertar_proyecto(datos)
                    st.success(f"✅ Proyecto **{nombre}** registrado. Ya aparece en el directorio y el motor de matching.")
                    st.balloons()
                except RuntimeError as e:
                    st.error(str(e))

# ── ACTORES ───────────────────────────────────────────────────────────────────
elif page == "actores":
    st.markdown("## 🤝 Actores del ecosistema")
    st.caption("Personas y organizaciones que quieren construir ciudad juntos.")

    c1, c2 = st.columns(2)
    with c1: perfil  = st.selectbox("Perfil", ["Todos"] + PERFILES)
    with c2: sector  = st.selectbox("Sector de interés", ["Todos"] + SECTORES)

    try:
        df = obtener_actores(perfil, sector)
    except RuntimeError as e:
        st.error(str(e)); st.stop()

    if df.empty:
        st.warning("No hay actores con esos filtros.")
    else:
        st.markdown(f"**{len(df)} actor(es) encontrado(s)**")
        for _, r in df.iterrows():
            st.markdown(f"""
            <div class="card">
                <h3>{r['nombre']} · <small>{r['perfil']}</small></h3>
                <p>{r['organizacion'] or '—'}</p>
                <span class="tag">{r['tipo_apoyo_ofrecido']}</span>
                <span class="tag">{r['sectores_interes']}</span>
                <br><small style="color:#999">{r['email']}</small>
            </div>""", unsafe_allow_html=True)

# ── NUEVO ACTOR ───────────────────────────────────────────────────────────────
elif page == "nuevo_actor":
    st.markdown("## ➕ Registrar como actor")
    st.caption("Dinos cómo puedes contribuir. El sistema te conectará con proyectos afines.")

    with st.form("form_actor", clear_on_submit=True):
        nombre       = st.text_input("Nombre completo *")
        organizacion = st.text_input("Organización o institución", help="Opcional")
        c1, c2 = st.columns(2)
        with c1:
            perfil     = st.selectbox("Tu perfil *", PERFILES)
            tipo_apoyo = st.selectbox("¿Qué tipo de apoyo puedes ofrecer? *", TIPOS_APOYO)
        with c2:
            sectores   = st.multiselect("Sectores de interés *", SECTORES)
            localidades = st.multiselect("Localidades de interés", LOCALIDADES)
        email = st.text_input("Email de contacto *", help="ejemplo@dominio.com")

        enviado = st.form_submit_button("Registrar actor", use_container_width=True)

    if enviado:
        datos = {
            "nombre": nombre, "organizacion": organizacion or "",
            "perfil": perfil, "sectores_interes": ", ".join(sectores),
            "localidades_interes": ", ".join(localidades),
            "tipo_apoyo_ofrecido": tipo_apoyo, "email": email,
        }
        errores = validar_actor(datos)
        if errores:
            for e in errores: st.error(e)
        else:
            with st.spinner("Registrando actor…"):
                try:
                    insertar_actor(datos)
                    st.success(f"✅ **{nombre}** registrado. Ahora apareces en el ecosistema y en el motor de matching.")
                except RuntimeError as e:
                    st.error(str(e))

# ── MATCHING ──────────────────────────────────────────────────────────────────
elif page == "matching":
    st.markdown("## 🔗 Motor de matching")
    st.caption("Selecciona un proyecto para encontrar actores que pueden apoyarlo según sector y tipo de colaboración.")

    try:
        df_p = obtener_proyectos()
    except RuntimeError as e:
        st.error(str(e)); st.stop()

    if df_p.empty:
        st.warning("Primero registra al menos un proyecto desde el menú.")
    else:
        opciones = {f"{r['nombre']} ({r['sector']})": idx
                    for idx, r in df_p.iterrows()}
        seleccion = st.selectbox("Selecciona un proyecto", list(opciones.keys()))
        fila_idx  = opciones[seleccion]
        proyecto  = df_p.iloc[fila_idx].to_dict()

        if st.button("🔍 Buscar actores compatibles", use_container_width=True):
            with st.spinner("Buscando matches en el ecosistema…"):
                try:
                    df_a   = obtener_actores()
                    matches = calcular_matches(proyecto, df_a)
                except RuntimeError as e:
                    st.error(str(e)); st.stop()

            if matches.empty:
                st.info("No se encontraron actores con match directo. Registra más actores para ampliar el ecosistema.")
            else:
                st.success(f"✅ {len(matches)} actor(es) con potencial de colaboración para **{proyecto['nombre']}**")
                for _, r in matches.iterrows():
                    estrellas = "★" * int(r["puntaje"]) + "☆" * (2 - int(r["puntaje"]))
                    st.markdown(f"""
                    <div class="match-card">
                        <strong>{r['nombre']}</strong> · {r['perfil']}
                        &nbsp;<span style="color:#E8A100">{estrellas}</span><br>
                        <span style="color:#27AE60">▶ {r['tipo_apoyo_ofrecido']}</span>
                        &nbsp;·&nbsp; {r['organizacion'] or '—'}<br>
                        <small>{r['email']}</small>
                    </div>""", unsafe_allow_html=True)

else:
    st.error(f"Página '{page}' no reconocida. Usa el menú lateral.")
