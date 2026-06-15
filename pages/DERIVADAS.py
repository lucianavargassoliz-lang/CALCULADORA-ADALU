import streamlit as st
from sympy import *
st.set_page_config(page_title="Calculadora de Derivadas", page_icon="∂", layout="centered")
x = symbols('x')
st.title("∂ Calculadora de Derivadas")
st.markdown("Escribe la función usando la sintaxis de Python:")
st.caption("`x**2` = x²  ·  `x**3` = x³  ·  `sin(x)` `cos(x)` `tan(x)`  ·  `exp(x)` = eˣ  ·  `ln(x)` = ln  ·  `sqrt(x)` = √x  ·  `*` para multiplicar")
funcion_str = st.text_input("f(x) =", placeholder="Ej: 3*x**2 + sin(x)")
st.markdown("**Ejemplos:**")
ejemplos = {
    "3x³ − 2x² + 5x": "3*x**3 - 2*x**2 + 5*x",
    "sin²(x) + cos(x)": "sin(x)**2 + cos(x)",
    "e^(x²)": "exp(x**2)",
    "ln(x³+1)": "ln(x**3 + 1)",
    "x²·sin(x)": "x**2 * sin(x)",
    "sin(x)/x²": "sin(x) / x**2",
    "sin(3x²+1)": "sin(3*x**2 + 1)",
}
cols = st.columns(4)
for i, (nombre, expr) in enumerate(ejemplos.items()):
    with cols[i % 4]:
        if st.button(nombre, key=f"ej_{i}"):
            st.session_state["ejemplo"] = expr
if "ejemplo" in st.session_state and not funcion_str:
    funcion_str = st.session_state["ejemplo"]
calcular = st.button("Calcular derivada ▶", type="primary", use_container_width=True)
def clasificar_expr(expr):
    reglas = []
    if isinstance(expr, Add): reglas.append("suma_resta")
    if isinstance(expr, Mul):
        args_no_num = [a for a in expr.args if not a.is_number]
        if len(args_no_num) > 1:
            tiene_neg = any(isinstance(a, Pow) and a.args[1].is_negative for a in expr.args)
            reglas.append("cociente" if tiene_neg else "producto")
    if isinstance(expr, Pow):
        base, exp_val = expr.args
        if base == x and exp_val.is_number:     reglas.append("potencia")
        elif exp_val.is_number:                  reglas.append("cadena_potencia")
        elif base.is_number:                     reglas.append("exponencial_base")
    if expr.has(sin) or expr.has(cos) or expr.has(tan): reglas.append("trigonometrica")
    if expr.has(exp):  reglas.append("exponencial_e")
    if expr.has(log):  reglas.append("logaritmo")
    if expr.has(sqrt): reglas.append("raiz")
    return list(dict.fromkeys(reglas))

