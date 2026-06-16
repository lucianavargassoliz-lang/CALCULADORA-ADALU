import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import re
st.set_page_config(layout="wide")
st.title("GRAFICADOR DE FUNCIONES")
st.image("imagen1.jpeg", width=250)
if "teclado_grafica" not in st.session_state:
    st.session_state.teclado_grafica = ""
def ingrese_simbolo(simbolo):
    if simbolo == "x²":
        st.session_state.teclado_grafica += "x^2"
    else:
        st.session_state.teclado_grafica += simbolo
def borrar_todo():
    st.session_state.teclado_grafica = ""
col_izquierda, col_derecha = st.columns([1, 1.2])
with col_izquierda:
    problema = st.text_input(
        "INGRESE LA FUNCIÓN QUE DESEE GRAFICAR",
        key="teclado_grafica",
    )
    numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
    letras = ["x", "y","z","w","v","i"]
    signos = [ "+", "-", "*", "/", "=","%","[]","<", ">", "(", ")", "÷", "±",
    "x²", "x³", "xⁿ", "log", "√", "∛", "≤", "≥",
    "∫", "lim", "∑", "∞", "π", "θ", "eˣ", "sin", "cos", "tan"
    , "∠", "∥"]
                  
    tecla_num, tecla_let, tecla_sig = st.tabs(["1,2,3", "x,y,z", "+,-,*"])
    with tecla_num:
        cols_num = st.columns(4)
        for i, num in enumerate(numeros):
            cols_num[i % 4].button(num, key=f"num_{num}_{i}", on_click=ingrese_simbolo, args=(num,))
    with tecla_let:
        cols_let = st.columns(2)
        for i, let in enumerate(letras):
            cols_let[i % 2].button(let, key=f"let_{let}_{i}", on_click=ingrese_simbolo, args=(let,))
    with tecla_sig:
        cols_sig = st.columns(5)
        for i, sig in enumerate(signos):
            cols_sig[i % 5].button(sig, key=f"sig_{sig}_{i}", on_click=ingrese_simbolo, args=(sig,))
    st.write("")
    col_borrar, col_ir = st.columns([1, 2])
    with col_borrar:
        st.button("Borrar todo", on_click=borrar_todo)
#Procesamiento matemático 
with col_derecha:
    st.subheader("PLANO CARTESIANO")
    m, b = 1.0, 0.0
    texto_funcion = st.session_state.teclado_grafica.strip().replace(" ", "")
    if texto_funcion:
        if texto_funcion.startswith("y="):
            texto_funcion = texto_funcion.replace("y=", "")
        try:
            # Procesador básico por expresiones regulares para identificar mx + b
            # Busca patrones como: 2x+3, -x-5, .5x, 4x, 3, etc.
            match = re.match(r'^([+-]?\d*\.?\d*)?x?([+-]\d*\.?\d*)?$', texto_funcion)
            if match and ('x' in texto_funcion or texto_funcion == ""):
                str_m, str_b = match.groups()
                if str_m == "" or str_m == "+": m = 1.0
                elif str_m == "-": m = -1.0
                elif str_m is not None: m = float(str_m)
                # Extraer b (intersección)
                if str_b is not None: b = float(str_b)
                else: b = 0.0
                st.success(f"Línea detectada de forma exitosa: $y = {m}x + {b}$")
            else:
                st.warning("Ecuación no lineal o compleja detectada. Usando valores temporales.")
        except Exception as e:
            st.error("Error al procesar la entrada matemática.")
    x = np.linspace(-15, 15, 400)
    y = m * x + b
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.plot(x, y, color="#5c1b1b", linewidth=2.5, label=f"y = {m}x + {b}")
    ax.axhline(0, color='black', linewidth=1.2)  
    ax.axvline(0, color='black', linewidth=1.2)  
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.grid(True, which='both', color='lightgray', linestyle='-', linewidth=0.)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    st.pyplot(fig)


