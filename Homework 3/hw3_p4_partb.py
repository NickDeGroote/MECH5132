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
a = 50
V = 14.645
q0 = 10
qf = 35
v0 = 0
vf = 0
t0 = 0
tf = 2
tb1 = V / a

[M1, b1] = cubic_polynomial_trajectory(q0, v0, qf, vf, t0, tf)  # Assume theta0 is zero
a1 = M1.inv() * b1

q1_piece1 = q0 + (a/2) * t ** 2
q1_piece2 = (qf + q0 - V * tf) / 2 + V * t
q1_piece3 = qf - (a * tf ** 2 / 2) + a * tf * t - (a / 2) * t ** 2


print("theta(t) 1:")
print(pretty(q1_piece1))
print(pretty(q1_piece2))
print(pretty(q1_piece3))
print("Latex Representation:")
print(latex(simplify(q1_piece1)))
print(latex(simplify(q1_piece2)))
print(latex(simplify(q1_piece3)))

v1_piece1 = diff(q1_piece1, t)
v1_piece2 = diff(q1_piece2, t)
v1_piece3 = diff(q1_piece3, t)
print("\nthetadot(t) 1:")
print(pretty(v1_piece1))
print(pretty(v1_piece2))
print(pretty(v1_piece3))
print("Latex Representation:")
print(latex(simplify(v1_piece1)))
print(latex(simplify(v1_piece2)))
print(latex(simplify(v1_piece3)))

alpha1_piece1 = diff(v1_piece1, t)
alpha1_piece2 = diff(v1_piece2, t)
alpha1_piece3 = diff(v1_piece3, t)
print("\nthetadoubledot(t) 1:")
print(pretty(alpha1_piece1))
print(pretty(alpha1_piece2))
print(pretty(alpha1_piece3))
print("Latex Representation:")
print(latex(simplify(alpha1_piece1)))
print(latex(simplify(alpha1_piece2)))
print(latex(simplify(alpha1_piece3)))

a = 50
V = -3.4109
q0 = 35
qf = 25
v0 = 0
vf = 0
t0 = 0
tf = 3
tb2 = -V / a

q2_piece1 = q0 - (a/2) * (t-2) ** 2
q2_piece2 = (qf + q0 - V * tf) / 2 + V * (t - 2)
q2_piece3 = qf - (-a * tf ** 2 / 2) + -a * tf * (t-2) - (-a / 2) * (t-2) ** 2


print("theta(t) 2:")
print(pretty(q2_piece1))
print(pretty(q2_piece2))
print(pretty(q2_piece3))
print("Latex Representation:")
print(latex(simplify(q2_piece1)))
print(latex(simplify(q2_piece2)))
print(latex(simplify(q2_piece3)))

v2_piece1 = diff(q2_piece1, t)
v2_piece2 = diff(q2_piece2, t)
v2_piece3 = diff(q2_piece3, t)
print("\nthetadot(t) 1:")
print(pretty(v2_piece1))
print(pretty(v2_piece2))
print(pretty(v2_piece3))
print("Latex Representation:")
print(latex(simplify(v2_piece1)))
print(latex(simplify(v2_piece2)))
print(latex(simplify(v2_piece3)))

alpha2_piece1 = diff(v2_piece1, t)
alpha2_piece2 = diff(v2_piece2, t)
alpha2_piece3 = diff(v2_piece3, t)
print("\nthetadoubledot(t) 1:")
print(pretty(alpha1_piece1))
print(pretty(alpha1_piece2))
print(pretty(alpha1_piece3))
print("Latex Representation:")
print(latex(simplify(alpha1_piece1)))
print(latex(simplify(alpha1_piece2)))
print(latex(simplify(alpha1_piece3)))

zero_tb1 = np.linspace(0, tb1, 50)
tb1_tf1_tb1 = np.linspace(tb1, 2 - tb1, 50)
tb1_tf1_tf1 = np.linspace(2 - tb1, 2, 50)

two_tb2 = np.linspace(2, 2 + tb2, 50)
tb2_tf2_tb2 = np.linspace(2 + tb2, 5 - tb2, 50)
tb2_tf2_tf2 = np.linspace(5 - tb2, 5, 50)

q1_piece1_lambda = lambdify(t, q1_piece1, "numpy")
q1_piece1_eval = q1_piece1_lambda(zero_tb1)
q1_piece2_lambda = lambdify(t, q1_piece2, "numpy")
q1_piece2_eval = q1_piece2_lambda(tb1_tf1_tb1)
q1_piece3_lambda = lambdify(t, q1_piece3, "numpy")
q1_piece3_eval = q1_piece3_lambda(tb1_tf1_tf1)

q2_piece1_lambda = lambdify(t, q2_piece1, "numpy")
q2_piece1_eval = q2_piece1_lambda(two_tb2)
q2_piece2_lambda = lambdify(t, q2_piece2, "numpy")
q2_piece2_eval = q2_piece2_lambda(tb2_tf2_tb2)
q2_piece3_lambda = lambdify(t, q2_piece3, "numpy")
q2_piece3_eval = q2_piece3_lambda(tb2_tf2_tf2)

