"""
_brand.py — inyección de sistema visual CityLab en Streamlit.
Llama inject_brand() como primera línea de cada página UI.
"""

import streamlit as st


def inject_brand() -> None:
    """Inyecta CSS global con tokens de marca CityLab."""
    st.markdown("""
    <style>
    /* ── Fuentes ─────────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&family=DM+Mono:wght@400&display=swap');

    /* ── Tokens ──────────────────────────────────────────────────────────── */
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

        --sp-1:  4px;
        --sp-2:  8px;
        --sp-3:  12px;
        --sp-4:  16px;
        --sp-6:  24px;
        --sp-8:  32px;
        --sp-12: 48px;
        --sp-16: 64px;

        --radius-sm: 2px;
        --radius-md: 6px;
        --radius-lg: 12px;

        --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
        --shadow-md: 0 4px 16px rgba(0,0,0,.10);
        --shadow-lg: 0 12px 40px rgba(0,0,0,.14);

        --max-width: 1280px;
    }

    /* ── Base ────────────────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: var(--font-body);
        background-color: var(--color-bg);
        color: var(--color-text);
    }

    /* ── Sidebar ─────────────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background-color: var(--color-primary) !important;
        border-right: none;
    }
    section[data-testid="stSidebar"] * {
        color: #FAFAF8 !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        color: #FAFAF8 !important;
        border: 1px solid rgba(255,255,255,.15) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
        font-size: .85rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        padding: var(--sp-3) var(--sp-4) !important;
        transition: background .15s, border-color .15s;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(232,67,122,.18) !important;
        border-color: var(--color-accent) !important;
    }

    /* ── Botones primarios ───────────────────────────────────────────────── */
    .stButton > button {
        background-color: var(--color-primary) !important;
        color: var(--color-bg) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
        font-size: .9rem !important;
        font-weight: 500 !important;
        padding: var(--sp-3) var(--sp-6) !important;
        letter-spacing: .01em;
        transition: background .15s, transform .1s;
    }
    .stButton > button:hover {
        background-color: #2A2A2A !important;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* ── Inputs de texto ─────────────────────────────────────────────────── */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: var(--color-surface) !important;
        border: 1px solid var(--color-border) !important;
        border-radius: var(--radius-md) !important;
        font-family: var(--font-body) !important;
        font-size: .9rem !important;
        color: var(--color-text) !important;
        padding: var(--sp-3) var(--sp-4) !important;
        transition: border-color .15s;
    }
    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 2px rgba(13,13,13,.08) !important;
        outline: none !important;
    }

    /* ── Labels de form ──────────────────────────────────────────────────── */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stMultiSelect label,
    .stCheckbox label {
        font-family: var(--font-body) !important;
        font-size: .8rem !important;
        font-weight: 500 !important;
        letter-spacing: .04em !important;
        text-transform: uppercase !important;
        color: var(--color-muted) !important;
    }

    /* ── Forms ───────────────────────────────────────────────────────────── */
    [data-testid="stForm"] {
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--sp-8) !important;
    }

    /* ── Headers ─────────────────────────────────────────────────────────── */
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
        font-weight: 700 !important;
        color: var(--color-primary) !important;
    }
    h3 {
        font-family: var(--font-body) !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        color: var(--color-primary) !important;
    }

    /* ── Hero band ───────────────────────────────────────────────────────── */
    .cl-hero {
        background: var(--color-primary);
        padding: var(--sp-12) var(--sp-8) var(--sp-8);
        border-radius: var(--radius-lg);
        margin-bottom: var(--sp-8);
    }
    .cl-hero h1 {
        color: var(--color-bg) !important;
        font-size: 3rem !important;
        max-width: 600px;
        line-height: 1.08 !important;
    }
    .cl-hero p {
        color: #9A9A9A;
        font-size: .95rem;
        margin: var(--sp-4) 0 0;
    }
    .cl-hero .cl-cta {
        display: inline-block;
        margin-top: var(--sp-6);
        font-family: var(--font-body);
        font-size: .85rem;
        color: var(--color-bg);
        opacity: .7;
        letter-spacing: .03em;
    }

    /* ── Cards de proyecto ───────────────────────────────────────────────── */
    .cl-card {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--sp-6);
        margin-bottom: var(--sp-4);
        transition: box-shadow .2s, transform .15s;
    }
    .cl-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    .cl-card h3 {
        margin: 0 0 var(--sp-2) 0;
        font-size: 1rem;
        font-weight: 500;
    }
    .cl-card p {
        margin: 0;
        color: var(--color-muted);
        font-size: .875rem;
        line-height: 1.5;
    }

    /* ── Tags ────────────────────────────────────────────────────────────── */
    .cl-tag {
        display: inline-block;
        background: var(--color-surface);
        color: var(--color-text);
        border: 1px solid var(--color-border);
        font-family: var(--font-mono);
        font-size: .72rem;
        padding: 2px 8px;
        border-radius: var(--radius-sm);
        margin: var(--sp-2) var(--sp-1) 0 0;
        letter-spacing: .02em;
    }
    .cl-tag-vuln {
        background: #FFF0F3;
        color: var(--color-accent);
        border-color: #F7C0CF;
    }

    /* ── Métricas ────────────────────────────────────────────────────────── */
    .cl-metric-row {
        display: flex;
        gap: var(--sp-4);
        margin-bottom: var(--sp-8);
        flex-wrap: wrap;
    }
    .cl-metric-box {
        flex: 1;
        min-width: 120px;
        background: var(--color-surface);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--sp-6) var(--sp-8);
        text-align: center;
    }
    .cl-metric-box .cl-num {
        font-family: var(--font-header);
        font-size: 2.4rem;
        font-weight: 700;
        color: var(--color-primary);
        line-height: 1;
    }
    .cl-metric-box .cl-lbl {
        font-family: var(--font-body);
        font-size: .75rem;
        font-weight: 500;
        color: var(--color-muted);
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-top: var(--sp-2);
    }

    /* ── Match card ──────────────────────────────────────────────────────── */
    .cl-match-card {
        background: var(--color-bg);
        border: 1px solid var(--color-border);
        border-left: 3px solid var(--color-accent);
        border-radius: var(--radius-md);
        padding: var(--sp-4) var(--sp-6);
        margin-bottom: var(--sp-3);
    }

    /* ── Número de índice (estilo editorial) ─────────────────────────────── */
    .cl-index {
        font-family: var(--font-mono);
        font-size: .75rem;
        color: var(--color-muted);
        letter-spacing: .05em;
    }

    /* ── Divisor ─────────────────────────────────────────────────────────── */
    hr {
        border: none;
        border-top: 1px solid var(--color-border);
        margin: var(--sp-8) 0;
    }

    /* ── Caption / helper text ───────────────────────────────────────────── */
    small, .stCaption {
        font-family: var(--font-body) !important;
        font-size: .78rem !important;
        color: var(--color-muted) !important;
    }

    /* ── Ocultar decoración Streamlit ────────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)
