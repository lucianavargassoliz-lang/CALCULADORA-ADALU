import streamlit as st
from styles import apply_styles
import base64
st.image("imagen2.jpeg", width=400)


st.set_page_config(
    page_title="SmartFunctions",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_styles()



st.title("Smart Functions")
st.subheader("Cada Funcion Cuenta una Historia; Nosotros te Ayudamos a Leerla!")
st.write("Bienvenido a SmartFunctions, tu calculadora de cálculo diferencial e integral. Escribe cualquier función, elige derivadas o integrales, y te mostramos el procedimiento completo: cada regla aplicada, cada paso justificado, hasta llegar al resultado final.")


st.markdown("""
<h2 style="
    font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:700;
    letter-spacing:0.1em; text-transform:uppercase; color:#9384A0; margin:0 0 22px 0;
">Módulos disponibles</h2>
""", unsafe_allow_html=True)

cards = [
    ("∂", "Derivadas", "Reglas de derivación explicadas: potencia, cadena, producto y cociente.", "#8B5FBF", "#F3ECF7", "/DERIVADAS"),
    ("∫", "Integrales", "Resolución por sustitución con procedimiento completo y verificación.", "#B9779E", "#FBEFF3", "/INTEGRALES"),
    ("f(x)", "Funciones", "Dominio, rango, intersecciones y comportamiento de cualquier función.", "#C58A4F", "#FBF1E5", "/FUNCIONES"),
]

cols = st.columns(3)
for col, (icon, title, desc, color, bg, link) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <a href="{link}" target="_self" style="text-decoration:none;">
        <div style="
            background:{bg}; border:1.5px solid {color}33; border-radius:16px;
            padding:26px 22px; height:100%; transition:all 0.2s;
            box-shadow:0 2px 8px rgba(46,36,53,0.04);
        ">
            <div style="
                font-size:1.5rem; font-family:'Fraunces',serif; font-weight:600;
                color:{color}; margin-bottom:14px;
            ">{icon}</div>
            <div style="
                font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:700;
                color:#2E2435; margin-bottom:8px;
            ">{title}</div>
            <div style="
                font-family:'Space Grotesk',sans-serif; font-size:0.83rem;
                color:#6B5C75; line-height:1.6;
            ">{desc}</div>
        </div>
        </a>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif;font-size:0.78rem;color:#B2A4BC;
            text-align:center;padding:6px 0 20px;">
    SmartFunctions · Calculadora educativa de cálculo
</div>
""", unsafe_allow_html=True)