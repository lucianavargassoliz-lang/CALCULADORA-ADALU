import streamlit as st
import numpy as np
import sympy as sp 
from logic.funciones import generar_funciones_derivada
st.sidebar.image("imagen1.jpeg", use_container_width=True)
st.sidebar.title("Menu principal")
pagina = st.sidebar.radio(
    "Navegacion",
    ["Como usar...", "Funciones", "Derivadas", "Integrales por Metodo por Sustitucion"]
)

if pagina == "Como usar...":
    st.image("imagen1.jpeg", width=400)
    st.header("Cada función cuenta una historia Y nosotros te ayudamos a leerla!!")
    
    st.write(
        "¡DOMINA EL CALCULO SIN COMPLICACIONES CON SMARTFUNCTIONES! "
        "Esta calculadora educativa es la herramienta definitiva para estudiantes de ciencias, "
        "ingeniería y matemáticas que buscan simplificar su vida académica. Olvídate de los dolores de cabeza: "
        "nuestra aplicación está completamente especializada en resolver funciones complejas, derivadas precisas e integrales "
        "mediante el método de sustitución. Más que una simple calculadora, es el tutor digital que necesitas para entender cada ejercicio, "
        "optimizar tu tiempo de estudio y asegurar tus calificaciones más altas. ¡Lleva tus habilidades matemáticas al siguiente nivel hoy mismo!"
    )
##FUNCIONES 

elif pagina == "Funciones":
    st.image("imagen1.jpeg", width=400)
    st.header("Módulo de Funciones")
    st.text_input("Ingrese su funcion")
    st.button("CALCULAR ahora ")

# luciana
#hola 


##DERIVADAS
elif pagina == "Derivadas":
    st.image("imagen1.jpeg", width=400)
    st.header("Módulo de Derivadas")
    st.write()





##INTEGRALES POR EL METODO DE SUSTITUCION 
elif pagina == "Integrales por Metodo por Sustitucion":
    st.image("imagen1.jpeg", width=400)
    st.header("Módulo de Integrales")
    st.write()
    
