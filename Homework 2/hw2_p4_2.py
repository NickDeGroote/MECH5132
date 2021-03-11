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


"""User Defined Variables"""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
"""""" """""" """""" """""" """""" """""" """""" """""" """""" """""" """""" ""
units = "degrees"  # Units for alpha
theta1, theta2, theta3, theta4, theta5, theta6, d2, d5, d6, ds = symbols(
    "theta1 theta2 theta3 theta4 theta5 theta6 d2 d5 d6 ds"
)  # Independent variables
# Note: DH table assumes the order: a, alpha, d, theta
dh_table = [
    [0, 90, 13, theta1],
    [8, 0, ds, theta2],
    [0, 90, 0, theta3],
    [0, -90, 8, theta4],
    [0, -90, 0, theta5],
    [0, 0, d5, theta6],
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
    count = count + 1


# Find composite rotation matrix by multiplying individual A matrices
A_tot = eye(4)
for A in rotation_matrices:
    A_tot = A_tot * A

r11, r12, r13, r21, r22, r23, r31, r32, r33, R = symbols(
    "r11 r12 r13 r21 r22 r23 r31 r32 r33 R")

xc, yc, zc, a2, a3, d, dist, ox, oy, oz = symbols(
    "xc yc zc a2 a3 d dist ox, oy, oz")

R = Matrix([[r11, r12, r13],
            [r21, r22, r23],
            [r31, r32, r33]])

# o = Matrix([[16],
#            [-d2],
#            [13+d6]])

o = Matrix([[ox],[oy],[oz]])

oc = o-d6*R*Matrix([[0],
                    [0],
                    [1]])

# d = 8
# a2 = 8
# a3 = 8

# xc = oc[0]
# yc = oc[1]
# zc = oc[2]



dist = xc**2 + yc**2 - d**2

EU_th1 = atan2((dist)**0.5, d)
EU_th2 = atan2((dist)**0.5, zc - d)
EU_th3 = atan2((dist + (zc - d)**2 - a2**2 - a3**2)/(2*a2*a3),
               (1 - ((dist + (zc-d)**2 - a2**2 - a3**2)/(2 * a2**2 * a3**2)))**0.5)

#print("o")
#print(pretty(o))
#print("\nwrist center:")
#print(pretty(oc))
#print("\nEuler Theta 1")
#print(EU_th1)

print("LaTex Representation end effector:")
print(latex(o))

print("LaTex Representation wrist center:")
print(latex(oc))

print("LaTex Representation EU_th1:")
print(latex(EU_th1))  # Print LaTex code for matrix

print("LaTex Representation EU_th2:")
print(latex(EU_th2))  # Print LaTex code for matrix

print("LaTex Representation EU_th3:")
print(latex(EU_th3))  # Print LaTex code for matrix

