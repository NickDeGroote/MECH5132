from sympy import *


def get_A_matrix(
    a: symbols, alpha: symbols, d: symbols, theta: symbols, units: str = "radians"
) -> Matrix:
    if is_float_or_int(alpha):
        alpha = convert_to_correct_units(alpha, units)
    if is_float_or_int(theta):
        theta = convert_to_correct_units(theta, units)

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


def is_float_or_int(angle: symbols) -> bool:
    if type(angle) == float or type(angle) == int:
        return True
    else:
        return False


def convert_to_correct_units(angle: symbols, units: str) -> float:
    if units == "radians":
        pass
    elif units == "degrees":
        deg_per_rad = pi / 180
        angle = angle * deg_per_rad
    return angle


def get_euler_angles(R: Matrix) -> tuple:
    # Writing these out for my own sanity...
    r11 = R[0, 0]
    r12 = R[0, 1]
    r13 = R[0, 2]
    r21 = R[1, 0]
    r22 = R[1, 1]
    r23 = R[1, 2]
    r31 = R[2, 0]
    r32 = R[2, 1]
    r33 = R[2, 2]

    theta = atan2(sqrt(1 - r33**2), r33)
    phi = atan2(r23, r13)
    psi = atan2(r32, -r31)

    return phi, theta, psi

"""User Defined Variables"""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
units = "degrees"  # Units for alpha
theta1, theta2, theta3, theta4, theta5, theta6, d6, d2 = symbols(
    "theta1 theta2 theta3 theta4 theta5 theta6 d5 ds"
)  # Independent variables
# Note: DH table assumes the order: a, alpha, d, theta
dh_table = [
    [0, 90, 13, theta1],
    [8, 0, d2, theta2],
    [0, 90, 0, theta3],
    [0, -90, 8, theta4],
    [0, -90, 0, theta5],
    [0, 0, d6, theta6],
]  # Table for DH Convention
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""

# Find individual A matrices
init_printing()
count = 0
rotation_matrices = []
for link in dh_table[0:3]:
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
R_03 = A_tot[0:3, 0:3]
print(simplify(R_03))
print("LaTex Representation, R_03:")
print(latex(simplify(R_03)))  # Print LaTex code for matrix


count = 0
rotation_matrices = []
for link in dh_table[3:6]:
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
R_63 = A_tot[0:3, 0:3]
print(simplify(R_63))
print("LaTex Representation, R_63:")
print(latex(simplify(R_63)))  # Print LaTex code for matrix

"""
Find Euler angles
"""
print("\n")
r11, r12, r13, r21, r22, r23, r31, r32, r33 = symbols("r11 r12 r13 r21 r22 r23 r31 r32 r33")
R = Matrix([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])
print(latex(R))
rhs = transpose(R_03) * R

print("RHS:")
print(latex(simplify(rhs)))
euler_angles = get_euler_angles(simplify(rhs))
print("Phi:")
print(euler_angles[0])
print(latex(simplify(euler_angles[0])))
print("Theta:")
print(euler_angles[1])
print(latex(simplify(euler_angles[1])))
print("Psi:")
print(euler_angles[2])
print(latex(simplify(euler_angles[2])))

for i in range(0, rhs.shape[0]):
    for j in range(0, rhs.shape[1]):
        print("Element: {}".format(i+j))
        print(latex(simplify(rhs[i, j])))
