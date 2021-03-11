import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = plt.axes(xlim=(-10,10),ylim=(-10,10))
ax.set_aspect('equal')
lines = plt.plot([])
arm_1, = ax.plot([], [], lw=2)
arm_2, = ax.plot([], [], lw=2)
arm_3, = ax.plot([], [], lw=2)

def init():
    arm_1.set_data([], [])
    arm_2.set_data([], [])
    arm_3.set_data([], [])
    return arm_1, arm_2, arm_3,

def animate(frame):
    time = frame/1000
    
    # Part c i
    # theta_1 = 0
    # theta_2 = 0
    # theta_3 = 0
    
    # Part c ii
    # theta_1 = 10
    # theta_2 = 20
    # theta_3 = 30
    
    # Part c iii
    # theta_1 = 90
    # theta_2 = 90
    # theta_3 = 90
    
    # Part d i
    # theta_1 = 2*np.pi*np.sin(time) #0
    # theta_2 = 0#2*np.pi*np.sin(time)
    # theta_3 = 0#2*np.pi*np.sin(time)
    
    # Part d ii
    theta_1 = 2*np.pi*np.sin(time)
    theta_2 = 2*np.pi*np.sin(time)
    theta_3 = 2*np.pi*np.sin(time)
    
    L_1 = 4
    L_2 = 3
    L_3 = 2
    x_1 = (0, L_1*np.cos(theta_1))
    y_1 = (0, L_1*np.sin(theta_1))
    x_2 = (L_1*np.cos(theta_1), L_1*np.cos(theta_1) + L_2*np.cos(theta_1+theta_2))
    y_2 = (L_1*np.sin(theta_1), L_1*np.sin(theta_1) + L_2*np.sin(theta_1+theta_2))
    x_3 = (L_1*np.cos(theta_1) + L_2*np.cos(theta_1+theta_2),
                   L_1*np.cos(theta_1) + L_2*np.cos(theta_1+theta_2) + L_3*np.cos(theta_1+theta_2+theta_3))
    y_3 = (L_1*np.sin(theta_1) + L_2*np.sin(theta_1+theta_2),
                   L_1*np.sin(theta_1) + L_2*np.sin(theta_1+theta_2) + L_3*np.sin(theta_1+theta_2+theta_3))
    arm_1.set_data(x_1, y_1)
    arm_2.set_data(x_2, y_2)
    arm_3.set_data(x_3, y_3)
    return arm_1, arm_2, arm_3,
    
robot = FuncAnimation(fig, animate, frames=500, interval=10, repeat=False, blit = True)
plt.show()
robot.save('robot.gif', fps=50)