# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:45:19 2021

@author: jonan
"""
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

## Coordinate matrices from HW2
# =============================================================================
# x_1 = (0, L_1*np.cos(theta_1))
#     y_1 = (0, L_1*np.sin(theta_1))
#     x_2 = (L_1*np.cos(theta_1), L_1*np.cos(theta_1) + L_2*np.cos(theta_1+theta_2))
#     y_2 = (L_1*np.sin(theta_1), L_1*np.sin(theta_1) + L_2*np.sin(theta_1+theta_2))
# =============================================================================

def A_position_matrix(th1,th2,l):
    """
    [a1, a2, a3]
    """
    a = np.array([[l*cos(th1), l*sin(th1)],
                  [l*cos(th1) + l/2*cos(th1+th2), l*sin(th1) + l/2*sin(th1+th2)],
                  [l*cos(th1) + l*cos(th1+th2), l*sin(th1) + l*sin(th1+th2)]])
    a = np.transpose(a)
    return a


## Attractive force (chapter 7, slide 23)
def F_att(a, a_final, d, zeta):  
    nrm = np.linalg.norm(a - a_final)
    if nrm <= d:
        f = -zeta * (a - a_final)
    else:
        f = -d*zeta*(a - a_final) / nrm
    return f


## Repulsive force (chapter 7, slide 24)
def F_rep(a, b, rho_0, eta):
    
    F = np.zeros_like(a)
        
    ## check every control point individually
    for j in range(a.shape[1]):  # every column in a is a control point
        a_j = a[:,j]
        
        ## find minimum distance to an obstacle and identify obstacle
        dist_min = 1e3
        for i in range(b.shape[1]):
            dist = np.linalg.norm(a_j - b[:,i])
            if dist < dist_min:
                dist_min = dist
                idx = i  # index of the closest obstacle
        rho = dist_min

        if rho > rho_0:
            f = np.array([0,0])
        else:
            grad = (a_j - b[:,idx]) / np.linalg.norm(a_j - b[:,idx])
            f = eta * (1/rho - 1/rho_0) * rho**(-2) * grad
            
        F[:,i] = f
        
    return F

## Calculate jacobians of the 3 control points (chapter 7, slide 27)
def jacobians(th1, th2, l):
    J1 = np.array([[-l*sin(th1), 0],
                   [ l*cos(th1), 0]])
    
    J2 = np.array([[-l*sin(th1) - l/2*sin(th1+th2), -l/2*sin(th1+th2)],
                   [ l*cos(th1) + l/2*cos(th1+th2),  l/2*cos(th1+th2)]])
    
    J3 = np.array([[-l*sin(th1) - l*sin(th1+th2), -l*sin(th1+th2)],
                   [ l*cos(th1) + l*cos(th1+th2),  l*cos(th1+th2)]])
    
    return [J1, J2, J3]


## Calculate forces (chapter 7, slide 28)
def calculate_force(th1, th2, F_att, F_rep, J):
    F = np.array([0.0, 0.0])
    
    for i in range(F_att.shape[1]):
        J_i_t = np.transpose(J[i])
        F_att_i = F_att[:,i]
        F_rep_i = F_rep[:,i]
        F += J_i_t.dot(F_att_i) + J_i_t.dot(F_rep_i)
        
    return F
    
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
      
    
if __name__ == "__main__":
    ## Prior tests
    l = 0.2
    # q_0 = np.array([3*np.pi/2, 0])
    # q_f = np.array([np.pi/2, 0])
    
    # A_0 = np.array([[0,-l], [0,-3*l/2], [0,-2*l]])
    A_f = np.array([[0,l], [0,3*l/2], [0,2*l]])
    # A_collision_test = A_position_matrix(3.247, 1.36, l)
    
    # A_0 = np.transpose(A_0)
    A_f = np.transpose(A_f)
    
    obstacles = np.array([[0.22, -0.22], [-0.22, -0.22]])
    obstacles = np.transpose(obstacles)

    # f_att = F_att(A_0, A_f, l, 0.1)
    
    # f_rep = F_rep(A_collision_test, obstacles, 0.1, 1e-3)
    
    # theta1 = q_0[0]
    # theta2 = q_0[1]
    
    # Force = calculate_force(theta1, theta2, f_att, f_rep, jacobians(theta1, theta2, l))
    
    ## Full procedure
# ============================================================================
    # Modify thetas to the configuation of the manipulator
    l = 0.2
    alpha = 0.029
    theta1 = 0
    theta2 = 0
    
    q_0 = np.array([3*np.pi/2,0])
    q_f = np.array([np.pi/2,0])
    q = q_0
    qq = [q_0]
    error = 1e3
    
    while error > 1e-2:
        # Calculate position of the manipulator in workspace
        A = A_position_matrix(q[0], q[1], l)
    
        # Calculate attractive and repulsive artificial forces
        f_att = F_att(A, A_f, l, 0.1)
        f_rep = F_rep(A, obstacles, 0.1, 1e-4)
    
        # Calculate Jacobians
        J = jacobians(q[0], q[1], l)
        print(pretty(J))
        
        # Calculate forces
        Force = calculate_force(q[0], q[1], f_att, f_rep, J)
        
        # Update q
        q = q + alpha * Force/np.linalg.norm(Force)
        error = np.linalg.norm(q - q_f)
        # print(error)
        
        qq.append(q)
# ============================================================================
     
# Part B


    
    

    