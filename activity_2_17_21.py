from sympy import symbols, Matrix, sin, cos, pi
from math import atan2
import numpy as np


def get_A_matrix(a: symbols, alpha: symbols, d: symbols, theta: symbols) -> Matrix:
    A = Matrix(
        [
            [
                cos(theta),
                -sin(theta) * cos(alpha),
                sin(theta) * sin(alpha),
                a * cos(theta),
            ],
            [
                sin(theta),
                cos(theta) * cos(alpha),
                -cos(theta) * sin(alpha),
                a * sin(theta),
            ],
            [0, sin(alpha), cos(alpha), d],
            [0, 0, 0, 1],
        ]
    )
    return A


ninety = 90 * (pi / 180)

a2, a3, d1, d6 = symbols("a2 a3 d1 d6")
th1, th2, th3, th4, th5, th6 = symbols("th1 th2 th3 th4 th5 th6")

A1 = get_A_matrix(0, ninety, d1, th1)
A2 = get_A_matrix(a2, 0, 0, th2)
A3 = get_A_matrix(a3, 0, 0, th3)

A4 = get_A_matrix(0, -ninety, 0, th4)
A5 = get_A_matrix(0, ninety, 0, th5)
A6 = get_A_matrix(0, 0, d6, th6)

R_30 = A1 * A2 * A3
R_63 = A4 * A5 * A6

print("R_30:")
print(R_30)
print("R_63:")
print(R_63)

T_60 = np.array(
    [
        [0.46, -0.64, -0.61, 0.61],
        [-0.68, 0.18, -0.71, -0.35],
        [0.57, 0.75, -0.35, 0.7],
        [0, 0, 0, 1],
    ]
)

ox = T_60[0][3]
oy = T_60[1][3]
oz = T_60[2][3]

a2 = 0.5
a3 = 0.5
d = 0.5

xc = ox - d * T_60[0][2]
yc = oy - d * T_60[1][2]
zc = oz - d * T_60[2][2]

theta1 = atan2(yc, xc)

D = (xc ** 2 + yc ** 2 - d ** 2 + (zc - d) ** 2 - a2 ** 2 - a3 ** 2) / (2 * a2 * a3)

theta3 = atan2(np.sqrt((1 - D ** 2)), D)
# theta3_neg = atan2(-np.sqrt(1 - D**2), D)

theta2 = atan2(zc, np.sqrt(xc ** 2 + yc ** 2 - d ** 2)) - atan2(
    a3 * np.sin(theta3), a2 + a3 * np.cos(theta3)
)

theta4 = atan2(
    -np.cos(theta1) * np.sin(theta2 + theta3) * T_60[0][2]
    - np.sin(theta1) * np.sin(theta2 + theta3) * T_60[1][2]
    + np.cos(theta2 + theta3) * T_60[2][2],
    np.cos(theta1) * np.cos(theta2 + theta3) * T_60[0][2]
    + np.sin(theta1) * np.cos(theta2 + theta3) * T_60[1][2]
    + np.sin(theta2 + theta3) * T_60[2][2],
)

theta5 = atan2(
    np.sqrt(1 - (np.sin(theta1) * T_60[0][2] - np.cos(theta1) * T_60[1][2]) ** 2),
    np.sin(theta1) * T_60[0][2] - np.cos(theta1) * T_60[1][2],
)

theta6 = atan2(
    np.sin(theta1) * T_60[0][1] - np.cos(theta1) * T_60[1][1],
    -np.sin(theta1) * T_60[0][0] + np.cos(theta1) * T_60[1][0],
)

print("\nTheta1:")
print(theta1)
print("Theta2:")
print(theta2)
print("Theta3:")
print(theta3)
print("Theta4:")
print(theta4)
print("Theta5:")
print(theta5)
print("Theta6:")
print(theta6)
