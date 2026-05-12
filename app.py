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
    page_title="CityLab",
    page_icon="○",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand CSS ─────────────────────────────────────────────────────────────────
def inject_brand():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&family=DM+Mono:wght@400&display=swap');

    :root {
        --color-primary:   #0D0D0D;
        --color-secondary: #F5F5F0;
        --color-accent:    #E8437A;
        --color-bg:        #FAFAF8;
        --color-surface:   #F0F0EB;
        --color-text:      #1A1A1A;
        --color-muted:     #6B6B6B;
        --color-border:    #E2E2DC;
        --font-header: 'Playfair Display', Georgia, serif;
        --font-body:   'DM Sans', system-ui, sans-serif;
        --font-mono:   'DM Mono', 'Courier New', monospace;
        --radius-sm: 2px; --radius-md: 6px; --radius-lg: 12px;
        --shadow-md: 0 4px 16px rgba(0,0,0,.10);
    }

    html, body, [class*="css"] {
        font-family: var(--font-body);
        background-color: var(--color-bg);
        color: var(--color-text);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--color-primary) !important;
    }
    section[data-testid="stSidebar"] * { color: #FAFAF8 !important; }
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        color: #FAFAF8 !important;
        border: 1px solid rgba(255,255,255,.12) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
        font-size: .85rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: background .15s;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(232,67,122,.2) !important;
        border-color: var(--color-accent) !important;
    }

    /* Botones */
    .stButton > button {
        background-color: var(--color-primary) !important;
        color: var(--color-bg) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
        font-size: .9rem !important;
        font-weight: 500 !important;
        padding: 10px 24px !important;
        letter-spacing: .01em;
        transition: background .15s, transform .1s;
    }
    .stButton > button:hover {
        background-color: #2A2A2A !important;
        transform: translateY(-1px);
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background-color: var(--color-surface) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
        color: var(--color-text) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 2px rgba(13,13,13,.08) !important;
    }

    /* Labels */
    .stTextInput label, .stTextArea label,
    .stSelectbox label, .stMultiSelect label, .stCheckbox label {
        font-family: var(--font-body) !important;
        font-size: .78rem !important;
        font-weight: 500 !important;
        letter-spacing: .04em !important;
        text-transform: uppercase !important;
        color: var(--color-muted) !important;
    }

    /* Form container */
    [data-testid="stForm"] {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: 32px !important;
    }

    /* Typography */
    h1 {
        font-family: var(--font-header) !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        letter-spacing: -.02em !important;
        color: var(--color-primary) !important;
        line-height: 1.1 !important;
    }
    h2 {
        font-family: var(--font-header) !important;
        font-size: 1.8rem !important;
        color: var(--color-primary) !important;
    }
    h3 {
        font-family: var(--font-body) !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }

    /* Components */
    .cl-hero {
        background: var(--color-primary);
        padding: 48px 48px 40px;
        border-radius: var(--radius-lg);
        margin-bottom: 32px;
    }
    .cl-hero h1 { color: #FAFAF8 !important; font-size: 3rem !important; max-width: 580px; }
    .cl-hero p  { color: #8A8A8A; font-size: .95rem; margin: 12px 0 0; }
    .cl-hero a  { color: #FAFAF8; opacity: .6; font-size: .82rem;
                  letter-spacing: .04em; text-decoration: none; display: block; margin-top: 24px; }

    .cl-card {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: 20px 24px;
        margin-bottom: 12px;
        transition: box-shadow .2s, transform .15s;
    }
    .cl-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
    .cl-card h3  { margin: 0 0 6px 0; font-size: .98rem; }
    .cl-card p   { margin: 0; color: var(--color-muted); font-size: .86rem; line-height: 1.5; }

    .cl-tag {
        display: inline-block;
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        font-family: var(--font-mono);
        font-size: .7rem;
        padding: 2px 8px;
        border-radius: var(--radius-sm);
        margin: 6px 4px 0 0;
        letter-spacing: .02em;
        color: var(--color-text);
    }
    .cl-tag-vuln {
        background: #FFF0F3;
        color: var(--color-accent);
        border-color: #F7C0CF;
    }

    .cl-metric-row { display: flex; gap: 12px; margin-bottom: 32px; flex-wrap: wrap; }
    .cl-metric-box {
        flex: 1; min-width: 120px;
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: 24px 28px; text-align: center;
    }
    .cl-metric-box .cl-num {
        font-family: var(--font-header); font-size: 2.4rem;
        font-weight: 700; color: var(--color-primary); line-height: 1;
    }
    .cl-metric-box .cl-lbl {
        font-family: var(--font-body); font-size: .72rem;
        font-weight: 500; color: var(--color-muted);
        text-transform: uppercase; letter-spacing: .06em; margin-top: 6px;
    }

    .cl-match-card {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-left: 3px solid var(--color-accent);
        border-radius: var(--radius-md);
        padding: 14px 20px; margin-bottom: 10px;
    }

    .cl-divider { border: none; border-top: 1px solid var(--color-border); margin: 32px 0; }
    .cl-index   { font-family: var(--font-mono); font-size: .72rem; color: var(--color-muted); }

    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# ── Base de datos ─────────────────────────────────────────────────────────────
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS proyectos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, descripcion TEXT NOT NULL,
                sector TEXT NOT NULL, localidad TEXT NOT NULL,
                zona_vulnerable INTEGER NOT NULL DEFAULT 0,
                presupuesto TEXT NOT NULL, tipo_apoyo_buscado TEXT NOT NULL,
                perfil_creador TEXT NOT NULL, contacto_nombre TEXT NOT NULL,
                contacto_email TEXT NOT NULL, estado TEXT NOT NULL DEFAULT 'activo',
                fecha_creacion TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS actores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, organizacion TEXT,
                perfil TEXT NOT NULL, sectores_interes TEXT NOT NULL,
                localidades_interes TEXT, tipo_apoyo_ofrecido TEXT NOT NULL,
                email TEXT NOT NULL, fecha_registro TEXT NOT NULL
            );
        """)
        conn.commit(); conn.close()
    except sqlite3.Error as e:
        st.error(f"Error al iniciar la base de datos: {e}"); st.stop()

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def insertar_proyecto(d):
    try:
        conn = get_conn()
        conn.execute("""INSERT INTO proyectos
            (nombre,descripcion,sector,localidad,zona_vulnerable,presupuesto,
             tipo_apoyo_buscado,perfil_creador,contacto_nombre,contacto_email,fecha_creacion)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (d["nombre"],d["descripcion"],d["sector"],d["localidad"],d["zona_vulnerable"],
             d["presupuesto"],d["tipo_apoyo_buscado"],d["perfil_creador"],
             d["contacto_nombre"],d["contacto_email"],datetime.now().isoformat()))
        conn.commit(); conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"No se pudo guardar el proyecto: {e}")

