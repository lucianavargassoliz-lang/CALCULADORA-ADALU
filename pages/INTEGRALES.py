import streamlit as st
import sympy as sp
from styles import apply_styles
import numpy as np
import matplotlib.pyplot as plt
##
def graficar_integral_indefinida(funcion_texto, x_min, x_max):
    try:
        x = sp.Symbol('x')
        funcion = sp.sympify(funcion_texto)
        integral = sp.integrate(funcion, x)

        f = sp.lambdify(x, funcion, "numpy")
        F = sp.lambdify(x, integral, "numpy")

        valores_x = np.linspace(x_min, x_max, 400)
        valores_y = f(valores_x)
        valores_F = F(valores_x)
        fig, ax = plt.subplots()

        ax.plot(valores_x, valores_y, label="f(x)")
        ax.plot(valores_x, valores_F, label="F(x)", linestyle="--")
        ##para area sombreada
        ax.fill_between(valores_x, valores_y, alpha=0.3)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        ##pdf
        import io
        buf = io.BytesIO()
        fig.savefig(buf, format="pdf", bbox_inches="tight")
        buf.seek(0)
        st.download_button(
    label="Descargar gráfica en PDF",
    data=buf,
    file_name="grafica_integral.pdf",
    mime="application/pdf"
)
    except:
        st.warning("UPS NO SE PUDO GRAFICAR")
##grafica

apply_styles()

x = sp.symbols('x')
u = sp.symbols('u')

st.title("Calculadora de Integrales")
st.markdown("Método de **Sustitución** — muestra el procedimiento completo paso a paso.")
st.caption("`x**2` = x²  ·  `x**3` = x³  ·  `sin(x)` `cos(x)` `tan(x)`  ·  `exp(x)` = eˣ  ·  `ln(x)`  ·  `*` para multiplicar")

if "funcion_input" not in st.session_state:
    st.session_state["funcion_input"] = ""

if "funcion_valor" not in st.session_state:
    st.session_state.funcion_valor = ""
def insertar_simbolo(simbolo):
    if simbolo == "x²":
        st.session_state["funcion_input"] += "x^2"
    else:
        st.session_state["funcion_input"] += simbolo

def borrar_todo():
    st.session_state["funcion_input"] = ""

def cargar_ejemplo(expr):
    st.session_state["funcion_input"] = expr

# Input de texto enlazado al session_state
funcion_str = st.text_input(
    "INGRESE LA FUNCIÓN QUE DESEE GRAFICAR / INTEGRAR",
    key="funcion_input",
    placeholder="Ej: 2*x * exp(x**2)",
)

st.markdown("**Teclado Matemático**")

numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
letras  = ["x", "y", "z", "w", "v", "i"]
signos  = ["+", "-", "*", "/", "=", "%", "[]", "<", ">", "(", ")", "÷", "±",
           "x²", "x³", "xⁿ", "log", "√", "∛", "≤", "≥",
           "∫", "lim", "∑", "∞", "π", "θ", "eˣ", "sin", "cos", "tan",
           "∠", "∥"]

tab_num, tab_let, tab_sig = st.tabs(["1,2,3", "x,y,z", "+,-,*"])

with tab_num:
    cols_num = st.columns(4) 
    for i, num in enumerate(numeros):
        cols_num[i % 4].button(num, key=f"num_int_{num}_{i}", 
                               on_click=insertar_simbolo, args=(num,))

with tab_let:
    cols_let = st.columns(2) 
    for i, let in enumerate(letras):
        cols_let[i % 2].button(let, key=f"let_int_{let}_{i}", 
                               on_click=insertar_simbolo, args=(let,))

with tab_sig:
    cols_sig = st.columns(5) 
    for i, sig in enumerate(signos):
        cols_sig[i % 5].button(sig, key=f"sig_int_{sig}_{i}", 
                               on_click=insertar_simbolo, args=(sig,))

st.write("")
col_borrar, col_graficar = st.columns([1, 2])
with col_borrar:
    st.button("BORRAR", on_click=borrar_todo, key="btn_borrar_int")
with col_graficar:
    calcular = st.button("Calcular integral ▶", type="primary", use_container_width=True)

st.markdown("**Ejemplos:**")
ejemplos = {
    "2x·eˣ²":       "2*x * exp(x**2)",
    "cos(x²)·2x":   "cos(x**2) * 2*x",
    "sin(3x)":       "sin(3*x)",
    "(2x+1)⁵":      "(2*x + 1)**5",
    "ln(x)/x":       "ln(x) / x",
    "x/(x²+1)":     "x / (x**2 + 1)",
    "e^(4x)":        "exp(4*x)",
    "x·√(x²+1)":    "x * sqrt(x**2 + 1)",
}

