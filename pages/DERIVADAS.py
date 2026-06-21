import streamlit as st
import sympy as sp
from styles import apply_styles
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
    "x²":  "**2",
    "x³":  "**3",
    "xⁿ":  "**",
    "eˣ":  "exp(x)",
    "√":   "sqrt(",
    "∛":   "**(1/3)",
    "÷":   "/",
    "±":   "+-",
    "log": "log(",
    "ln":  "ln(",
    "sin": "sin(",
    "cos": "cos(",
    "tan": "tan(",
    "lim": "limit(",
    "∑":   "Sum(",
    "∫":   "integrate(",
    "∞":   "oo",
    "π":   "pi",
    "θ":   "theta",
    "≤":   "<=",
    "≥":   ">=",
}

def insertar_simbolo(simbolo):
    texto_a_insertar = MAPEO_SIMBOLOS.get(simbolo, simbolo)
    texto_a_insertar = texto_a_insertar.replace("−", "-").replace("–", "-").replace("—", "-")
    st.session_state["funcion_input"] += texto_a_insertar

def borrar_ultimo():
    st.session_state["funcion_input"] = st.session_state["funcion_input"][:-1]

def borrar_todo():
    st.session_state["funcion_input"] = ""

def cargar_ejemplo(expresion_ejemplo):
    st.session_state["funcion_input"] = expresion_ejemplo

funcion_str = st.text_input(
    "f(x) =",
    key="funcion_input",
    placeholder="Ej: 3*x**2 + sin(x)",
)
st.markdown("TECLADO INGRESA TU DERIVADA")

numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."]
letras  = ["x", "y", "z", "w", "v", "i"]
signos  = [
    "+", "-", "*", "/", "(", ")", "=", "%",
    "x²", "x³", "xⁿ", "log", "ln", "√", "∛",
    "≤", "≥", "∫", "lim", "∑", "∞", "π", "θ",
    "eˣ", "sin", "cos", "tan", "÷", "±",
]

tab_num, tab_let, tab_sig = st.tabs(["1,2,3", "x,y,z", "+,-,*"])
with tab_num:
    cols_num = st.columns(4)
    for idx, num in enumerate(numeros):
        cols_num[idx % 4].button(num, key=f"num_{num}_{idx}", on_click=insertar_simbolo, args=(num,))
with tab_let:
    cols_let = st.columns(3)
    for idx, let in enumerate(letras):
        cols_let[idx % 3].button(let, key=f"let_{let}_{idx}", on_click=insertar_simbolo, args=(let,))
with tab_sig:
    cols_sig = st.columns(5)
    for idx, sig in enumerate(signos):
        cols_sig[idx % 5].button(sig, key=f"sig_{sig}_{idx}", on_click=insertar_simbolo, args=(sig,))

st.write("")
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.button("⌫ Borrar último", on_click=borrar_ultimo, use_container_width=True)
with col_b2:
    st.button("Borrar todo", on_click=borrar_todo, use_container_width=True)

st.markdown("**Ejemplos:**")
ejemplos = {
    "3x³ − 2x² + 5x": "3*x**3 - 2*x**2 + 5*x",
    "sin²(x) + cos(x)": "sin(x)**2 + cos(x)",
    "e^(x²)":           "exp(x**2)",
    "ln(x³+1)":         "ln(x**3 + 1)",
    "x²·sin(x)":        "x**2 * sin(x)",
    "sin(x)/x²":        "sin(x) / x**2",
    "sin(3x²+1)":       "sin(3*x**2 + 1)",
}

cols_ej = st.columns(4)
for idx, (nombre, expr) in enumerate(ejemplos.items()):
    with cols_ej[idx % 4]:
        st.button(nombre, key=f"ej_{idx}", on_click=cargar_ejemplo, args=(expr,))

calcular = st.button("CALCULAR DERIVADA", type="primary", use_container_width=True)

# PARA NO PERDER LA ESTRUCTURA 
funcion_str = st.session_state.get("funcion_input", "")