def insertar_actor(d):
    try:
        conn = get_conn()
        conn.execute("""INSERT INTO actores
            (nombre,organizacion,perfil,sectores_interes,localidades_interes,
             tipo_apoyo_ofrecido,email,fecha_registro)
            VALUES (?,?,?,?,?,?,?,?)""",
            (d["nombre"],d["organizacion"],d["perfil"],d["sectores_interes"],
             d["localidades_interes"],d["tipo_apoyo_ofrecido"],d["email"],
             datetime.now().isoformat()))
        conn.commit(); conn.close()
    except sqlite3.Error as e:
        raise RuntimeError(f"No se pudo guardar el actor: {e}")

def obtener_proyectos(sector=None, localidad=None, solo_vulnerables=False):
    try:
        conn = get_conn()
        q = "SELECT * FROM proyectos WHERE estado='activo'"; params = []
        if sector and sector != "Todos":
            q += " AND sector=?"; params.append(sector)
        if localidad and localidad != "Todas":
            q += " AND localidad=?"; params.append(localidad)
        if solo_vulnerables:
            q += " AND zona_vulnerable=1"
        q += " ORDER BY fecha_creacion DESC"
        df = pd.read_sql_query(q, conn, params=params); conn.close(); return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener proyectos: {e}")

def obtener_actores(perfil=None, sector=None):
    try:
        conn = get_conn()
        q = "SELECT * FROM actores WHERE 1=1"; params = []
        if perfil and perfil != "Todos":
            q += " AND perfil=?"; params.append(perfil)
        if sector and sector != "Todos":
            q += " AND sectores_interes LIKE ?"; params.append(f"%{sector}%")
        q += " ORDER BY fecha_registro DESC"
        df = pd.read_sql_query(q, conn, params=params); conn.close(); return df
    except Exception as e:
        raise RuntimeError(f"Error al obtener actores: {e}")

