from sympy import Matrix, sin, cos, symbols


theta1, theta2, theta4 = symbols("theta1 theta2 theta4")
d3, d4 = symbols("d3 d6")
a1, a2 = symbols("a1 a2")

A1 = Matrix([[cos(theta1),-sin(theta1), 0, a1*cos(theta1)],
             [sin(theta1), cos(theta1), 0, a1*sin(theta1)],
             [0, 0, 1, 0],
             [0, 0, 0, 1]
             ])

A2 = Matrix([[cos(theta2), sin(theta2), 0, a2*cos(theta2)],
             [sin(theta2),-cos(theta2), 0, a2*sin(theta2)],
             [0, 0, -1, 0],
             [0, 0, 0, 1]
             ])

A3 = Matrix([[1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, d3],
            [0, 0, 0, 1]
            ])
           
A4 = Matrix([[cos(theta4),-sin(theta4), 0, 0],
             [sin(theta4), cos(theta4), 0, 0],
             [0, 0, 1, d4],
             [0, 0, 0, 1]
             ])
                 
T2_0 = A1*A2
T3_0 = A1*A2*A3
T4_0 = A1*A2*A3*A4


z0 = Matrix([[0],[0],[1]])

o0 = Matrix([[0],[0],[0]])

z1 = Matrix([[A1[0,2]],
             [A1[1,2]],
             [A1[2,2]]])

z2 = Matrix([[T2_0[0,2]],
             [T2_0[1,2]],
             [T2_0[2,2]]])

z3 = Matrix([[T3_0[0,2]],
             [T3_0[1,2]],
             [T3_0[2,2]]])

o1 = Matrix([[A1[0,3]],
             [A1[1,3]],
             [A1[2,3]]])

o2 = Matrix([[T2_0[0,3]],
             [T2_0[1,3]],
             [T2_0[2,3]]])

o3 = Matrix([[T3_0[0,3]],
             [T3_0[1,3]],
             [T3_0[2,3]]])

o4 = Matrix([[T4_0[0,3]],
             [T4_0[1,3]],
             [T4_0[2,3]]])


J = Matrix([[z0.cross(o4-o0), z1.cross(o4-o1), z2, z3.cross(o4-o3)],
            [z0, z1, Matrix([[0],[0],[0]]), z3]])

print(J)




