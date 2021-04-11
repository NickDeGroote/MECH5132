from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from sympy.plotting import plot
from typing import Tuple, List


def cubic_polynomial_trajectory(
    q0: symbols, v0: symbols, qf: symbols, vf: symbols, t0: symbols, tf: symbols
) -> List[symbols]:
    M = Matrix(
        [
            [1, t0, t0 ** 2, t0 ** 3],
            [0, 1, 2 * t0, 3 * t0 ** 2],
            [1, tf, tf ** 2, tf ** 3],
            [0, 1, 2 * tf, 3 * tf ** 2],
        ]
    )

    b = Matrix([q0, v0, qf, vf])
    """
    q0 = a0 + a1 * t0 + a2 * t0 ** 2 + a3 * t0 ** 3
    v0 = a1 + 2 * a2 * t0 + 3 * a3 * t0 ** 2
    qf = a0 + a1 * tf + a2 * tf ** 2 + a3 * tf ** 3
    vf = a1 + 2 * a2 * tf + 3 * a3 * tf ** 2
    """
    return [M, b]


t = symbols("t")

q0 = 10
qf = 35
v0 = 0
vf = 0
t0 = 0
tf = 2

[M1, b1] = cubic_polynomial_trajectory(q0, v0, qf, vf, t0, tf)  # Assume theta0 is zero
a1 = M1.inv() * b1
print(latex(a1))

q1 = a1[0] + a1[1] * t + a1[2] * t ** 2 + a1[3] * t ** 3
print("theta(t) 1:")
print(pretty(q1))
print("Latex Representation:")
print(latex(simplify(q1)))

v1 = diff(q1, t)
print("\nthetadot(t) 1:")
print(pretty(v1))
print("Latex Representation:")
print(latex(simplify(v1)))

alpha1 = diff(v1, t)
print("\nthetadoubledot(t) 1:")
print(pretty(alpha1))
print("Latex Representation:")
print(latex(simplify(alpha1)))

q0 = 35
qf = 25
v0 = 0
vf = 0
t0 = 2
tf = 5

[M2, b2] = cubic_polynomial_trajectory(q0, v0, qf, vf, t0, tf)  # Assume theta0 is zero
a2 = M2.inv() * b2
q2 = a2[0] + a2[1] * t + a2[2] * t ** 2 + a2[3] * t ** 3

print("theta(t) 2:")
print(pretty(q2))
print("Latex Representation:")
print(latex(simplify(q2)))

v2 = diff(q2, t)
print("\nthetadot(t) 2:")
print(pretty(v2))
print("Latex Representation:")
print(latex(simplify(v2)))

alpha2 = diff(v2, t)
print("\nthetadoubledot(t) 2:")
print(pretty(alpha2))
print("Latex Representation:")
print(latex(simplify(alpha2)))

xrange1 = np.linspace(0, 2, 100)
xrange2 = np.linspace(2, 5, 100)
q1_lambda = lambdify(t, q1, "numpy")
q1_eval = q1_lambda(xrange1)
q2_lambda = lambdify(t, q2, "numpy")
q2_eval = q2_lambda(xrange2)

v1_lambda = lambdify(t, v1, "numpy")
v1_eval = v1_lambda(xrange1)
v2_lambda = lambdify(t, v2, "numpy")
v2_eval = v2_lambda(xrange2)

alpha1_lambda = lambdify(t, alpha1, "numpy")
alpha1_eval = alpha1_lambda(xrange1)
alpha2_lambda = lambdify(t, alpha2, "numpy")
alpha2_eval = alpha2_lambda(xrange2)

plt.plot(xrange1, q1_eval, "b")
plt.plot(xrange2, q2_eval, "b")
plt.xlabel("Time (sec)")
plt.ylabel(r"${\Theta}$ (degrees)")
plt.title("Position vs. Time, Two Cubic Segments")
plt.show()

plt.figure()
plt.plot(xrange1, v1_eval, "b")
plt.plot(xrange2, v2_eval, "b")
plt.xlabel("Time (sec)")
plt.ylabel(r"$\dot{\Theta}$ (degrees / sec)")
plt.title("Velocity vs. Time, Two Cubic Segments")
plt.show()

plt.figure()
plt.plot(xrange1, alpha1_eval, "b")
plt.plot(xrange2, alpha2_eval, "b")
plt.xlabel("Time (sec)")
plt.ylabel(r"$\ddot{\Theta}$ (degrees / $sec^{2}$)")
plt.title("Acceleration vs. Time, Two Cubic Segments")
plt.show()

