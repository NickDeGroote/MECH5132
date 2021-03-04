import math

import numpy as np
import sympy as sp
from sympy import symbols
from sympy.strategies.rl import subs

t1, t2, t3, t4, t5, t6 = symbols("t1 t2 t3 t4 t5 t6")
d1, d6 = symbols("d1 d6")
ox, oy, oz = symbols("ox oy oz")
a2, a3 = symbols("a2 a3")

ninety = symbols("ninety")

print(f"{sp.cos(t1)}")

cs = sp.cos(t1)

print(f"{cs.subs(t1, np.pi)}")


def dh(a, alph, d, th):
    dh01 = np.array(
        [
            [
                sp.cos(th),
                -sp.sin(th) * sp.cos(alph),
                sp.sin(th) * sp.sin(alph),
                a * sp.cos(th),
            ],
            [
                sp.sin(th),
                sp.cos(th) * sp.cos(alph),
                -sp.cos(th) * sp.sin(alph),
                a * sp.sin(th),
            ],
            [0, sp.sin(alph), sp.cos(alph), d],
            [0, 0, 0, 1],
        ]
    )

    return dh01


dh1 = dh(0, ninety, d1, t1)
dh2 = dh(a2, 0, 0, t2)
dh3 = dh(a3, 0, 0, t3)
dh4 = dh(0, ninety, 0, t4)
dh5 = dh(0, 0, 0, t5)
dh6 = dh(0, 0, d6, t6)
"""
DH65 = np.dot(dh6, dh5)
DH64 = np.dot(DH65, dh4)
DH63 = np.dot(DH64, dh3)
DH62 = np.dot(DH63, dh2)
DH61 = np.dot(DH62, dh1)
"""

DH12 = np.dot(dh1, dh2)
DH13 = np.dot(DH12, dh3)


# DH34 = np.dot(dh3, dh4)
DH35 = np.dot(dh4, dh5)
DH36 = np.dot(DH35, dh6)


np.set_printoptions(precision=2, suppress=True, linewidth=120)
print(f"{DH36}")
