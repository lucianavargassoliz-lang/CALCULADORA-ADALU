import streamlit as st
import numpy as np
from logic.funciones_f import calcular_funcion, graficar_funcion, tabla_valores
from styles import apply_styles
import io
from matplotlib.backends.backend_pdf import PdfPages
apply_styles()
st.image("imagen2.jpeg", width=400)
if "teclado_grafica" not in st.session_state:
    st.session_state.teclado_grafica = ""
def ingrese_simbolo(simbolo):
    conversiones = {
        "x²":  "x^2",
        "x³":  "x^3",
        "xⁿ":  "x^n",
        "|x|": "|x|",
        "bˣ":  "b**x",
    }
    st.session_state.teclado_grafica += conversiones.get(simbolo, simbolo)
def borrar_todo():
    st.session_state.teclado_grafica = ""

st.title("GRAFICADOR DE FUNCIONES")
col_izquierda, col_derecha = st.columns([1, 1.2])
with col_izquierda:
    st.text_input(
        "INGRESE LA FUNCIÓN QUE DESEE GRAFICAR",
        key="teclado_grafica",
    )
    numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
    letras  = ["x", "y", "z", "w", "v", "i"]
    signos  = [
        "+", "-", "*", "/", "=", "%",
        "[]", "<", ">", "(", ")",
        "÷", "±",
        "x²", "x³", "xⁿ",
        "log", "ln",
        "√", "∛",
        "≤", "≥",
        "∫", "lim", "∑",
        "∞", "π", "θ",
        "eˣ",
        "bˣ",
        "|x|",
        "sin", "cos", "tan", "tg",
        "∠", "∥",
    ]
    tecla_numeros, tecla_letras, tecla_signos = st.tabs(["1,2,3", "x,y,z", "+,-,*"])
    with tecla_numeros:
        cols_num = st.columns(4)
        for i, num in enumerate(numeros):
            cols_num[i % 4].button(num, key=f"num_{num}_{i}",
                                   on_click=ingrese_simbolo, args=(num,))
    with tecla_letras:
        cols_let = st.columns(2)
        for i, let in enumerate(letras):
            cols_let[i % 2].button(let, key=f"let_{let}_{i}",
                                   on_click=ingrese_simbolo, args=(let,))
    with tecla_signos:
        cols_sig = st.columns(5)
        for i, sig in enumerate(signos):
            cols_sig[i % 5].button(sig, key=f"sig_{sig}_{i}",
                                   on_click=ingrese_simbolo, args=(sig,))
    st.write("")
    col_borrar, col_graficar = st.columns([1, 2])
    with col_borrar:
        st.button("BORRAR", on_click=borrar_todo)
    with col_graficar:
        btn_graficar = st.button("GRAFICAR", type="primary")
with col_derecha:
    st.subheader("PLANO CARTESIANO")
    with st.expander("", expanded=False):
        x_min, x_max = st.slider("Rango X", -50, 50, (-15, 15), step=1)
    texto = st.session_state.teclado_grafica.strip()
    if btn_graficar and texto:
        try:
            expr_py, tipo = calcular_funcion(texto)
            st.success(f"✓ {tipo}: `{texto}`")
            figura = graficar_funcion(expr_py, texto, x_min, x_max)
            st.pyplot(figura)
            # PDF
            buf = io.BytesIO()
            with PdfPages(buf) as pdf:
             pdf.savefig(figura, bbox_inches="tight")

            buf.seek(0)
            pdf_bytes = buf.read()
            #boton
            st.download_button(
    label="Descargar gráfica en PDF",
    data=pdf_bytes,
    file_name="grafica_funcion.pdf",
    mime="application/pdf"
)

            if st.checkbox("Mostrar tabla de valores"):
                df = tabla_valores(expr_py, x_min, x_max)
                st.dataframe(df, use_container_width=True, hide_index=True)
        except Exception as ex:
            st.error(f"No se pudo interpretar la función: {ex} — revisa la escritura.")
    elif not texto:
        st.info("INGRESA LA FUNCIÓN QUE DESEAS GRAFICAR")


