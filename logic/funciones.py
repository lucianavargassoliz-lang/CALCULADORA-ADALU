import sympy as sp
def generar_funciones_derivada(expresion):
    x = sp.symbols('x')
    funcion = sp.sympify(expresion)
    derivada = sp.diff(funcion, x)
    f = sp.lambdify(x, funcion, 'numpy')
    df = sp.lambdify(x, derivada, 'numpy')
    return f, df, derivada

