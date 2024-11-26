1
import sympy as spx = sp.symbols('x')
equation = sp.Eq(2*x + 3, 9)
solution = sp.solve(equation, x)
print(solution)

2
from sympy import Symbolimport sympy as sp
x = Symbol('x')
expr = 3 * x ** 2 + 2 * x + 1
solution = sp.diff(expr, x)print(solution)

3
from sympy import symbols, diff, simplify
import matplotlib.pyplot as plt
import numpy as np

# Шаг 1. Определение переменных и функции
x = symbols('x')
expr = x**2 - 4 * x + 3  # Заданная функция

# Шаг 2. Нахождение производной
derivative = diff(expr, x)
print(f"Производная: {derivative}")

# Шаг 3. Упрощение выражения
simplified_expr = simplify(expr)
print(f"Упрощённая функция: {simplified_expr}")

# Шаг 4. Построение графиков функции и её производной
x_vals = np.linspace(0, 4, 100)
y_vals = [expr.subs(x, val) for val in x_vals]
dy_vals = [derivative.subs(x, val) for val in x_vals]

plt.plot(x_vals, y_vals, label='f(x)')
plt.plot(x_vals, dy_vals, label="f'(x)")
plt.axhline(0, color='black', linewidth=0.5)
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции и её производной')
plt.grid(True)
plt.show()
