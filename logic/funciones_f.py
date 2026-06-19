import numpy as np
import matplotlib.pyplot as plt
import re
def normalizar(expr):
    expr = expr.strip().replace(" ", "")
    for prefix in ("f(x)=", "y=", "f(x)", "y"):
        if expr.startswith(prefix):
            expr = expr[len(prefix):]
            break
    reemplazos = [
        ("x³",  "x**3"),
        ("x²",  "x**2"),
        ("xⁿ",  "x**n"),
        ("^",   "**"),
        ("√",   "np.sqrt"),
        ("∛",   "np.cbrt"),
        ("π",   "np.pi"),
        ("∞",   "np.inf"),
        ("eˣ",  "np.exp(x)"),
        ("sin", "np.sin"),
        ("cos", "np.cos"),
        ("tan", "np.tan"),
        ("log", "np.log10"),
        ("ln",  "np.log"),
        ("÷",   "/"),
    ]
    for orig, nuevo in reemplazos:
        expr = expr.replace(orig, nuevo)
    expr = re.sub(r'(\d)(x)',    r'\1*\2', expr)
    expr = re.sub(r'(\d)(np\.)', r'\1*\2', expr)
    expr = re.sub(r'(\d)(\()',   r'\1*\2', expr)
    return expr
def detectar_tipo(expr_py):
    e = expr_py.lower()
    if re.fullmatch(r'[+-]?\d*\.?\d*', e):
        return "Función constante"
    if re.fullmatch(r'[+-]?\d*\.?\d*\*?x([+-]\d*\.?\d*)?', e):
        return "Función lineal (mx + b)" if ("+" in e[1:] or "-" in e[1:]) else "Función lineal (mx)"
    if "x**2" in e:
        return "Función cuadrática"
    if "x**3" in e:
        return "Función cúbica"
    if "np.sqrt" in e:
        return "Función irracional (raíz cuadrada)"
    if "np.cbrt" in e:
        return "Función irracional (raíz cúbica)"
    if re.search(r'1/x\*\*2', e):
        return "Función racional (1/x²)"
    if "1/x" in e:
        return "Función racional (1/x)"
    if "np.sin" in e:
        return "Función trigonométrica — seno"
    if "np.cos" in e:
        return "Función trigonométrica — coseno"
    if "np.tan" in e:
        return "Función trigonométrica — tangente"
    if "np.log10" in e:
        return "Función logarítmica (base 10)"
    if "np.log" in e:
        return "Función logarítmica natural"
    if "np.exp" in e:
        return "Función exponencial"
    return "Función personalizada"
def evaluar_funcion(expr_py, x):
    namespace = {"x": x, "np": np}
    with np.errstate(divide='ignore', invalid='ignore'):
        y = eval(expr_py, {"__builtins__": {}}, namespace)
    return np.where(np.isfinite(y), y, np.nan)
def rango_y(expr_py):
    if "1/x" in expr_py:
        return -10.0, 10.0
    if "np.tan" in expr_py:
        return -8.0, 8.0
    if "np.sqrt" in expr_py or "np.cbrt" in expr_py:
        return -2.0, 10.0
    return -15.0, 15.0
def calcular_funcion(expresion_raw):
    expr_py = normalizar(expresion_raw)
    evaluar_funcion(expr_py, np.array([1.0, 2.0]))
    tipo = detectar_tipo(expr_py)
    return expr_py, tipo
def graficar_funcion(expr_py, texto_original, x_min=-15, x_max=15):
    x = np.linspace(x_min, x_max, 800)
    y = evaluar_funcion(expr_py, x)
    y_min, y_max = rango_y(expr_py)
    fig, ax = plt.subplots(figsize=(9, 9.8))
    ax.plot(x, y, color="#5c1b1b", linewidth=2.5, label=texto_original)
    ax.axhline(0, color='black', linewidth=1.2)
    ax.axvline(0, color='black', linewidth=1.2)
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.grid(True, which='both', color='lightgray', linestyle='-', linewidth=0.5)
    ax.legend(fontsize=12, loc="upper left")
    ax.annotate("", xy=(x_max, 0), xytext=(x_max - 0.8, 0),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
    ax.annotate("", xy=(0, y_max), xytext=(0, y_max - 0.8),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
    ax.text(x_max - 0.5, -1.2, "x", fontsize=13, color="black")
    ax.text(0.4, y_max - 1.2,  "y", fontsize=13, color="black")
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    return fig
def tabla_valores(expr_py, x_min=-15, x_max=15, n=11):
    import pandas as pd
    x_vals = np.linspace(x_min, x_max, n)
    y_vals = evaluar_funcion(expr_py, x_vals)
    df = pd.DataFrame({
        "x":    np.round(x_vals, 2),
        "f(x)": np.round(y_vals, 4)
    })
    return df
def generar():
    pass

#