def detectar_reglas_usadas(expr):
    """ Analiza la estructura de la expresión de SymPy para ver qué reglas se aplicaron """
    reglas_detectadas = []
    if isinstance(expr, sp.Add): 
        reglas_detectadas.append("suma_resta")
        
    if isinstance(expr, sp.Mul):
        args_no_num = [a for a in expr.args if not a.is_number]
        if len(args_no_num) > 1:
            tiene_exponente_negativo = any(isinstance(a, sp.Pow) and a.args[1].is_negative for a in expr.args)
            reglas_detectadas.append("cociente" if tiene_exponente_negativo else "producto")
            
    if isinstance(expr, sp.Pow):
        base, exponente = expr.args
        if base == x and exponente.is_number:    
            reglas_detectadas.append("potencia")
        elif exponente.is_number:                 
            reglas_detectadas.append("cadena_potencia")
        elif base.is_number:                    
            reglas_detectadas.append("exponencial_base")
            
    if expr.has(sp.sin) or expr.has(sp.cos) or expr.has(sp.tan): 
        reglas_detectadas.append("trigonometrica")
    if expr.has(sp.exp):  reglas_detectadas.append("exponencial_e")
    if expr.has(sp.log):  reglas_detectadas.append("logaritmo")
    if expr.has(sp.sqrt): reglas_detectadas.append("raiz")
    
    return list(dict.fromkeys(reglas_detectadas)) # Evita duplicados de reglas