v1_piece1_lambda = lambdify(t, v1_piece1, "numpy")
v1_piece1_eval = v1_piece1_lambda(zero_tb1)
v1_piece2_lambda = lambdify(t, v1_piece2, "numpy")
v1_piece2_eval = np.asarray([v1_piece2_lambda(tb1_tf1_tb1)] * 50)
v1_piece3_lambda = lambdify(t, v1_piece3, "numpy")
v1_piece3_eval = v1_piece3_lambda(tb1_tf1_tf1)

v2_piece1_lambda = lambdify(t, v2_piece1, "numpy")
v2_piece1_eval = v2_piece1_lambda(two_tb2)
v2_piece2_lambda = lambdify(t, v2_piece2, "numpy")
v2_piece2_eval = np.asarray([v2_piece2_lambda(tb2_tf2_tb2)] * 50)
v2_piece3_lambda = lambdify(t, v2_piece3, "numpy")
v2_piece3_eval = v2_piece3_lambda(tb2_tf2_tf2)

alpha1_piece1_lambda = lambdify(t, alpha1_piece1, "numpy")
alpha1_piece1_eval = np.asarray([alpha1_piece1_lambda(zero_tb1)] * 50)
alpha1_piece1_eval[-1] = 0
alpha1_piece2_lambda = lambdify(t, alpha1_piece2, "numpy")
alpha1_piece2_eval = np.asarray([alpha1_piece2_lambda(tb1_tf1_tb1)] * 50)
alpha1_piece2_eval[-1] = -50
alpha1_piece3_lambda = lambdify(t, alpha1_piece3, "numpy")
alpha1_piece3_eval = np.asarray([alpha1_piece3_lambda(tb1_tf1_tf1)] * 50)

alpha2_piece1_lambda = lambdify(t, alpha2_piece1, "numpy")
alpha2_piece1_eval = np.asarray([alpha2_piece1_lambda(two_tb2)] * 50)
alpha2_piece1_eval[-1] = 0
alpha2_piece2_lambda = lambdify(t, alpha2_piece2, "numpy")
alpha2_piece2_eval = np.asarray([alpha2_piece2_lambda(tb2_tf2_tb2)] * 50)
#alpha2_piece2_eval[-1] = 50
alpha2_piece3_lambda = lambdify(t, alpha2_piece3, "numpy")
alpha2_piece3_eval = np.asarray([alpha2_piece3_lambda(tb2_tf2_tf2)] * 50)
alpha2_piece3_eval[0] = 0
"""
v1_lambda = lambdify(t, v1, "numpy")
v1_eval = v1_lambda(xrange1)
v2_lambda = lambdify(t, v2, "numpy")
v2_eval = v2_lambda(xrange2)

alpha1_lambda = lambdify(t, alpha1, "numpy")
alpha1_eval = alpha1_lambda(xrange1)
alpha2_lambda = lambdify(t, alpha2, "numpy")
alpha2_eval = alpha2_lambda(xrange2)
"""
plt.plot(zero_tb1, q1_piece1_eval, "b")
plt.plot(tb1_tf1_tb1, q1_piece2_eval, "b")
plt.plot(tb1_tf1_tf1, q1_piece3_eval, "b")
plt.plot(two_tb2, q2_piece1_eval, "b")
plt.plot(tb2_tf2_tb2, q2_piece2_eval, "b")
plt.plot(tb2_tf2_tf2, q2_piece3_eval, "b")
plt.xlabel("Time (sec)")
plt.ylabel(r"${\Theta}$ (degrees)")
plt.title("Position vs. Time, Linear Segments with Parabolic Blends")

plt.figure()
plt.plot(zero_tb1, v1_piece1_eval, "b")
plt.plot(tb1_tf1_tb1, v1_piece2_eval, "b")
plt.plot(tb1_tf1_tf1, v1_piece3_eval, "b")
plt.plot(two_tb2, v2_piece1_eval, "b")
plt.plot(tb2_tf2_tb2, v2_piece2_eval, "b")
plt.plot(tb2_tf2_tf2, v2_piece3_eval, "b")
plt.ylabel(r"$\dot{\Theta}$ (degrees / sec)")
plt.title("Velocity vs. Time, Linear Segments with Parabolic Blends")

plt.figure()
plt.plot(zero_tb1, alpha1_piece1_eval, "b")
plt.plot(tb1_tf1_tb1, alpha1_piece2_eval, "b")
plt.plot(tb1_tf1_tf1, alpha1_piece3_eval, "b")
plt.plot(two_tb2, alpha2_piece1_eval, "b")
plt.plot(tb2_tf2_tb2, alpha2_piece2_eval, "b")
plt.plot(tb2_tf2_tf2, alpha2_piece3_eval, "b")
plt.ylabel(r"$\dot{\Theta}$ (degrees / sec)")
plt.title("Velocity vs. Time, Linear Segments with Parabolic Blends")
plt.ylabel(r"$\ddot{\Theta}$ (degrees / $sec^{2}$)")
plt.title("Acceleration vs. Time, Linear Segments with Parabolic Blends")

plt.show()
