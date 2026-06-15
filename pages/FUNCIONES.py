import streamlit as st
st.markdown("Teclado Matemático")
if "input_texto" not in st.session_state:
    st.session_state.input_texto = ""
simbolos = [
    "x²", "xⁿ", "log", "√", "∛", "≤", "≥", "÷",
    "∫", "lim", "∑", "∞", "π", "θ", "f(x)"
]
cols = st.columns(8)
for i, simb in enumerate(simbolos):
    col_actual = cols[i % 8] 
    if col_actual.button(simb, key=f"btn_{simb}_{i}"):
        st.session_state.input_texto += simb
if st.button("Borrar todo"):
    st.session_state.input_texto = ""
# Nota: Usamos value=st.session_state.input_texto para sincronizarlo
problema = st.text_input(
    "Ingrese un problema", 
    value=st.session_state.input_texto,
    key="campo_problema"
)
if problema != st.session_state.input_texto:
    st.session_state.input_texto = problema
if st.button("Ir", type="primary"):
    st.write(f"Procesando: {problema}")


