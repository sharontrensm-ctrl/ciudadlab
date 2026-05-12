"""
app.py — entry point de la aplicación.
Registra páginas, inyecta CSS global, inicializa DB, enruta navegación.
No contiene lógica de negocio ni queries directas.
"""

import streamlit as st
from data.models import init_db
from ui import inicio, proyectos, nuevo_proyecto, actores, nuevo_actor, matching_ui
from config import PAGINAS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quito Ciudad Lab",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.header-band {
    background: #0B1F2E;
    padding: 2rem 2.5rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}
.header-band h1 {
    color: #E8FF4A; font-size: 2.4rem;
    font-weight: 800; margin: 0 0 .3rem 0; letter-spacing: -1px;
}
.header-band p { color: #8BAFC2; font-size: .95rem; margin: 0; }

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
    background: #0B1F2E; color: #E8FF4A;
    font-size: .72rem; font-weight: 700;
    padding: .2rem .55rem; border-radius: 4px;
    margin: .3rem .2rem 0 0;
    font-family: 'Space Mono', monospace;
}
.tag-vulnerable { background: #C0392B; color: #fff; }

.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.metric-box {
    flex: 1; background: #0B1F2E;
    border-radius: 10px; padding: 1.1rem 1.4rem; text-align: center;
}
.metric-box .num { color: #E8FF4A; font-size: 2rem; font-weight: 800; }
.metric-box .lbl { color: #8BAFC2; font-size: .78rem; margin-top: .2rem; }

.match-card {
    background: #EAF9F1;
    border-left: 4px solid #27AE60;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: .8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Init DB ───────────────────────────────────────────────────────────────────
try:
    init_db()
except RuntimeError as e:
    st.error(f"Error crítico al iniciar la base de datos: {e}")
    st.stop()

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "inicio"

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏙️ Ciudad Lab")
    st.markdown("---")
    nav = {
        "🏠 Inicio": "inicio",
        "📋 Proyectos": "proyectos",
        "➕ Registrar proyecto": "nuevo_proyecto",
        "🤝 Actores": "actores",
        "➕ Registrar actor": "nuevo_actor",
        "🔗 Matching": "matching",
    }
    for etiqueta, clave in nav.items():
        if st.button(etiqueta, use_container_width=True):
            st.session_state.page = clave

# ── Router ────────────────────────────────────────────────────────────────────
pagina = st.session_state.page

if pagina == "inicio":
    inicio.render()
elif pagina == "proyectos":
    proyectos.render()
elif pagina == "nuevo_proyecto":
    nuevo_proyecto.render()
elif pagina == "actores":
    actores.render()
elif pagina == "nuevo_actor":
    nuevo_actor.render()
elif pagina == "matching":
    matching_ui.render()
else:
    st.error(f"Página '{pagina}' no reconocida.")