def calcular_matches(proyecto, df_actores):
    if df_actores.empty: return pd.DataFrame()
    tipo = proyecto.get("tipo_apoyo_buscado","")
    sector = proyecto.get("sector","")
    m_apoyo  = df_actores["tipo_apoyo_ofrecido"].str.contains(tipo, case=False, na=False)
    m_sector = df_actores["sectores_interes"].str.contains(sector, case=False, na=False)
    result = df_actores[m_apoyo | m_sector].copy()
    result["puntaje"] = result.apply(
        lambda r: (1 if tipo.lower() in r["tipo_apoyo_ofrecido"].lower() else 0) +
                  (1 if sector.lower() in r["sectores_interes"].lower() else 0), axis=1)
    return result.sort_values("puntaje", ascending=False).reset_index(drop=True)

def validar_proyecto(d):
    errores = []
    if not d.get("nombre","").strip(): errores.append("El nombre del proyecto es obligatorio.")
    elif len(d["nombre"]) > MAX_NOMBRE: errores.append(f"El nombre no puede superar {MAX_NOMBRE} caracteres.")
    if not d.get("descripcion","").strip(): errores.append("La descripción es obligatoria.")
    elif len(d["descripcion"]) > MAX_DESCRIPCION: errores.append(f"La descripción no puede superar {MAX_DESCRIPCION} caracteres.")
    if not d.get("contacto_nombre","").strip(): errores.append("El nombre de contacto es obligatorio.")
    email = d.get("contacto_email","").strip()
    if not email: errores.append("El email de contacto es obligatorio.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El email no tiene un formato válido (ejemplo: nombre@dominio.com).")
    return errores

def validar_actor(d):
    errores = []
    if not d.get("nombre","").strip(): errores.append("El nombre es obligatorio.")
    if not d.get("sectores_interes"): errores.append("Selecciona al menos un sector de interés.")
    email = d.get("email","").strip()
    if not email: errores.append("El email es obligatorio.")
    elif "@" not in email or "." not in email.split("@")[-1]:
        errores.append("El email no tiene un formato válido (ejemplo: nombre@dominio.com).")
    return errores

# ── Init ──────────────────────────────────────────────────────────────────────
init_db()
inject_brand()

if "page" not in st.session_state:
    st.session_state.page = "inicio"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 24px; border-bottom: 1px solid rgba(255,255,255,.1); margin-bottom: 20px;">
        <div style="font-family:'DM Mono',monospace; font-size:.7rem; color:#6B6B6B;
                    letter-spacing:.12em; text-transform:uppercase; margin-bottom:4px;">
            Plataforma urbana
        </div>
        <div style="font-family:'Playfair Display',serif; font-size:1.3rem;
                    color:#FAFAF8; font-weight:700; letter-spacing:-.01em;">
            CityLab
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav = {
        "Inicio":              "inicio",
        "Proyectos":           "proyectos",
        "Registrar proyecto":  "nuevo_proyecto",
        "Actores":             "actores",
        "Registrar actor":     "nuevo_actor",
        "Motor de matching":   "matching",
    }
    for etiqueta, clave in nav.items():
        if st.button(etiqueta, use_container_width=True):
            st.session_state.page = clave

# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page

