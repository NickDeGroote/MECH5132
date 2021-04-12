from sympy import symbols, Matrix, lambdify
import numpy as np
import matplotlib.pyplot as plt
from sympy.plotting import plot
from typing import Tuple, List


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


def get_theta_lengths(points: np.array) -> Tuple[int, int]:
    theta1_dist = 0
    theta2_dist = 0
    for point, next_point in zip(points, points[1:]):
        theta1_dist += abs(next_point[0] - point[0])
        theta2_dist += abs(next_point[1] - point[1])
    return theta1_dist, theta2_dist


def labmdify_function(polynomial):
    t = symbols("t")
    domain = np.linspace(polynomial[1], polynomial[2], 100)
    q_lambda = lambdify(t, polynomial[0], "numpy")
    q_eval = q_lambda(domain)
    return domain, q_eval


def plot_polynomials(polynomial_list, title):
    plt.figure()
    for polynomial_vals in polynomial_list:
        plt.plot(polynomial_vals[0], polynomial_vals[1], "b")
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (Radians)")


def normalize_polynomials(tf, polynomial_vals):
    normalized_poly_vals = []
    norm_factor = tf / polynomial_vals[-1][0][-1]
    for polynomial in polynomial_vals:
        norm_poly_domain = np.multiply(polynomial[0], norm_factor)
        normalized_poly_vals.append((norm_poly_domain, polynomial[1]))
    return normalized_poly_vals


def get_velocity_signs(points):
    velocities1 = []
    velocities2 = []
    for point, next_point in zip(points, points[1:]):
        if next_point[0] > point[0]:
            velocities1.append(1)
        else:
            velocities1.append(-1)
        if next_point[1] > point[1]:
            velocities2.append(1)
        else:
            velocities2.append(-1)
    return np.asarray(velocities1), np.asarray(velocities2)


def get_normalized_cubics(tf, points1, points2, velocities1, velocities2) -> Tuple:
    t = symbols("t")
    velocities1 = np.insert(velocities1, 0, 0)
    velocities2 = np.insert(velocities2, 0, 0)

    polynomials1 = []
    polynomials2 = []
    time1 = 0
    time2 = 0
    for i in range(0, len(points1) - 1):
        q1_initial = points1[i]
        q1_final = points1[i + 1]

        v1_initial = velocities1[i]
        v1_final = velocities1[i + 1]

        delta_t1 = abs(q1_final - q1_initial)

        [M1, b1] = cubic_polynomial_trajectory(
            q1_initial, v1_initial, q1_final, v1_final, time1, time1 + delta_t1
        )
        a1 = M1.inv() * b1
        q1 = a1[0] + a1[1] * t + a1[2] * t ** 2 + a1[3] * t ** 3
        polynomials1.append((q1, time1, time1 + delta_t1))
        time1 = time1 + delta_t1

    for i in range(0, len(points2) - 1):
        q2_initial = points2[i]
        q2_final = points2[i + 1]
        v2_initial = velocities2[i]
        v2_final = velocities2[i + 1]
        delta_t2 = abs(q2_final - q2_initial)

        [M2, b2] = cubic_polynomial_trajectory(
            q2_initial, v2_initial, q2_final, v2_final, time2, time2 + delta_t2
        )
        a2 = M2.inv() * b2
        q2 = a2[0] + a2[1] * t + a2[2] * t ** 2 + a2[3] * t ** 3
        polynomials2.append((q2, time2, time2 + delta_t2))
        time2 = time2 + delta_t2

    print(polynomials1)
    print(polynomials2)

    polynomial_vals1 = []
    for polynomial in polynomials1:
        polynomial_vals1.append(labmdify_function(polynomial))

    polynomial_vals2 = []
    for polynomial in polynomials2:
        polynomial_vals2.append(labmdify_function(polynomial))

    normalized_polynomials1 = normalize_polynomials(tf, polynomial_vals1)
    normalized_polynomials2 = normalize_polynomials(tf, polynomial_vals2)
    plot_polynomials(normalized_polynomials1, r"${\Theta}_1$ vs. Time ")
    plot_polynomials(normalized_polynomials2, r"${\Theta}_2$ vs. Time ")
    plt.show()
    return normalized_polynomials1, normalized_polynomials2


tf = 5
points_1 = np.array([3*np.pi/2, np.pi/2])
points_2 = np.array([0, -1.135, 0])
velocities_1 = np.array([0, 0])
velocities_2 = np.array([0, 0, 0])
normalized_polynomials = get_normalized_cubics(tf, points_1, points_2, velocities_1, velocities_2)
