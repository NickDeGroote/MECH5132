from sympy import *
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


a0, a1, a2, a3, q0, qf, v0, vf, t0, tf = symbols(
    "a_0 a_1 a_2 a_3 theta_0 theta_f thetadot_0 thetadot_f t_0 t_f"
)
[M, b] = cubic_polynomial_trajectory(q0, 0, qf, 0, 0, tf)  # Assume theta0 is zero
a = M.inv() * b
print(latex(M))
print("a vector:")
print(pretty(a))
print("\nLatex Representation:")
print(latex(simplify(a)))
