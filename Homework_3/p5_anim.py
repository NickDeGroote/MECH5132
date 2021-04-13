import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = plt.axes(xlim=(-0.5,0.5),ylim=(-0.5,0.5))
ax.set_aspect('equal')
plt.plot()
plt.plot(0.22,-0.22,'ro') 
plt.plot(-0.22,-0.22,'ro') 
lines = plt.plot([])
arm_1, = ax.plot([], [], lw=2)
arm_2, = ax.plot([], [], lw=2)

def init():
    arm_1.set_data([], [])
    arm_2.set_data([], [])
    
    return arm_1, arm_2,

def animate(frame):
    time = frame/1000
    
    # theta_1 = 2*np.pi*np.sin(time)
    # theta_2 = 2*np.pi*np.sin(time)
    
    theta_1 = 0.202642367284676*time**3 - 0.954929658551372*time**2 + 4.71238898038469
    
    if time <= 2.5:
        theta_2 = -1.55252382153739*time**3 + 7.9295154185022*time**2 - 12.0*time + 4.53999999999999
        
    else:
        theta_2 = 1.55252382153739*time**3 - 2.6431718061674*time**2
        
    
    L_1 = 0.2
    L_2 = 0.2
    x_1 = (0, L_1*np.cos(theta_1))
    y_1 = (0, L_1*np.sin(theta_1))
    x_2 = (L_1*np.cos(theta_1), L_1*np.cos(theta_1) + L_2*np.cos(theta_1+theta_2))
    y_2 = (L_1*np.sin(theta_1), L_1*np.sin(theta_1) + L_2*np.sin(theta_1+theta_2))
    
    arm_1.set_data(x_1, y_1)
    arm_2.set_data(x_2, y_2)
    
    return arm_1, arm_2,

frms = 5000    
robot = FuncAnimation(fig, animate, frames=frms, interval=(5/frms)*1000, repeat=False, blit = True)
plt.show()
#robot.save('robot.mp4', writer='ffmpeg', fps=60)