def generar_pasos(expr):
    pasos = []
    def analizar(e, nivel=0):
        if isinstance(e, Add):
            pasos.append(("regla", "📘 Regla de la Suma/Resta", "Si f(x) = u ± v  →  f'(x) = u' ± v'"))
            pasos.append(("info", f"Se identifican **{len(e.args)} términos** que se derivan por separado:", None))
            for i, t in enumerate(e.args, 1):
                pasos.append(("termino", f"  Término {i}: `{t}`  →  derivada: `{diff(t, x)}`", None))
                analizar(t, nivel + 1)
        elif isinstance(e, Mul):
            args_no_num = [a for a in e.args if not a.is_number]
            tiene_neg = any(isinstance(a, Pow) and a.args[1].is_negative for a in e.args)
            if tiene_neg and len(args_no_num) >= 2:
                num_a = [a for a in e.args if not (isinstance(a, Pow) and a.args[1].is_negative and not a.args[0].is_number)]
                den_a = [Pow(a.args[0], -a.args[1]) for a in e.args if isinstance(a, Pow) and a.args[1].is_negative and not a.args[0].is_number]
                u = Mul(*num_a) if num_a else S.One
                v = Mul(*den_a) if den_a else S.One
                du, dv = diff(u, x), diff(v, x)
                pasos.append(("regla", "📙 Regla del Cociente", "Si f = u/v  →  f' = (u'v − uv') / v²"))
                pasos.append(("info", f"  u = `{u}`  →  u' = `{du}`", None))
                pasos.append(("info", f"  v = `{v}`  →  v' = `{dv}`", None))
            elif len(args_no_num) > 1:
                u, v = args_no_num[0], Mul(*args_no_num[1:])
                du, dv = diff(u, x), diff(v, x)
                pasos.append(("regla", "📗 Regla del Producto", "Si f = u·v  →  f' = u'v + uv'"))
                pasos.append(("info", f"  u = `{u}`  →  u' = `{du}`", None))
                pasos.append(("info", f"  v = `{v}`  →  v' = `{dv}`", None))
                analizar(u, nivel + 1)
                analizar(v, nivel + 1)
            else:
                analizar(args_no_num[0], nivel + 1)
        elif isinstance(e, Pow):
            base, exp_val = e.args
            if base == x and exp_val.is_number:
                pasos.append(("regla", "📕 Regla de la Potencia", "Si f = xⁿ  →  f' = n·xⁿ⁻¹"))
                pasos.append(("info", f"  x^{exp_val}  →  `{exp_val}·x^{exp_val - 1}`", None))
            elif not base.has(x) and exp_val.has(x):
                pasos.append(("regla", "📒 Exponencial base constante", "Si f = aˣ  →  f' = aˣ·ln(a)"))
            elif exp_val.is_number and base.has(x) and base != x:
                dg = diff(base, x)
                pasos.append(("regla", "🔗 Regla de la Cadena + Potencia", "Si f = [g(x)]ⁿ  →  f' = n·[g]ⁿ⁻¹·g'"))
                pasos.append(("info", f"  g(x) = `{base}`  →  g' = `{dg}`", None))
                analizar(base, nivel + 1)
        elif isinstance(e, sin):
            arg = e.args[0]
            if arg != x:
                dg = diff(arg, x)
                pasos.append(("regla", "🔗 Regla de la Cadena + sin", "Si f = sin(g)  →  f' = cos(g)·g'"))
                pasos.append(("info", f"  g(x) = `{arg}`  →  g' = `{dg}`", None))
            else:
                pasos.append(("regla", "📐 Derivada de sin(x)", "d/dx[sin(x)] = cos(x)"))
        elif isinstance(e, cos):
            arg = e.args[0]
            if arg != x:
                dg = diff(arg, x)
                pasos.append(("regla", "🔗 Regla de la Cadena + cos", "Si f = cos(g)  →  f' = −sin(g)·g'"))
                pasos.append(("info", f"  g(x) = `{arg}`  →  g' = `{dg}`", None))
            else:
                pasos.append(("regla", "📐 Derivada de cos(x)", "d/dx[cos(x)] = −sin(x)"))
        elif isinstance(e, tan):
            arg = e.args[0]
            if arg != x:
                dg = diff(arg, x)
                pasos.append(("regla", "🔗 Regla de la Cadena + tan", "Si f = tan(g)  →  f' = sec²(g)·g'"))
                pasos.append(("info", f"  g(x) = `{arg}`  →  g' = `{dg}`", None))
            else:
                pasos.append(("regla", "📐 Derivada de tan(x)", "d/dx[tan(x)] = sec²(x)"))
        elif isinstance(e, exp):
            arg = e.args[0]
            if arg != x:
                dg = diff(arg, x)
                pasos.append(("regla", "🔗 Regla de la Cadena + eˣ", "Si f = e^g  →  f' = e^g·g'"))
                pasos.append(("info", f"  g(x) = `{arg}`  →  g' = `{dg}`", None))
                analizar(arg, nivel + 1)
            else:
                pasos.append(("regla", "📗 Derivada de eˣ", "d/dx[eˣ] = eˣ"))
        elif isinstance(e, log):
            arg = e.args[0]
            if arg != x:
                dg = diff(arg, x)
                pasos.append(("regla", "🔗 Regla de la Cadena + ln", "Si f = ln(g)  →  f' = g'/g"))
                pasos.append(("info", f"  g(x) = `{arg}`  →  g' = `{dg}`", None))
                analizar(arg, nivel + 1)
            else:
                pasos.append(("regla", "📗 Derivada de ln(x)", "d/dx[ln(x)] = 1/x"))
        elif e == x:
            pasos.append(("regla", "📕 Derivada de x", "d/dx[x] = 1"))
        elif e.is_number:
            pasos.append(("regla", "📕 Constante", f"d/dx[{e}] = 0"))
    analizar(expr)
    return pasos

