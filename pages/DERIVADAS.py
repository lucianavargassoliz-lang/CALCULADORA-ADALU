import streamlit as st
import sympy as sp
from styles import apply_styles
import numpy as np
import matplotlib.pyplot as plt
apply_styles()
st.set_page_config(page_title="Calculadora de Derivadas", page_icon="∂", layout="centered")
st.image("imagen1.jpeg", width=400)

x = sp.symbols('x')

st.title("Calculadora de Derivadas")
st.markdown("Escribe la función usando la sintaxis de Python aqui unos ejemplos para que lo puedas realizar")
st.caption("`x**2` = x²  ·  `x**3` = x³  ·  `sin(x)` `cos(x)` `tan(x)`  ·  `exp(x)` = eˣ  ·  `ln(x)` = ln  ·  `sqrt(x)` = √x  ·  `*` para multiplicar")

if "funcion_input" not in st.session_state:
    st.session_state["funcion_input"] = ""
if "funcion_valor" not in st.session_state:
    st.session_state.funcion_valor = ""

MAPEO_SIMBOLOS = {
    "x²":"**2", "x³":"**3", "xⁿ":"**", "eˣ":"exp(x)",
    "√":"sqrt(", "∛":"**(1/3)", "÷":"/", "±":"+-",
    "log":"log(", "ln":"ln(", "sin":"sin(", "cos":"cos(", "tan":"tan(",
    "lim":"limit(", "∑":"Sum(", "∫":"integrate(",
    "∞":"oo", "π":"pi", "θ":"theta", "≤":"<=", "≥":">=",
}

def insertar_simbolo(s):
    t = MAPEO_SIMBOLOS.get(s, s).replace("−","-").replace("–","-").replace("—","-")
    st.session_state["funcion_input"] += t

def borrar_todo():
    st.session_state["funcion_input"] = ""

def cargar_ejemplo(e):
    st.session_state["funcion_input"] = e

col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.text_input("f(x) =", key="funcion_input", placeholder="Ej: 3*x**2 + sin(x)")

    numeros = ["1","2","3","4","5","6","7","8","9","0","."]
    letras  = ["x","y","z","w","v","i"]
    signos  = ["+","-","*","/","=","%","[]","<",">","(",")", "÷","±",
               "x²","x³","xⁿ","log","√","∛","≤","≥",
               "∫","lim","∑","∞","π","θ","eˣ","sin","cos","tan","∠","∥"]

    t1, t2, t3 = st.tabs(["1,2,3", "x,y,z", "+,-,*"])
    with t1:
        c = st.columns(4)
        for i,n in enumerate(numeros): c[i%4].button(n, key=f"n{i}", on_click=insertar_simbolo, args=(n,))
    with t2:
        c = st.columns(2)
        for i,l in enumerate(letras): c[i%2].button(l, key=f"l{i}", on_click=insertar_simbolo, args=(l,))
    with t3:
        c = st.columns(5)
        for i,s in enumerate(signos): c[i%5].button(s, key=f"s{i}", on_click=insertar_simbolo, args=(s,))

    st.write("")
    cb, cc = st.columns([1,2])
    with cb: st.button("BORRAR", on_click=borrar_todo)
    with cc: calcular = st.button("CALCULAR DERIVADA", type="primary")

with col_der:
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
    ce = st.columns(2)
    for i,(nombre,expr) in enumerate(ejemplos.items()):
        with ce[i%2]: st.button(nombre, key=f"ej{i}", on_click=cargar_ejemplo, args=(expr,))

funcion_str = st.session_state.get("funcion_input", "")


def detectar_reglas(expr):
    r = []
    if isinstance(expr, sp.Add): r.append("suma_resta")
    if isinstance(expr, sp.Mul):
        sn = [a for a in expr.args if not a.is_number]
        if len(sn) > 1:
            r.append("cociente" if any(isinstance(a, sp.Pow) and a.args[1].is_negative for a in expr.args) else "producto")
    if isinstance(expr, sp.Pow):
        b, e = expr.args
        if b == x and e.is_number: r.append("potencia")
        elif e.is_number: r.append("cadena_potencia")
        elif b.is_number: r.append("exponencial_base")
    if expr.has(sp.sin) or expr.has(sp.cos) or expr.has(sp.tan): r.append("trigonometrica")
    if expr.has(sp.exp):  r.append("exponencial_e")
    if expr.has(sp.log):  r.append("logaritmo")
    if expr.has(sp.sqrt): r.append("raiz")
    return list(dict.fromkeys(r))