# ── INICIO ────────────────────────────────────────────────────────────────────
if page == "inicio":
    st.markdown("""
    <div class="cl-hero">
        <h1>Diseñamos ciudades a las que quieres pertenecer.</h1>
        <p>Convertimos problemáticas del territorio en oportunidades de cambio,<br>
           conectando ciudadanos, academia e instituciones.</p>
        <a href="#">↳ Explorar todos los proyectos</a>
    </div>
    """, unsafe_allow_html=True)

    try:
        df_p = obtener_proyectos(); df_a = obtener_actores()
    except RuntimeError as e:
        st.error(str(e)); st.stop()

    n_vuln = int(df_p["zona_vulnerable"].sum()) if not df_p.empty else 0

    st.markdown(f"""
    <div class="cl-metric-row">
        <div class="cl-metric-box">
            <div class="cl-num">{len(df_p)}</div>
            <div class="cl-lbl">Proyectos activos</div>
        </div>
        <div class="cl-metric-box">
            <div class="cl-num">{len(df_a)}</div>
            <div class="cl-lbl">Actores en el ecosistema</div>
        </div>
        <div class="cl-metric-box">
            <div class="cl-num">{n_vuln}</div>
            <div class="cl-lbl">Zonas vulnerables</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Proyectos recientes")
        if df_p.empty:
            st.info("Aún no hay proyectos. Registra el primero desde el menú.")
        else:
            for i, (_, r) in enumerate(df_p.head(3).iterrows()):
                vuln = '<span class="cl-tag cl-tag-vuln">zona vulnerable</span>' if r["zona_vulnerable"] else ""
                st.markdown(f"""
                <div class="cl-card">
                    <span class="cl-index">#{i+1:02d}</span>
                    <h3>{r['nombre']}</h3>
                    <p>{str(r['descripcion'])[:110]}…</p>
                    <span class="cl-tag">{r['sector']}</span>
                    <span class="cl-tag">{r['localidad']}</span>
                    {vuln}
                </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### Actores recientes")
        if df_a.empty:
            st.info("Sé el primero en registrarte como actor del ecosistema.")
        else:
            for _, r in df_a.head(3).iterrows():
                st.markdown(f"""
                <div class="cl-card">
                    <h3>{r['nombre']}</h3>
                    <p>{r['organizacion'] or 'Independiente'} · {r['perfil']}</p>
                    <span class="cl-tag">{r['tipo_apoyo_ofrecido']}</span>
                </div>""", unsafe_allow_html=True)

# ── PROYECTOS ─────────────────────────────────────────────────────────────────
elif page == "proyectos":
    st.markdown("## Proyectos")
    st.caption("Filtra por sector, localidad o nivel de prioridad territorial.")
    st.markdown('<hr class="cl-divider">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: sector = st.selectbox("Sector", ["Todos"] + SECTORES)
    with c2: localidad = st.selectbox("Localidad", ["Todas"] + LOCALIDADES)
    with c3: solo_vuln = st.checkbox("Solo zonas vulnerables")

    try: df = obtener_proyectos(sector, localidad, solo_vuln)
    except RuntimeError as e: st.error(str(e)); st.stop()

    if df.empty:
        st.warning("No hay proyectos con esos filtros. Amplía la búsqueda.")
    else:
        st.markdown(f"<p class='cl-index'>{len(df)} proyecto(s)</p>", unsafe_allow_html=True)
        for i, (_, r) in enumerate(df.iterrows()):
            vuln = '<span class="cl-tag cl-tag-vuln">zona vulnerable</span>' if r["zona_vulnerable"] else ""
            st.markdown(f"""
            <div class="cl-card">
                <span class="cl-index">#{i+1:02d}</span>
                <h3>{r['nombre']}</h3>
                <p>{r['descripcion']}</p>
                <span class="cl-tag">{r['sector']}</span>
                <span class="cl-tag">{r['localidad']}</span>
                <span class="cl-tag">{r['tipo_apoyo_buscado']}</span>
                {vuln}
                <br><small style="color:var(--color-muted);font-size:.78rem;margin-top:8px;display:block">
                    Contacto: {r['contacto_nombre']} · {r['contacto_email']}
                </small>
            </div>""", unsafe_allow_html=True)

# ── NUEVO PROYECTO ────────────────────────────────────────────────────────────
elif page == "nuevo_proyecto":
    st.markdown("## Registrar proyecto")
    st.caption("Tu proyecto aparecerá en el directorio y estará disponible para el motor de matching.")
    st.markdown('<hr class="cl-divider">', unsafe_allow_html=True)

    with st.form("form_proyecto", clear_on_submit=True):
        nombre = st.text_input("Nombre del proyecto *", help="Máx. 120 caracteres")
        descripcion = st.text_area("Describe el proyecto *", height=110,
            help="¿Qué problemática resuelve y cómo? Máx. 600 caracteres")
        c1, c2 = st.columns(2)
        with c1:
            sector = st.selectbox("Sector principal *", SECTORES)
            localidad = st.selectbox("Localidad *", LOCALIDADES)
        with c2:
            presupuesto = st.selectbox("Presupuesto estimado *", PRESUPUESTOS)
            tipo_apoyo = st.selectbox("¿Qué tipo de apoyo buscas? *", TIPOS_APOYO)
        zona_vulnerable = st.checkbox(
            "El proyecto está en zona de alta vulnerabilidad",
            help="Activa si el área tiene necesidades críticas de intervención urbana")
        perfil_creador = st.selectbox("Tu perfil *", PERFILES)
        c3, c4 = st.columns(2)
        with c3: contacto_nombre = st.text_input("Tu nombre *")
        with c4: contacto_email  = st.text_input("Tu email *", help="nombre@dominio.com")
        enviado = st.form_submit_button("Registrar proyecto", use_container_width=True)

    if enviado:
        datos = {"nombre": nombre, "descripcion": descripcion, "sector": sector,
                 "localidad": localidad, "zona_vulnerable": int(zona_vulnerable),
                 "presupuesto": presupuesto, "tipo_apoyo_buscado": tipo_apoyo,
                 "perfil_creador": perfil_creador, "contacto_nombre": contacto_nombre,
                 "contacto_email": contacto_email}
        errores = validar_proyecto(datos)
        if errores:
            for e in errores: st.error(e)
        else:
            with st.spinner("Guardando proyecto…"):
                try:
                    insertar_proyecto(datos)
                    st.success(f"**{nombre}** fue registrado. Ya aparece en el directorio y en el motor de matching.")
                    st.balloons()
                except RuntimeError as e:
                    st.error(str(e))

# ── ACTORES ───────────────────────────────────────────────────────────────────
elif page == "actores":
    st.markdown("## Actores del ecosistema")
    st.caption("Personas y organizaciones comprometidas con construir ciudad.")
    st.markdown('<hr class="cl-divider">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: perfil = st.selectbox("Perfil", ["Todos"] + PERFILES)
    with c2: sector = st.selectbox("Sector de interés", ["Todos"] + SECTORES)

    try: df = obtener_actores(perfil, sector)
    except RuntimeError as e: st.error(str(e)); st.stop()

    if df.empty:
        st.warning("No hay actores con esos filtros.")
    else:
        st.markdown(f"<p class='cl-index'>{len(df)} actor(es)</p>", unsafe_allow_html=True)
        for _, r in df.iterrows():
            st.markdown(f"""
            <div class="cl-card">
                <h3>{r['nombre']}</h3>
                <p>{r['organizacion'] or 'Independiente'} · {r['perfil']}</p>
                <span class="cl-tag">{r['tipo_apoyo_ofrecido']}</span>
                <span class="cl-tag">{r['sectores_interes']}</span>
                <br><small style="color:var(--color-muted);font-size:.78rem;margin-top:8px;display:block">
                    {r['email']}
                </small>
            </div>""", unsafe_allow_html=True)

# ── NUEVO ACTOR ───────────────────────────────────────────────────────────────
elif page == "nuevo_actor":
    st.markdown("## Registrar como actor")
    st.caption("Dinos cómo puedes contribuir. Te conectaremos con proyectos que necesitan lo que ofreces.")
    st.markdown('<hr class="cl-divider">', unsafe_allow_html=True)

    with st.form("form_actor", clear_on_submit=True):
        nombre = st.text_input("Nombre completo *")
        organizacion = st.text_input("Organización o institución", help="Opcional — deja vacío si eres independiente")
        c1, c2 = st.columns(2)
        with c1:
            perfil = st.selectbox("Tu perfil *", PERFILES)
            tipo_apoyo = st.selectbox("¿Qué tipo de apoyo puedes ofrecer? *", TIPOS_APOYO)
        with c2:
            sectores   = st.multiselect("Sectores de interés *", SECTORES)
            localidades = st.multiselect("Localidades de interés", LOCALIDADES)
        email = st.text_input("Email de contacto *", help="nombre@dominio.com")
        enviado = st.form_submit_button("Registrar actor", use_container_width=True)

    if enviado:
        datos = {"nombre": nombre, "organizacion": organizacion or "",
                 "perfil": perfil, "sectores_interes": ", ".join(sectores),
                 "localidades_interes": ", ".join(localidades),
                 "tipo_apoyo_ofrecido": tipo_apoyo, "email": email}
        errores = validar_actor(datos)
        if errores:
            for e in errores: st.error(e)
        else:
            with st.spinner("Registrando actor…"):
                try:
                    insertar_actor(datos)
                    st.success(f"**{nombre}** fue registrado. Ahora apareces en el ecosistema y en el motor de matching.")
                except RuntimeError as e:
                    st.error(str(e))

# ── MATCHING ──────────────────────────────────────────────────────────────────
elif page == "matching":
    st.markdown("## Motor de matching")
    st.caption("Selecciona un proyecto para encontrar actores compatibles por sector y tipo de colaboración.")
    st.markdown('<hr class="cl-divider">', unsafe_allow_html=True)

    try: df_p = obtener_proyectos()
    except RuntimeError as e: st.error(str(e)); st.stop()

    if df_p.empty:
        st.warning("Primero registra al menos un proyecto desde el menú.")
    else:
        opciones = {f"{r['nombre']} — {r['sector']}": idx for idx, r in df_p.iterrows()}
        seleccion = st.selectbox("Selecciona un proyecto", list(opciones.keys()))
        fila_idx  = opciones[seleccion]
        proyecto  = df_p.iloc[fila_idx].to_dict()

        if st.button("Buscar actores compatibles", use_container_width=True):
            with st.spinner("Analizando compatibilidad en el ecosistema…"):
                try:
                    df_a    = obtener_actores()
                    matches = calcular_matches(proyecto, df_a)
                except RuntimeError as e:
                    st.error(str(e)); st.stop()

            if matches.empty:
                st.info("No se encontraron actores con match directo. Registra más actores para ampliar el ecosistema.")
            else:
                st.success(f"{len(matches)} actor(es) compatibles con **{proyecto['nombre']}**")
                for _, r in matches.iterrows():
                    estrellas = "●" * int(r["puntaje"]) + "○" * (2 - int(r["puntaje"]))
                    st.markdown(f"""
                    <div class="cl-match-card">
                        <strong style="font-family:var(--font-body)">{r['nombre']}</strong>
                        &nbsp;·&nbsp; <span style="color:var(--color-muted)">{r['perfil']}</span>
                        &nbsp;<span style="color:var(--color-accent);font-family:var(--font-mono);
                                           font-size:.8rem">{estrellas}</span><br>
                        <span class="cl-tag">{r['tipo_apoyo_ofrecido']}</span>
                        <br><small style="color:var(--color-muted);font-size:.78rem;
                                         display:block;margin-top:8px">{r['email']}</small>
                    </div>""", unsafe_allow_html=True)

else:
    st.error(f"Página '{page}' no reconocida. Usa el menú lateral.")