cols_ej = st.columns(4)
for i, (nombre, expr) in enumerate(ejemplos.items()):
    with cols_ej[i % 4]:
        st.button(nombre, key=f"ej_int_{i}", on_click=cargar_ejemplo, args=(expr,))

funcion_str = st.session_state.get("funcion_input", "")

def detectar_sustitucion(f_expr):
    for sub in sp.preorder_traversal(f_expr):
        if sub.func == sp.exp:
            arg = sub.args[0]
            if arg != x and arg.has(x): return (arg, sp.diff(arg, x), "exponencial")
    for sub in sp.preorder_traversal(f_expr):
        if sub.func in (sp.sin, sp.cos, sp.tan):
            arg = sub.args[0]
            if arg != x and arg.has(x): return (arg, sp.diff(arg, x), "trigonometrica")
    for sub in sp.preorder_traversal(f_expr):
        if sub.func == sp.log:
            arg = sub.args[0]
            if arg != x and arg.has(x): return (arg, sp.diff(arg, x), "logaritmo")
    for sub in sp.preorder_traversal(f_expr):
        if sub.func == sp.Pow:
            base, exp_val = sub.args
            if base.has(x) and base != x and exp_val.is_number and exp_val != sp.Rational(1, 2):
                return (base, sp.diff(base, x), "potencia")
    for sub in sp.preorder_traversal(f_expr):
        if sub.func == sp.Pow:
            base, exp_val = sub.args
            if base.has(x) and base != x and exp_val == sp.Rational(1, 2):
                return (base, sp.diff(base, x), "raiz")
    if f_expr.func == sp.Mul:
        for factor in f_expr.args:
            if factor.func == sp.Pow and factor.args[1].is_negative:
                base = factor.args[0]
                if base.has(x) and base != x: return (base, sp.diff(base, x), "denominador")
    return None

def tipo_label(tipo):
    labels = {
        "exponencial":    "Exponencial compuesta  e^g(x)",
        "trigonometrica": "Trigonométrica compuesta",
        "logaritmo":      "Logarítmica compuesta  ln(g(x))",
        "potencia":       "Potencia compuesta  [g(x)]ⁿ",
        "raiz":           "Raíz compuesta  √g(x)",
        "denominador":    "Fracción con denominador compuesto",
    }
    return labels.get(tipo, tipo)

def regla_base(tipo):
    reglas = {
        "exponencial":    "∫ eᵘ du = eᵘ + C",
        "trigonometrica": "∫ sin(u) du = −cos(u) + C  |  ∫ cos(u) du = sin(u) + C  |  ∫ tan(u) du = −ln|cos(u)| + C",
        "logaritmo":      "∫ (1/u) du = ln|u| + C",
        "potencia":       "∫ uⁿ du = uⁿ⁺¹/(n+1) + C",
        "raiz":           "∫ √u du = (2/3)u^(3/2) + C",
        "denominador":    "∫ (1/u) du = ln|u| + C",
    }
    return reglas.get(tipo, "")

def generar_procedimiento(f_expr):
    pasos = []
    det = detectar_sustitucion(f_expr)
    if det is None:
        pasos.append(("aviso", "No se detectó sustitución evidente. Se integra directamente.", None))
        resultado = sp.integrate(f_expr, x)
        pasos.append(("resultado", resultado, None))
        return pasos
    u_expr, du_dx, tipo = det
    du_simplif = sp.simplify(du_dx)
    pasos.append(("regla", "Paso 1 — Identificar el tipo de integral", f"Tipo detectado: **{tipo_label(tipo)}**"))
    pasos.append(("info", "La función contiene una expresión compuesta dentro de ella, lo que indica que debemos aplicar el **método de sustitución**.", None))
    pasos.append(("regla", "Paso 2 — Elegir la sustitución  u = g(x)", "Elegimos como **u** la expresión interna (la que está dentro de la función compuesta)."))
    pasos.append(("latex", f"u = {sp.latex(u_expr)}", None))
    pasos.append(("regla", "Paso 3 — Calcular du/dx and despejar dx", "Derivamos u respecto a x para obtener du, luego despejamos dx."))
    pasos.append(("latex", f"\\frac{{du}}{{dx}} = {sp.latex(du_simplif)}", None))
    pasos.append(("latex", f"du = {sp.latex(du_simplif)} \\, dx", None))
    if du_simplif == 0:
        pasos.append(("aviso", "La derivada de u es 0, revisar la función.", None))
        return pasos
    pasos.append(("latex", f"dx = \\dfrac{{du}}{{{sp.latex(du_simplif)}}}", None))
    pasos.append(("regla", "Paso 4 — Sustituir en la integral", "Reemplazamos x por u en la integral, incluyendo el dx."))
    try:
        f_sust = f_expr.subs(u_expr, u)
        integrando_u = sp.simplify(f_sust / du_simplif)
        pasos.append(("latex", f"\\int {sp.latex(f_expr)} \\, dx = \\int {sp.latex(integrando_u)} \\, du", None))
    except Exception:
        integrando_u = None
        pasos.append(("info", "La integral queda expresada en términos de u.", None))
    pasos.append(("regla", "Paso 5 — Resolver la integral en términos de u", regla_base(tipo)))
    try:
        if integrando_u is not None: integral_u = sp.integrate(integrando_u, u)
        else: integral_u = sp.integrate(f_expr, x).subs(u_expr, u)
        pasos.append(("latex", f"= {sp.latex(integral_u)} + C", None))
    except Exception:
        integral_u = None
        pasos.append(("info", "No se pudo resolver simbólicamente en u.", None))
    pasos.append(("regla", "Paso 6 — Regresar a la variable original x", "Reemplazamos u por g(x) para expresar el resultado en términos de x."))
    pasos.append(("latex", f"u = {sp.latex(u_expr)}", None))
    resultado_final = sp.simplify(sp.integrate(f_expr, x))
    if integral_u is not None:
        en_x = sp.simplify(integral_u.subs(u, u_expr))
        pasos.append(("latex", f"= {sp.latex(en_x)} + C", None))
    pasos.append(("resultado", resultado_final, None))
    return pasos


