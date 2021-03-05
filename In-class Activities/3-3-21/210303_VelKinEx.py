from sympy import Matrix, sin, cos, symbols


theta1, theta2, theta4, theta5, theta6 = symbols("theta1 theta2 theta4 theta5 theta6")
d2, d3, d6 = symbols("d2 d3 d6")

A1 = Matrix([[cos(theta1), 0 , -sin(theta1), 0],
       [sin(theta1), 0, cos(theta1), 0],
       [0, -1,0, 0],
       [0,0,0,1]
       ])

A2 = Matrix([[cos(theta2), 0 , sin(theta2), 0],
       [sin(theta2), 0, -cos(theta2), 0],
       [0, 1,0, d2],
       [0,0,0,1]
       ])


A3 = Matrix([[1, 0 ,0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, d3],
       [0,0,0,1]
       ])


A4 = Matrix([[cos(theta4), 0 , -sin(theta4), 0],
       [sin(theta4), 0, cos(theta4), 0],
       [0, -1,0, 0],
       [0,0,0,1]
       ])


A5 = Matrix([[cos(theta5), 0 , sin(theta5), 0],
       [sin(theta5), 0, -cos(theta5), 0],
       [0, -1,0, 0],
       [0,0,0,1]
       ])


A6 = Matrix([[cos(theta6), -sin(theta6), 0, 0],
       [sin(theta6), cos(theta6), 0, 0],
       [0, 0, 1, d6],
       [0,0,0,1]
       ])

T2_0 = A1*A2
T3_0 = A1*A2*A3
T4_0 = A1*A2*A3*A4
T5_0 = A1*A2*A3*A4*A5
T6_0 = A1*A2*A3*A4*A5*A6

z0 = Matrix([[0],[0],[1]])

o0 = Matrix([[0],[0],[0]])

z1 = Matrix([[A1[0,2]],
             [A1[1,2]],
             [A1[2,2]]])

o1 = Matrix([[A1[0,3]],
             [A1[1,3]],
             [A1[2,3]]])

o2 = Matrix([[T2_0[0,3]],
             [T2_0[1,3]],
             [T2_0[2,3]]])

z2 = Matrix([[T2_0[0,2]],
             [T2_0[1,2]],
             [T2_0[2,2]]])

z3 = Matrix([[T3_0[0,2]],
             [T3_0[1,2]],
             [T3_0[2,2]]])

o3 = Matrix([[T3_0[0,3]],
             [T3_0[1,3]],
             [T3_0[2,3]]])

o4 = Matrix([[T4_0[0,3]],
             [T4_0[1,3]],
             [T4_0[2,3]]])

z4 = Matrix([[T4_0[0,2]],
             [T4_0[1,2]],
             [T4_0[2,2]]])

z5 = Matrix([[T5_0[0,2]],
             [T5_0[1,2]],
             [T5_0[2,2]]])

o5 = Matrix([[T5_0[0,3]],
             [T5_0[1,3]],
             [T5_0[2,3]]])

o6 = Matrix([[T6_0[0,3]],
             [T6_0[1,3]],
             [T6_0[2,3]]])

J = Matrix([[z0.cross(o6-o0), z1.cross(o6-o1), z2, z3.cross(o6-o3), z4.cross(o6-o3), z5.cross(o6-o3)],
            [z0, z1, Matrix([[0],[0],[0]]), z3, z4, z5]])

print(J[:,3])