def obtener_pasos(expr):
    pasos = []

    def procesar(e, nivel=0):
        if isinstance(e, sp.Add):
            pasos.append(("regla", "Regla de la Suma/Resta", "Si f(x) = u ± v  →  f'(x) = u' ± v'"))
            pasos.append(("info", f"Se identifican **{len(e.args)} términos** que se derivan por separado:", None))
            for i, t in enumerate(e.args, 1):
                pasos.append(("latex_termino", f"\\text{{Término {i}:}}\\quad {sp.latex(t)} \\quad\\rightarrow\\quad {sp.latex(sp.diff(t, x))}", None))
                procesar(t, nivel+1)

        elif isinstance(e, sp.Mul):
            sn = [a for a in e.args if not a.is_number]
            hay_div = any(isinstance(a, sp.Pow) and a.args[1].is_negative for a in e.args)
            if hay_div and len(sn) >= 2:
                na = [a for a in e.args if not (isinstance(a, sp.Pow) and a.args[1].is_negative and not a.args[0].is_number)]
                da = [sp.Pow(a.args[0], -a.args[1]) for a in e.args if isinstance(a, sp.Pow) and a.args[1].is_negative and not a.args[0].is_number]
                u = sp.Mul(*na) if na else sp.S.One
                v = sp.Mul(*da) if da else sp.S.One
                du, dv = sp.diff(u, x), sp.diff(v, x)
                pasos.append(("regla", "Regla del Cociente", "Si f = u/v  →  f' = (u'v − uv') / v²"))
                pasos.append(("latex_info", f"u = {sp.latex(u)} \\quad\\Rightarrow\\quad u' = {sp.latex(du)}", None))
                pasos.append(("latex_info", f"v = {sp.latex(v)} \\quad\\Rightarrow\\quad v' = {sp.latex(dv)}", None))
            elif len(sn) > 1:
                u, v = sn[0], sp.Mul(*sn[1:])
                du, dv = sp.diff(u, x), sp.diff(v, x)
                pasos.append(("regla", "Regla del Producto", "Si f = u·v  →  f' = u'v + uv'"))
                pasos.append(("latex_info", f"u = {sp.latex(u)} \\quad\\Rightarrow\\quad u' = {sp.latex(du)}", None))
                pasos.append(("latex_info", f"v = {sp.latex(v)} \\quad\\Rightarrow\\quad v' = {sp.latex(dv)}", None))
                procesar(u, nivel+1); procesar(v, nivel+1)
            else:
                procesar(sn[0], nivel+1)

        elif isinstance(e, sp.Pow):
            b, exp = e.args
            if b == x and exp.is_number:
                pasos.append(("regla", "Regla de la Potencia", "Si f = xⁿ  →  f' = n·xⁿ⁻¹"))
                pasos.append(("latex_info", f"x^{{{exp}}} \\quad\\rightarrow\\quad {sp.latex(sp.diff(e, x))}", None))
            elif not b.has(x) and exp.has(x):
                pasos.append(("regla", "Exponencial base constante", "Si f = aˣ  →  f' = aˣ·ln(a)"))
            elif exp.is_number and b.has(x) and b != x:
                dg = sp.diff(b, x)
                pasos.append(("regla", "Regla de la Cadena + Potencia", "Si f = [g(x)]ⁿ  →  f' = n·[g]ⁿ⁻¹·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(b)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
                procesar(b, nivel+1)

        elif isinstance(e, sp.sin):
            arg = e.args[0]
            if arg != x:
                pasos.append(("regla", "Regla de la Cadena + sin", "Si f = sin(g)  →  f' = cos(g)·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(sp.diff(arg,x))}", None))
            else:
                pasos.append(("regla", "Derivada de sin(x)", "d/dx[sin(x)] = cos(x)"))

        elif isinstance(e, sp.cos):
            arg = e.args[0]
            if arg != x:
                pasos.append(("regla", "Regla de la Cadena + cos", "Si f = cos(g)  →  f' = −sin(g)·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(sp.diff(arg,x))}", None))
            else:
                pasos.append(("regla", "Derivada de cos(x)", "d/dx[cos(x)] = −sin(x)"))

        elif isinstance(e, sp.tan):
            arg = e.args[0]
            if arg != x:
                pasos.append(("regla", "Regla de la Cadena + tan", "Si f = tan(g)  →  f' = sec²(g)·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(sp.diff(arg,x))}", None))
            else:
                pasos.append(("regla", "Derivada de tan(x)", "d/dx[tan(x)] = sec²(x)"))

        elif isinstance(e, sp.exp):
            arg = e.args[0]
            if arg != x:
                pasos.append(("regla", "Regla de la Cadena + eˣ", "Si f = e^g  →  f' = e^g·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(sp.diff(arg,x))}", None))
                procesar(arg, nivel+1)
            else:
                pasos.append(("regla", "Derivada de eˣ", "d/dx[eˣ] = eˣ"))

        elif isinstance(e, sp.log):
            arg = e.args[0]
            if arg != x:
                pasos.append(("regla", "Regla de la Cadena + ln", "Si f = ln(g)  →  f' = g'/g"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(sp.diff(arg,x))}", None))
                procesar(arg, nivel+1)
            else:
                pasos.append(("regla", "Derivada de ln(x)", "d/dx[ln(x)] = 1/x"))

        elif e == x:
            pasos.append(("regla", "Derivada de x", "d/dx[x] = 1"))
        elif e.is_number:
            pasos.append(("regla", "Constante", f"d/dx[{e}] = 0"))

    procesar(expr)
    return pasos
##grafica
def graficar_funcion_y_derivada(funcion, derivada, variable):
    try:
        fn_original = sp.lambdify(variable, funcion, "numpy")
        fn_derivada = sp.lambdify(variable, derivada, "numpy")

        valores_x = np.linspace(-10, 10, 400)
        valores_y_orig = fn_original(valores_x)
        valores_y_deriv = fn_derivada(valores_x)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(valores_x, valores_y_orig, label="f(x)")
        ax.plot(valores_x, valores_y_deriv, label="f'(x)", linestyle="--")

        ax.axhline(0)
        ax.axvline(0)

        ax.set_title("f(x) y su derivada")
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
    file_name="grafica_derivada.pdf",
    mime="application/pdf"
)
        ##
    except:
        st.warning("No se pudo graficar.")
        ##fin 

if calcular and funcion_str:
    try:
        entrada = funcion_str.replace("ln(","log(").replace("−","-").replace("–","-").replace("—","-")
        f_expr  = sp.sympify(entrada, locals={"x":x, "e":sp.E, "pi":sp.pi})
        f_prima = sp.diff(f_expr, x)
        f_simp  = sp.simplify(f_prima)

        st.markdown("---")
        st.markdown("Función ingresada")
        st.latex(f"f(x) = {sp.latex(f_expr)}")

        st.markdown("---")
        st.markdown("Procedimiento paso a paso")
        n = 1
        for tipo, contenido, formula in obtener_pasos(f_expr):
            if tipo == "regla":
                st.markdown(f"**Paso {n}: {contenido}**")
                if formula: st.markdown(f"> *{formula}*")
                n += 1
            elif tipo in ("latex_info","latex_termino"):
                st.latex(contenido)
            else:
                st.markdown(contenido)

        st.markdown("---")
        st.markdown("Derivación formal")
        st.latex(f"f'(x) = \\frac{{d}}{{dx}}\\left[{sp.latex(f_expr)}\\right] = {sp.latex(f_prima)}")

        st.markdown("---")
        st.success("RESULTADO FINAL")
        st.latex(f"f'(x) = {sp.latex(f_simp)}")
        st.markdown("---")
        st.markdown("GRAFICA DE LA FUNCION Y SU DERIVADA")
        graficar_funcion_y_derivada(f_expr, f_prima, x)

        fe = sp.expand(f_prima)
        if fe != f_simp:
            st.markdown("**Forma expandida:**")
            st.latex(f"f'(x) = {sp.latex(fe)}")

        st.markdown("---")
        st.markdown("Reglas utilizadas")
        tabla_reglas = {
            "suma_resta":      ("Suma/Resta",        r"\frac{d}{dx}[u \pm v] = u' \pm v'"),
            "producto":        ("Producto",           r"\frac{d}{dx}[u \cdot v] = u'v + uv'"),
            "cociente":        ("Cociente",           r"\frac{d}{dx}\left[\frac{u}{v}\right] = \frac{u'v - uv'}{v^2}"),
            "potencia":        ("Potencia",           r"\frac{d}{dx}[x^n] = n \cdot x^{n-1}"),
            "cadena_potencia": ("Cadena",             r"\frac{d}{dx}[g(x)^n] = n \cdot g^{n-1} \cdot g'"),
            "trigonometrica":  ("Trigonométricas",    r"\sin' = \cos,\quad \cos' = -\sin,\quad \tan' = \sec^2"),
            "exponencial_e":   ("Exponencial e",      r"\frac{d}{dx}[e^x] = e^x \quad|\quad \frac{d}{dx}[e^{g}] = e^{g} \cdot g'"),
            "exponencial_base":("Exponencial base a", r"\frac{d}{dx}[a^x] = a^x \cdot \ln(a)"),
            "logaritmo":       ("Logaritmo natural",  r"\frac{d}{dx}[\ln x] = \frac{1}{x} \quad|\quad \frac{d}{dx}[\ln g] = \frac{g'}{g}"),
            "raiz":            ("Raíz cuadrada",      r"\frac{d}{dx}[\sqrt{x}] = \frac{1}{2\sqrt{x}}"),
        }
        for clave in detectar_reglas(f_expr):
            if clave in tabla_reglas:
                nombre, formula = tabla_reglas[clave]
                st.markdown(f"**{nombre}**")
                st.latex(formula)

    except Exception as err:
        st.error(f"Error: `{err}`")
        st.markdown("**Sintaxis correcta:**")
        st.code("3*x**2 + sin(x)\nexp(x**2)\nln(x**3 + 1)\nx**2 * cos(x)\nsin(x) / x**2")

elif calcular and not funcion_str:
    st.warning("Escribe una función primero.")



