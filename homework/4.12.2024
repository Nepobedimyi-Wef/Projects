6.
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Определяем функцию, описывающую ОДУ
def model(x, y):
    dydx = -2 * y
    return dydx

y0 = [2]
t_span = (0, 2)  # Интервал времени от 0 до 5
t_eval = np.linspace(t_span[0], t_span[1], 100)

solution = solve_ivp(model, t_span, y0, t_eval=t_eval)

x = solution.t
y = solution.y[0]

plt.plot(x, y, label='y(t)')
plt.title('Решение ОДУ: dy/dx = -2y')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()


7.
import numpy as np
from scipy.linalg import inv

A = np.array([[4,7],
              [2,6]])

A_inv = inv(A)
print("Обратная матрица A:", A_inv)




8.


import numpy as np
from scipy.optimize import fsolve
def system(vars):
    x,y = vars
    return [x**2 + y**2 , x + y]

initial_guess = [0.5, 0.5]

solution = fsolve(system, initial_guess)

x, y = solution
print(f"x = {x:.6f}, y = {y:.6f}")


9.


import numpy as np
from scipy.linalg import det

A = np.array([[3, 1],
              [4, 2]])

determinant = det(A)

print("Определитель матрицы A:",determinant)



10.