def obtener_pasos_derivacion(expr):
    """ Recorre la expresión de forma recursiva para armar la explicación paso a paso """
    pasos = []
    def procesar_nodo(e, nivel=0):
        if isinstance(e, sp.Add):
            pasos.append(("regla", "Regla de la Suma/Resta", "Si f(x) = u ± v  →  f'(x) = u' ± v'"))
            pasos.append(("info", f"Se identifican **{len(e.args)} términos** que se derivan por separado:", None))
            for idx, termino in enumerate(e.args, 1):
                pasos.append(("latex_termino", f"\\text{{Término {idx}:}}\\quad {sp.latex(termino)} \\quad\\rightarrow\\quad {sp.latex(sp.diff(termino, x))}", None))
                procesar_nodo(termino, nivel + 1)
                
        elif isinstance(e, sp.Mul):
            args_no_num = [a for a in e.args if not a.is_number]
            tiene_exponente_negativo = any(isinstance(a, sp.Pow) and a.args[1].is_negative for a in e.args)
            
            if tiene_exponente_negativo and len(args_no_num) >= 2:
              
                numerador_args = [a for a in e.args if not (isinstance(a, sp.Pow) and a.args[1].is_negative and not a.args[0].is_number)]
                denominador_args = [sp.Pow(a.args[0], -a.args[1]) for a in e.args if isinstance(a, sp.Pow) and a.args[1].is_negative and not a.args[0].is_number]
                
                u = sp.Mul(*numerador_args) if numerador_args else sp.S.One
                v = sp.Mul(*denominador_args) if denominador_args else sp.S.One
                du, dv = sp.diff(u, x), sp.diff(v, x)
                
                pasos.append(("regla", "Regla del Cociente", "Si f = u/v  →  f' = (u'v − uv') / v²"))
                pasos.append(("latex_info", f"u = {sp.latex(u)} \\quad\\Rightarrow\\quad u' = {sp.latex(du)}", None))
                pasos.append(("latex_info", f"v = {sp.latex(v)} \\quad\\Rightarrow\\quad v' = {sp.latex(dv)}", None))
                
            elif len(args_no_num) > 1:
                
                u, v = args_no_num[0], sp.Mul(*args_no_num[1:])
                du, dv = sp.diff(u, x), sp.diff(v, x)
                
                pasos.append(("regla", "Regla del Producto", "Si f = u·v  →  f' = u'v + uv'"))
                pasos.append(("latex_info", f"u = {sp.latex(u)} \\quad\\Rightarrow\\quad u' = {sp.latex(du)}", None))
                pasos.append(("latex_info", f"v = {sp.latex(v)} \\quad\\Rightarrow\\quad v' = {sp.latex(dv)}", None))
                procesar_nodo(u, nivel + 1)
                procesar_nodo(v, nivel + 1)
            else:
                procesar_nodo(args_no_num[0], nivel + 1)
                
        elif isinstance(e, sp.Pow):
            base, exponente = e.args
            if base == x and exponente.is_number:
                pasos.append(("regla", "Regla de la Potencia", "Si f = xⁿ  →  f' = n·xⁿ⁻¹"))
                pasos.append(("latex_info", f"x^{{{exponente}}} \\quad\\rightarrow\\quad {sp.latex(sp.diff(e, x))}", None))
            elif not base.has(x) and exponente.has(x):
                pasos.append(("regla", "Exponencial base constante", "Si f = aˣ  →  f' = aˣ·ln(a)"))
            elif exponente.is_number and base.has(x) and base != x:
                dg = sp.diff(base, x)
                pasos.append(("regla", "Regla de la Cadena + Potencia", "Si f = [g(x)]ⁿ  →  f' = n·[g]ⁿ⁻¹·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(base)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
                procesar_nodo(base, nivel + 1)
                
        elif isinstance(e, sp.sin):
            arg = e.args[0]
            if arg != x:
                dg = sp.diff(arg, x)
                pasos.append(("regla", "Regla de la Cadena + sin", "Si f = sin(g)  →  f' = cos(g)·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
            else:
                pasos.append(("regla", "Derivada de sin(x)", "d/dx[sin(x)] = cos(x)"))
                
        elif isinstance(e, sp.cos):
            arg = e.args[0]
            if arg != x:
                dg = sp.diff(arg, x)
                pasos.append(("regla", "Regla de la Cadena + cos", "Si f = cos(g)  →  f' = −sin(g)·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
            else:
                pasos.append(("regla", "Derivada de cos(x)", "d/dx[cos(x)] = −sin(x)"))
                
        elif isinstance(e, sp.tan):
            arg = e.args[0]
            if arg != x:
                dg = sp.diff(arg, x)
                pasos.append(("regla", "Regla de la Cadena + tan", "Si f = tan(g)  →  f' = sec²(g)·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
            else:
                pasos.append(("regla", "Derivada de tan(x)", "d/dx[tan(x)] = sec²(x)"))
                
        elif isinstance(e, sp.exp):
            arg = e.args[0]
            if arg != x:
                dg = sp.diff(arg, x)
                pasos.append(("regla", "Regla de la Cadena + eˣ", "Si f = e^g  →  f' = e^g·g'"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
                procesar_nodo(arg, nivel + 1)
            else:
                pasos.append(("regla", "Derivada de eˣ", "d/dx[eˣ] = eˣ"))
                
        elif isinstance(e, sp.log):
            arg = e.args[0]
            if arg != x:
                dg = sp.diff(arg, x)
                pasos.append(("regla", "Regla de la Cadena + ln", "Si f = ln(g)  →  f' = g'/g"))
                pasos.append(("latex_info", f"g(x) = {sp.latex(arg)} \\quad\\Rightarrow\\quad g' = {sp.latex(dg)}", None))
                procesar_nodo(arg, nivel + 1)
            else:
                pasos.append(("regla", "Derivada de ln(x)", "d/dx[ln(x)] = 1/x"))
                
        elif e == x:
            pasos.append(("regla", "Derivada de x", "d/dx[x] = 1"))
        elif e.is_number:
            pasos.append(("regla", "Constante", f"d/dx[{e}] = 0"))
            
    procesar_nodo(expr)
    return pasos

if calcular and funcion_str:
    try:
       
        entrada_limpia = funcion_str.replace("ln(", "log(")
        entrada_limpia = entrada_limpia.replace("−", "-").replace("–", "-").replace("—", "-")
        
        f_expr = sp.sympify(entrada_limpia, locals={"x": x, "e": sp.E, "pi": sp.pi})
        f_prima = sp.diff(f_expr, x)
        f_simp  = sp.simplify(f_prima)

        st.markdown("---")
        st.markdown("Función ingresada")
        st.latex(f"f(x) = {sp.latex(f_expr)}")

        st.markdown("---")
        st.markdown("Procedimiento paso a paso")
        pasos_procedimiento = obtener_pasos_derivacion(f_expr)
        contador_pasos = 1
        
        for tipo, contenido, formula in pasos_procedimiento:
            if tipo == "regla":
                st.markdown(f"**Paso {contador_pasos}: {contenido}**")
                if formula: 
                    st.markdown(f"> *{formula}*")
                contador_pasos += 1
            elif tipo in ("latex_info", "latex_termino"):
                st.latex(contenido)
            else:
                st.markdown(contenido)

        st.markdown("---")
        st.markdown("Derivación formal")
        st.latex(f"f'(x) = \\frac{{d}}{{dx}}\\left[{sp.latex(f_expr)}\\right] = {sp.latex(f_prima)}")

        st.markdown("---")
        st.success("RESULTADO FINAL")
        st.latex(f"f'(x) = {sp.latex(f_simp)}")

        f_exp = sp.expand(f_prima)
        if f_exp != f_simp:
            st.markdown("**Forma expandida:**")
            st.latex(f"f'(x) = {sp.latex(f_exp)}")

        st.markdown("---")
        st.markdown("Reglas utilizadas")
        tabla_reglas = {
            "suma_resta":       ("Suma / Resta",          r"\frac{d}{dx}[u \pm v] = u' \pm v'"),
            "producto":         ("Producto",               r"\frac{d}{dx}[u \cdot v] = u'v + uv'"),
            "cociente":         ("Cociente",               r"\frac{d}{dx}\left[\frac{u}{v}\right] = \frac{u'v - uv'}{v^2}"),
            "potencia":         ("Potencia",               r"\frac{d}{dx}[x^n] = n \cdot x^{n-1}"),
            "cadena_potencia":  ("Regla de la Cadena",     r"\frac{d}{dx}[g(x)^n] = n \cdot g^{n-1} \cdot g'"),
            "trigonometrica":   ("Trigonométricas",        r"\sin' = \cos,\quad \cos' = -\sin,\quad \tan' = \sec^2"),
            "exponencial_e":    ("Exponencial e",          r"\frac{d}{dx}[e^x] = e^x \quad|\quad \frac{d}{dx}[e^{g}] = e^{g} \cdot g'"),
            "exponencial_base": ("Exponencial base a",     r"\frac{d}{dx}[a^x] = a^x \cdot \ln(a)"),
            "logaritmo":        ("Logaritmo natural",      r"\frac{d}{dx}[\ln x] = \frac{1}{x} \quad|\quad \frac{d}{dx}[\ln g] = \frac{g'}{g}"),
            "raiz":             ("Raíz cuadrada",          r"\frac{d}{dx}[\sqrt{x}] = \frac{1}{2\sqrt{x}}"),
        }
        
        for clave in detectar_reglas_usadas(f_expr):
            if clave in tabla_reglas:
                nombre_regla, formula_regla = tabla_reglas[clave]
                st.markdown(f"**{nombre_regla}**")
                st.latex(formula_regla)
##GRAFICA DE DERIVADAS 
        st.markdown("")
        st.markdown("GRAFICA DE f(x) y f'(x)")
        import numpy as np
        import matplotlib.pyplot as plt
        x_min = -5.0
        x_max =  5.0
        mostrar_f      = st.checkbox("Mostrar f(x)",   value=True,  key="check_f")
        mostrar_prima  = st.checkbox("Mostrar f'(x)",  value=True,  key="check_fp")

        if x_min >= x_max:
            st.warning("El valor de x mínimo debe ser menor que x máximo.")
        else:
            f_num      = sp.lambdify(x, f_expr,  modules=["numpy"])
            fprima_num = sp.lambdify(x, f_simp,  modules=["numpy"])
            xs = np.linspace(x_min, x_max, 800)
            try:
                ys_f  = np.array(f_num(xs),      dtype=float)
                ys_fp = np.array(fprima_num(xs), dtype=float)
                ##NOS AYUDA A QUE LA GRAFICA SEA LEGIBLE
                LIMITE = 1e6
                ys_f  = np.where(np.abs(ys_f)  > LIMITE, np.nan, ys_f)
                ys_fp = np.where(np.abs(ys_fp) > LIMITE, np.nan, ys_fp)

                fig, ax = plt.subplots(figsize=(8, 4))

                if mostrar_f:
                    ax.plot(xs, ys_f,  label=f"f(x) = ${sp.latex(f_expr)}$",
                            color="#1fafb4", linewidth=2)
                if mostrar_prima:
                    ax.plot(xs, ys_fp, label=f"f'(x) = ${sp.latex(f_simp)}$",
                            color="#8f0eff", linewidth=2, linestyle="--")

                ax.axhline(0, color="black", linewidth=0.8, linestyle="-")
                ax.axvline(0, color="black", linewidth=0.8, linestyle="-")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.legend(fontsize=9)
                ax.grid(True, alpha=0.3)
                ax.set_xlim(x_min, x_max)

                valores_validos = []
                if mostrar_f:
                    valores_validos.append(ys_f[np.isfinite(ys_f)])
                if mostrar_prima:
                    valores_validos.append(ys_fp[np.isfinite(ys_fp)])
                if valores_validos:
                    todos = np.concatenate(valores_validos)
                    if len(todos) > 0:
                        margen = (todos.max() - todos.min()) * 0.1 or 1
                        ax.set_ylim(todos.min() - margen, todos.max() + margen)

                st.pyplot(fig)
                plt.close(fig)

            except Exception as graf_err:
                st.error(f"No se pudo graficar: `{graf_err}`")
    except Exception as err:
        st.error(f"Error: `{err}`")
        st.markdown("**Sintaxis correcta:**")
        st.code("3*x**2 + sin(x)\nexp(x**2)\nln(x**3 + 1)\nx**2 * cos(x)\nsin(x) / x**2")

elif calcular and not funcion_str:
    st.warning("Escribe una función primero.")