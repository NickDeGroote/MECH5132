from sympy import symbols, Matrix, sin, cos, pi, atan2, trigsimp


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

a1, a2, d3, d4 = symbols("a1 a2 d3 d4")
th1, th2, th4 = symbols("th1 th2 th4")

A1 = get_A_matrix(a1, 0, 0, th1)
A2 = get_A_matrix(a2, 2 * ninety, 0, th2)
A3 = get_A_matrix(0, 0, d3, 0)
A4 = get_A_matrix(0, 0, d4, th4)

T_40 = A1 * A2 * A3 * A4

print("T_40:")
print(trigsimp(T_40))