if calcular and funcion_str:
    try:
        
        fs = funcion_str.replace("^", "**")
        fs = fs.replace("÷", "/").replace("−", "-").replace("–", "-").replace("—", "-")
        fs = fs.replace("ln(", "log(").replace("eˣ", "exp(x)")
        
        
        for letra in ['x', 'y', 'z', 'w', 'v', 'i', 's', 'c', 't', 'l']:
            for i in range(10):
                fs = fs.replace(f"{i}{letra}", f"{i}*{letra}")
                
        ns = {name: getattr(sp, name) for name in dir(sp) if not name.startswith('_')}
        ns['x'] = x
        ns['u'] = u
        f_expr = sp.sympify(fs, locals=ns)
        
        st.markdown("---")
        st.markdown("Integral a resolver")
        st.latex(f"\\int {sp.latex(f_expr)} \\, dx")
        st.markdown("---")
        st.markdown("Procedimiento — Método de Sustitución")
        
        pasos = generar_procedimiento(f_expr)
        for tipo, contenido, extra in pasos:
            if tipo == "regla":
                st.markdown(f"### {contenido}")
                if extra: st.markdown(f">{extra}")
            elif tipo == "info": st.markdown(contenido)
            elif tipo == "latex": st.latex(contenido)
            elif tipo == "aviso": st.warning(contenido)
            elif tipo == "resultado":
                st.markdown("---")
                st.success("Resultado Final")
                st.latex(f"\\int {sp.latex(f_expr)} \\, dx = {sp.latex(contenido)} + C")
                ##
                st.markdown("---")
                st.subheader("GRAFICA DE LA FUNCION ORIGINAL Y DE LA INTEGRAL f(x) y F(x)")

        if funcion_str.strip():
          col_s1, col_s2 = st.columns(2)
        with col_s1:
         x_min = st.slider("X mínimo:", min_value=-50, max_value=-1, value=-10, step=1)
        with col_s2:
         x_max = st.slider("X máximo:", min_value=1, max_value=50, value=10, step=1)

        graficar_integral_indefinida(funcion_str, x_min, x_max)
                ##
                
        st.markdown("---")
        st.markdown("Verificación")
        st.markdown("Derivando el resultado debemos recuperar f(x):")
        res = sp.simplify(sp.integrate(f_expr, x))
        verif = sp.simplify(sp.diff(res, x))
        st.latex(f"\\frac{{d}}{{dx}}\\left[{sp.latex(res)} + C\\right] = {sp.latex(verif)}")
        
        if sp.simplify(verif - f_expr) == 0:
            st.success("Verificación correcta — la derivada del resultado coincide con f(x).")
        else:
            st.info("El resultado es correcto (SymPy puede expresarlo en forma equivalente).")
            
    except Exception as err:
        st.error(f"Error al interpretar la expresión: `{err}` — Revisa la escritura de la función.")
        st.markdown("**Sintaxis correcta:**")
        st.code("2*x * exp(x**2)\ncos(x**2) * 2*x\nsin(3*x)\n(2*x + 1)**5")
        
elif calcular and not funcion_str:
    st.warning("Escribe una función primero.")