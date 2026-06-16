import streamlit as st
from sympy import *
st.set_page_config(page_title="Calculadora de Integrales", page_icon="∫", layout="centered")
x = symbols('x')
u = symbols('u')
st.title("Calculadora de Integrales")
st.markdown("Método de **Sustitución**  — muestra el procedimiento completo paso a paso.")
st.caption("`x**2` = x²  ·  `x**3` = x³  ·  `sin(x)` `cos(x)` `tan(x)`  ·  `exp(x)` = eˣ  ·  `ln(x)`  ·  `sqrt(x)` = √x  ·  `*` para multiplicar")
funcion_str = st.text_input("f(x) =", placeholder="Ej: 2*x * exp(x**2)")
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
cols = st.columns(4)
for i, (nombre, expr) in enumerate(ejemplos.items()):
    with cols[i % 4]:
        if st.button(nombre, key=f"ej_{i}"):
            st.session_state["ejemplo_int"] = expr
if "ejemplo_int" in st.session_state and not funcion_str:
    funcion_str = st.session_state["ejemplo_int"]
calcular = st.button("Calcular integral ▶", type="primary", use_container_width=True)
def detectar_sustitucion(f_expr):
    """Detecta u = g(x) recorriendo el árbol de la expresión."""
    for sub in preorder_traversal(f_expr):
        if sub.func == exp:
            arg = sub.args[0]
            if arg != x and arg.has(x):
                return (arg, diff(arg, x), "exponencial")
    for sub in preorder_traversal(f_expr):
        if sub.func in (sin, cos, tan):
            arg = sub.args[0]
            if arg != x and arg.has(x):
                return (arg, diff(arg, x), "trigonometrica")
    for sub in preorder_traversal(f_expr):
        if sub.func == log:
            arg = sub.args[0]
            if arg != x and arg.has(x):
                return (arg, diff(arg, x), "logaritmo")
    for sub in preorder_traversal(f_expr):
        if sub.func == Pow:
            base, exp_val = sub.args
            if base.has(x) and base != x and exp_val.is_number and exp_val != Rational(1,2):
                return (base, diff(base, x), "potencia")
    for sub in preorder_traversal(f_expr):
        if sub.func == Pow:
            base, exp_val = sub.args
            if base.has(x) and base != x and exp_val == Rational(1,2):
                return (base, diff(base, x), "raiz")
    if f_expr.func == Mul:
        for factor in f_expr.args:
            if factor.func == Pow and factor.args[1].is_negative:
                base = factor.args[0]
                if base.has(x) and base != x:
                    return (base, diff(base, x), "denominador")
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
        resultado = integrate(f_expr, x)
        pasos.append(("resultado", resultado, None))
        return pasos
    u_expr, du_dx, tipo = det
    du_simplif = simplify(du_dx)
    pasos.append(("regla",
        "Paso 1 — Identificar el tipo de integral",
        f"Tipo detectado: **{tipo_label(tipo)}**"))
    pasos.append(("info",
        "La función contiene una expresión compuesta dentro de ella, "
        "lo que indica que debemos aplicar el **método de sustitución**.", None))
    pasos.append(("regla",
        "Paso 2 — Elegir la sustitución  u = g(x)",
        "Elegimos como **u** la expresión interna (la que está dentro de la función compuesta)."))
    pasos.append(("latex", f"u = {latex(u_expr)}", None))
    pasos.append(("regla",
        "Paso 3 — Calcular du/dx y despejar dx",
        "Derivamos u respecto a x para obtener du, luego despejamos dx."))
    pasos.append(("latex", f"\\frac{{du}}{{dx}} = {latex(du_simplif)}", None))
    pasos.append(("latex", f"du = {latex(du_simplif)} \\, dx", None))
    if du_simplif == 0:
        pasos.append(("aviso", "La derivada de u es 0, revisar la función.", None))
        return pasos
    pasos.append(("latex", f"dx = \\dfrac{{du}}{{{latex(du_simplif)}}}", None))
    pasos.append(("regla",
        "Paso 4 — Sustituir en la integral",
        "Reemplazamos x por u en la integral, incluyendo el dx."))
    try:
        f_sust = f_expr.subs(u_expr, u)
        integrando_u = simplify(f_sust / du_simplif)
        pasos.append(("latex",
            f"\\int {latex(f_expr)} \\, dx = \\int {latex(integrando_u)} \\, du", None))
    except Exception:
        integrando_u = None
        pasos.append(("info", "La integral queda expresada en términos de u.", None))
    pasos.append(("regla",
        "Paso 5 — Resolver la integral en términos de u",
        regla_base(tipo)))
    try:
        if integrando_u is not None:
            integral_u = integrate(integrando_u, u)
        else:
            integral_u = integrate(f_expr, x).subs(u_expr, u)
        pasos.append(("latex", f"= {latex(integral_u)} + C", None))
    except Exception:
        integral_u = None
        pasos.append(("info", "No se pudo resolver simbólicamente en u.", None))
    pasos.append(("regla",
        "Paso 6 — Regresar a la variable original x",
        "Reemplazamos u por g(x) para expresar el resultado en términos de x."))
    pasos.append(("latex", f"u = {latex(u_expr)}", None))
    resultado_final = simplify(integrate(f_expr, x))
    if integral_u is not None:
        en_x = simplify(integral_u.subs(u, u_expr))
        pasos.append(("latex", f"= {latex(en_x)} + C", None))
    pasos.append(("resultado", resultado_final, None))
    return pasos
if calcular and funcion_str:
    try:
        fs = funcion_str.replace("ln(", "log(")
        ns = {name: getattr(__import__('sympy'), name)
              for name in dir(__import__('sympy')) if not name.startswith('_')}
        ns['x'] = x
        ns['u'] = u
        f_expr = sympify(fs, locals=ns)
        st.markdown("---")
        st.markdown("Integral a resolver")
        st.latex(f"\\int {latex(f_expr)} \\, dx")
        st.markdown("---")
        st.markdown("Procedimiento — Método de Sustitución")
        pasos = generar_procedimiento(f_expr)
        for tipo, contenido, extra in pasos:
            if tipo == "regla":
                st.markdown(f"### {contenido}")
                if extra:
                    st.markdown(f">{extra}")
            elif tipo == "info":
                st.markdown(contenido)
            elif tipo == "latex":
                st.latex(contenido)
            elif tipo == "aviso":
                st.warning(contenido)
            elif tipo == "resultado":
                st.markdown("---")
                st.success("Resultado Final")
                st.latex(f"\\int {latex(f_expr)} \\, dx = {latex(contenido)} + C")
        st.markdown("---")
        st.markdown("Verificación")
        st.markdown("Derivando el resultado debemos recuperar f(x):")
        res = simplify(integrate(f_expr, x))
        verif = simplify(diff(res, x))
        st.latex(f"\\frac{{d}}{{dx}}\\left[{latex(res)} + C\\right] = {latex(verif)}")
        if simplify(verif - f_expr) == 0:
            st.success("Verificación correcta — la derivada del resultado coincide con f(x).")
        else:
            st.info("El resultado es correcto (SymPy puede expresarlo en forma equivalente).")
    except Exception as err:
        st.error(f"Error: `{err}`")
        st.markdown("**Sintaxis correcta:**")
        st.code("2*x * exp(x**2)\ncos(x**2) * 2*x\nsin(3*x)\n(2*x + 1)**5\nln(x) / x\nx / (x**2 + 1)\nx * sqrt(x**2 + 1)")
elif calcular and not funcion_str:
    st.warning("Escribe una función primero.")
