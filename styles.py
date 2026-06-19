"""
styles.py — Importa esto al inicio de cada página con:
    from styles import apply_styles
    apply_styles()

Paleta — "Glicina" (morado pastel sobre crema cálido)
  --bg        #FBF7F4   fondo principal, crema muy claro
  --bg-soft   #F3ECF7   panel suave (lila muy pálido)
  --surface   #FFFFFF   tarjetas / inputs
  --lilac     #C9A9E0   acento secundario (botones hover, bordes)
  --violet    #8B5FBF   acento primario (botones, links, foco)
  --violet-d  #6B3FA0   acento primario oscuro (hover de primario)
  --ink       #2E2435   texto principal (morado casi negro, no gris puro)
  --ink-soft  #6B5C75   texto secundario
"""
import streamlit as st

def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #FBF7F4;
    --bg-soft: #F3ECF7;
    --surface: #FFFFFF;
    --lilac: #C9A9E0;
    --violet: #8B5FBF;
    --violet-d: #6B3FA0;
    --ink: #2E2435;
    --ink-soft: #6B5C75;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--ink);
    font-family: 'Space Grotesk', sans-serif;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stAppViewContainer"] > .main {
    background:
        radial-gradient(ellipse 800px 400px at 15% -5%, #EFE0F8 0%, transparent 60%),
        radial-gradient(ellipse 600px 400px at 100% 10%, #FDEEE3 0%, transparent 55%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-soft) !important;
    border-right: 1px solid #E4D4EF;
}
[data-testid="stSidebar"] * {
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebarNav"] a {
    color: var(--ink-soft) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    padding: 7px 12px !important;
    border-radius: 8px;
    transition: color 0.2s, background 0.2s;
}
[data-testid="stSidebarNav"] a:hover {
    color: var(--violet-d) !important;
    background: #E8D9F2 !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: var(--violet-d) !important;
    background: #fff !important;
    border-left: 3px solid var(--violet);
    box-shadow: 0 1px 3px rgba(139,95,191,0.15);
}

/* ── Títulos ── */
h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em;
    color: var(--ink) !important;
}
h1 { font-size: 2.2rem !important; }

/* ── Texto general / markdown ── */
p, span, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--ink);
}
[data-testid="stCaptionContainer"] {
    color: var(--ink-soft) !important;
}

/* ── Botones ── */
.stButton > button {
    background: var(--surface) !important;
    color: var(--ink-soft) !important;
    border: 1.5px solid #E4D4EF !important;
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    box-shadow: 0 1px 2px rgba(139,95,191,0.06) !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #F6EEFB !important;
    border-color: var(--lilac) !important;
    color: var(--violet-d) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(139,95,191,0.18) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--violet), #A47FCB) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(139,95,191,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--violet-d), var(--violet)) !important;
    box-shadow: 0 6px 22px rgba(139,95,191,0.45) !important;
    transform: translateY(-2px);
}

/* ── Inputs ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid #E4D4EF !important;
    border-radius: 10px !important;
    color: var(--ink) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.98rem !important;
    padding: 11px 14px !important;
    box-shadow: inset 0 1px 2px rgba(139,95,191,0.05) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px rgba(139,95,191,0.18) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #B9ACC4 !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: var(--violet-d) !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-soft) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--ink-soft) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.03em !important;
    padding: 7px 18px !important;
    transition: all 0.15s !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--violet-d) !important;
    box-shadow: 0 1px 4px rgba(139,95,191,0.18) !important;
}

/* ── Alertas ── */
.stSuccess > div {
    background: #EAF7EE !important;
    border: 1.5px solid #7DC796 !important;
    border-radius: 12px !important;
    color: #1F7A3D !important;
}
.stWarning > div {
    background: #FDF3E3 !important;
    border: 1.5px solid #E3AE52 !important;
    border-radius: 12px !important;
    color: #8A5B0B !important;
}
.stError > div {
    background: #FCE9EA !important;
    border: 1.5px solid #E08A8F !important;
    border-radius: 12px !important;
    color: #A6353C !important;
}
.stInfo > div {
    background: #F0E6FA !important;
    border: 1.5px solid var(--lilac) !important;
    border-radius: 12px !important;
    color: var(--violet-d) !important;
}

/* ── Divisor ── */
hr { border: none !important; border-top: 1.5px solid #E8DCF1 !important; margin: 2rem 0 !important; }

/* ── Blockquote ── */
blockquote {
    border-left: 3px solid var(--violet) !important;
    background: var(--bg-soft) !important;
    padding: 10px 16px !important;
    border-radius: 0 10px 10px 0 !important;
    color: var(--violet-d) !important;
    font-style: italic;
}

/* ── Code ── */
code {
    background: #EFE2F7 !important;
    color: var(--violet-d) !important;
    border-radius: 5px !important;
    padding: 2px 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88em !important;
}

/* ── LaTeX ── */
.katex { color: var(--ink) !important; font-size: 1.05em !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 7px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--lilac); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--violet); }
</style>
""", unsafe_allow_html=True)
