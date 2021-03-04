from sympy import *


def get_A_matrix(
    a: symbols, alpha: symbols, d: symbols, theta: symbols, units: str = "radians"
) -> Matrix:
    if units == "radians":
        pass
    elif units == "degrees":
        deg_per_rad = pi / 180
        alpha = alpha * deg_per_rad

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


"""User Defined Variables"""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
units = "degrees"  # Units for alpha
theta1, theta3, a1, a3, d2 = symbols("theta1 theta3 a1 a3 d2")  # Independent variables
# Note: DH table assumes the order: a, alpha, d, theta
dh_table = [
    [0, 90, 0, theta1],
    [0, -90, d2, 0],
    [a3, 0, 0, theta3],
]  # Table for DH Convention
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# Find individual A matrices
init_printing()
count = 0
rotation_matrices = []
for link in dh_table:
    a = link[0]
    alpha = link[1]
    d = link[2]
    theta = link[3]
    curr_a_matrix = get_A_matrix(a, alpha, d, theta, units)
    rotation_matrices.append(curr_a_matrix)
    print("\nRotation matrix from frame {} to frame {}:".format(count, count + 1))
    print(pretty(curr_a_matrix))
    print("LaTex Representation:")
    print(latex(curr_a_matrix))  # Print LaTex code for matrix
    count = count + 1

# Find composite rotation matrix by multiplying individual A matrices
A_tot = eye(4)
for A in rotation_matrices:
    A_tot = A_tot * A
print("\nComposite Rotation Matrix:")
print(simplify(A_tot))
print("LaTex Representation:")
print(latex(simplify(A_tot)))  # Print LaTex code for matrix
