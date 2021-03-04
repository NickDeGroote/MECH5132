from sympy import Matrix sin cos


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

z0 = Matrix([0],[0],[1])

z1 = Matrix([[A1[0][2]],
             [A1[1][2]],
             [A1[2][2]]])

T2_0 = A1*A2

z2 = Matrix([[T2_0[0][2]],
             [T2_0[1][2]],
             [T2_0[2][2]]])








