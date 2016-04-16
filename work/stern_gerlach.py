#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def dynamics(mass=1, N=1000, alpha=1, gamma=1,
             vy=100, vx=20, y_end=10):
    # We are making a range of values between
    # -1/2 and 1/2 for possible spin values in the z direction
    L_z = np.random.uniform(-1, 1, N)
    L_x = np.random. np.sqrt(1-L_z**2)

    #calculate the force in the z direction, see griffiths page 182 for more info
    f_z = gamma * alpha*L_z
    f_x = (np.random.choice([-1, 1], N) *
            gamma * alpha*L_x)

    #force is constant in the z direction, thus there is a constant acceleration. Calculate using F=ma
    a_z = f_z / mass
    a_x = f_x / mass

    # F = 0 in the y direction, thus we can calculate the
    # time it takes for the atom to go from the beginning of the
    # magnetic field to the end.
    t = y_end / vy

    # Calculate the final z position
    z_final = .5 * a_z * t**2
    x_final = .5 * a_x * t**2

    return z_final, x_final


if __name__ == '__main__':
    parameters = {
        'mass':  1,    #Mass of atom (kg)
        'N':     1000, #Number of atom
        'alpha': 1,    #Small deviation from homogeneity
        'gamma': 1,    #Gyromagnetic constant
        'vy':    500,  #Velocity in the y-direction (m/s)
        'vx':    20,   #Velocity in the x-direction in (m/s)
        'y_end': 20    #y distance particle will travel
    }

    z, x = dynamics(**parameters)
    plt.scatter(x, z)
    plt.show()
