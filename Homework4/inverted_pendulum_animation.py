"""
General Numerical Solver for the 1D Time-Dependent Schrodinger's equation.

adapted from code at http://matplotlib.sourceforge.net/examples/animation/double_pendulum_animated.py

Double pendulum formula translated from the C code at
http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import time
from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation


class DoublePendulum:
    """Double Pendulum Class

    init_state is [theta1, omega1, theta2, omega2] in degrees,
    where theta1, omega1 is the angular position and velocity of the first
    pendulum arm, and theta2, omega2 is that of the second pendulum arm
    """

    def __init__(
        self,
        init_state=[130, 0, -20, 0],
        L1=0.5,  # length of pendulum 1 in m
        L2=0.5,  # length of pendulum 2 in m
        M1=0.2,  # mass of pendulum 1 in kg
        M2=0.2,  # mass of pendulum 2 in kg
        G=9.8,  # acceleration due to gravity, in m/s**2
        origin=(0, 0),
    ):
        self.init_state = np.asarray(init_state, dtype="float")
        self.params = (L1, L2, M1, M2, G)
        self.origin = origin
        self.time_elapsed = 0

        self.state = self.init_state * np.pi / 180.0
        self.theta1_sp = 90.0 * np.pi / 180.0
        self.theta2_sp = 0.0 * np.pi / 180.0
        self.kp1 = 10
        self.kd1 = 0.75
        self.kp2 = 10
        self.kd2 = 1.5

        # Parameter tracking
        self.theta1_tracker = []
        self.theta2_tracker = []
        self.tau1_tracker = []
        self.tau2_tracker = []
        self.time_tracker = []

    def position(self):
        """compute the current x,y positions of the pendulum arms"""
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum(
            [
                self.origin[0],
                L1 * cos(self.state[0]),
                L2 * cos(self.state[0] + self.state[2]),
            ]
        )
        y = np.cumsum(
            [
                self.origin[1],
                L1 * sin(self.state[0]),
                L2 * sin(self.state[0] + self.state[2]),
            ]
        )
        return (x, y)

    def energy(self):
        """compute the energy of the current state"""
        (L1, L2, M1, M2, G) = self.params

        x = np.cumsum([L1 * sin(self.state[0]), L2 * sin(self.state[2])])
        y = np.cumsum([-L1 * cos(self.state[0]), -L2 * cos(self.state[2])])
        vx = np.cumsum(
            [
                L1 * self.state[1] * cos(self.state[0]),
                L2 * self.state[3] * cos(self.state[2]),
            ]
        )
        vy = np.cumsum(
            [
                L1 * self.state[1] * sin(self.state[0]),
                L2 * self.state[3] * sin(self.state[2]),
            ]
        )

        U = G * (M1 * y[0] + M2 * y[1])
        K = 0.5 * (M1 * np.dot(vx, vx) + M2 * np.dot(vy, vy))

        return U + K

    def dstate_dt(self, state, t):
        """compute the derivative of the given state"""
        (M1, M2, L1, L2, G) = self.params

        dydx = np.zeros_like(state)
        dydx[0] = state[1]
        dydx[2] = state[3]

        theta1 = state[0]
        theta2 = state[2]

        error_theta1 = self.theta1_sp - state[0]
        error_theta2 = self.theta2_sp - state[2]

        tau1 = min(self.kp1 * error_theta1 - state[1] * self.kd1, 50)
        tau2 = min(self.kp2 * error_theta2 - state[3] * self.kd2, 50)

        dydx[1] = (
            2 * L2 * tau1
            - 2 * L2 * tau2
            - 2 * L1 * tau2 * cos(theta2)
            + L1 ** 2 * L2 * M2 * state[1] ** 2 * sin(2 * theta2)
            + G * L1 * L2 * M2 * cos(theta1 + 2 * theta2)
            + 2 * L1 * L2 ** 2 * M2 * state[1] ** 2 * sin(theta2)
            + 2 * L1 * L2 ** 2 * M2 * state[3] ** 2 * sin(theta2)
            - 2 * G * L1 * L2 * M1 * cos(theta1)
            - G * L1 * L2 * M2 * cos(theta1)
            + 4 * L1 * L2 ** 2 * M2 * state[1] * state[3] * sin(theta2)
        ) / (L1 ** 2 * L2 * (2 * M1 + M2 - M2 * cos(2 * theta2)))

        dydx[3] = -(
            L2 ** 2 * M2 * tau1
            - L1 ** 2 * M2 * tau2
            - L1 ** 2 * M1 * tau2
            - L2 ** 2 * M2 * tau2
            + L1 * L2 * M2 * tau1 * cos(theta2)
            - 2 * L1 * L2 * M2 * tau2 * cos(theta2)
            + L1 * L2 ** 3 * M2 ** 2 * state[1] ** 2 * sin(theta2)
            + L1 ** 3 * L2 * M2 ** 2 * state[1] ** 2 * sin(theta2)
            + L1 * L2 ** 3 * M2 ** 2 * state[3] ** 2 * sin(theta2)
            - G * L1 * L2 ** 2 * M2 ** 2 * cos(theta1)
            + L1 ** 2 * L2 ** 2 * M2 ** 2 * state[1] ** 2 * sin(2 * theta2)
            + (L1 ** 2 * L2 ** 2 * M2 ** 2 * state[3] ** 2 * sin(2 * theta2)) / 2
            - G * L1 ** 2 * L2 * M2 ** 2 * sin(theta1) * sin(theta2)
            + L1 ** 2 * L2 ** 2 * M2 ** 2 * state[1] * state[3] * sin(2 * theta2)
            + L1 ** 3 * L2 * M1 * M2 * state[1] ** 2 * sin(theta2)
            + G * L1 * L2 ** 2 * M2 ** 2 * cos(theta1) * cos(theta2) ** 2
            + 2 * L1 * L2 ** 3 * M2 ** 2 * state[1] * state[3] * sin(theta2)
            - G * L1 * L2 ** 2 * M1 * M2 * cos(theta1)
            - G * L1 * L2 ** 2 * M2 ** 2 * cos(theta2) * sin(theta1) * sin(theta2)
            - G * L1 ** 2 * L2 * M1 * M2 * sin(theta1) * sin(theta2)
        ) / (L1 ** 2 * L2 ** 2 * M2 * (-M2 * cos(theta2) ** 2 + M1 + M2))

        self.theta1_tracker.append(state[0])
        self.theta2_tracker.append(state[2])
        self.tau1_tracker.append(tau1)
        self.tau2_tracker.append(tau2)
        self.time_tracker.append(self.time_elapsed)

        return dydx

    def step(self, dt):
        """execute one time step of length dt and update state"""
        self.state = integrate.odeint(self.dstate_dt, self.state, [0, dt])[1]
        self.time_elapsed += dt


# ------------------------------------------------------------
# set up initial state and global variables
pendulum = DoublePendulum([270.0, 0.0, 0.0, 0.0])
dt = 1.0 / 100  # 100 fps

# ------------------------------------------------------------
# set up figure and animation
fig = plt.figure()
ax = fig.add_subplot(
    111, aspect="equal", autoscale_on=False, xlim=(-1.25, 1.25), ylim=(-1.25, 1.25)
)
ax.grid()
ax.set_xlabel("x (meters)")
ax.set_xlabel("y (meters)")
ax.set_title("Double Pendulum Animation (PD Control)")

fig_theta = plt.figure()
ax_theta = fig_theta.add_subplot(111, autoscale_on=True)
ax_theta.grid()

(line,) = ax.plot([], [], "o-", lw=2)
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
energy_text = ax.text(0.02, 0.90, "", transform=ax.transAxes)


def init():
    """initialize animation"""
    line.set_data([], [])
    time_text.set_text("")
    energy_text.set_text("")
    return line, time_text, energy_text


def animate(i):
    """perform animation step"""
    global pendulum, dt
    pendulum.step(dt)

    line.set_data(*pendulum.position())
    # time_text.set_text('time = %.1f' % pendulum.time_elapsed)
    return line, time_text, energy_text


def simulate(pendulum):
    """perform animation step"""
    for i in range(0, 5000):
        pendulum.step(1 / 2000)


# choose the interval based on dt and the time to animate one step
from time import time, sleep

t0 = time()
#animate(0)
t1 = time()
interval = 1000 * dt - (t1 - t0)


#ani = animation.FuncAnimation(
#    fig, animate, frames=125, interval=interval, blit=True, init_func=init)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html


simulate(pendulum)
ax_theta.plot(pendulum.time_tracker, pendulum.theta1_tracker)
ax_theta.plot(pendulum.time_tracker, pendulum.theta2_tracker)
ax_theta.legend(["Theta 1", "Theta 2"])
ax_theta.set_xlabel("Time")
ax_theta.set_ylabel("Angle (radians)")
ax_theta.set_title("Double Pendulum Angles Over Time (PD Control)")

# writer = PillowWriter(fps=25)
#ani.save("double_pendulum_pd.gif", fps=30)

plt.show()