# ── Resultado ─────────────────────────────────────────────────────────────────
if calcular and funcion_str:
    try:
        fs = funcion_str.replace("ln(", "log(")
        f_expr = sympify(fs, locals={"x": x, "e": E, "pi": pi})
        f_prima = diff(f_expr, x)
        f_simp  = simplify(f_prima)

        st.markdown("---")
        st.markdown("## 📥 Función ingresada")
        st.latex(f"f(x) = {latex(f_expr)}")

        st.markdown("---")
        st.markdown("## 🪜 Procedimiento paso a paso")
        pasos = generar_pasos(f_expr)
        n = 1
        for tipo, contenido, formula in pasos:
            if tipo == "regla":
                st.markdown(f"**Paso {n}: {contenido}**")
                if formula: st.markdown(f"> 📐 *{formula}*")
                n += 1
            else:
                st.markdown(contenido)

        st.markdown("---")
        st.markdown("## 🔢 Derivación formal")
        st.latex(f"f'(x) = \\frac{{d}}{{dx}}\\left[{latex(f_expr)}\\right] = {latex(f_prima)}")

        st.markdown("---")
        st.success("### ✅ Resultado Final")
        st.latex(f"f'(x) = {latex(f_simp)}")

        f_exp = expand(f_prima)
        if f_exp != f_simp:
            st.markdown("**Forma expandida:**")
            st.latex(f"f'(x) = {latex(f_exp)}")

        st.markdown("---")
        st.markdown("Reglas utilizadas")
        tabla = {
            "suma_resta":       ("Suma/Resta",          "d/dx[u±v] = u'±v'"),
            "producto":         ("Producto",             "d/dx[u·v] = u'v+uv'"),
            "cociente":         ("Cociente",             "d/dx[u/v] = (u'v−uv')/v²"),
            "potencia":         ("Potencia",             "d/dx[xⁿ] = n·xⁿ⁻¹"),
            "cadena_potencia":  ("Cadena",               "d/dx[g(x)ⁿ] = n·gⁿ⁻¹·g'"),
            "trigonometrica":   ("Trigonométricas",      "sin'=cos, cos'=−sin, tan'=sec²"),
            "exponencial_e":    ("Exponencial eˣ",       "d/dx[eˣ]=eˣ  |  d/dx[e^g]=e^g·g'"),
            "exponencial_base": ("Exponencial base a",   "d/dx[aˣ]=aˣ·ln(a)"),
            "logaritmo":        ("Logaritmo natural",    "d/dx[ln(x)]=1/x  |  d/dx[ln(g)]=g'/g"),
            "raiz":             ("Raíz cuadrada",        "d/dx[√x]=1/(2√x)"),
        }
        for clave in clasificar_expr(f_expr):
            if clave in tabla:
                nombre, f2 = tabla[clave]
                st.markdown(f"- **{nombre}**: `{f2}`")

    except Exception as err:
        st.error(f"Error: `{err}`")
        st.markdown("**Sintaxis correcta:**")
        st.code("3*x**2 + sin(x)\nexp(x**2)\nln(x**3 + 1)\nx**2 * cos(x)\nsin(x) / x**2")
elif calcular and not funcion_str:
    st.warning("Escribe una función primero.")
