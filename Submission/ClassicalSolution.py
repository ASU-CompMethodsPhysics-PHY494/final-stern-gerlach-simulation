#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def dynamics(mass=1, N=1000, alpha=1, gamma=1,
             vy=100, vx=20, B_end=10, Y_end = 40,vz = 20):
    # We are making a range of values between
    # -1/2 and 1/2 for possible spin values in the z direction
    # Classical mechanics says nothing against the idea of spin having to be between
    # the values of -1/2 and 1/2 , the way we will interpret this from here on is that
    # the radius of the Spin-space is = 1, not sqrt(3)/2, this makes it much better as
    # well as giving us the result we wanted .Think about it to, if we sent a particle
    # with spin = 0 in the z direction, then the formula we have fails: 3/4 = s_z^2 +S_y^2 + S_x^2 as
    # unless increase S_x or S_y above 1/2, we cant equate the sides. This meanst that we are wrong
    # by contradiction. We thus must make the assumption that we can have an atom with 100% of its spin
    # in a single axis direction. This would force the bounds to be -1 to 1: From that, we can solve for S_x

    S_z   = np.random.uniform(-1, 1, N)
    S_y   = np.random.uniform(-1, 1, N)

    # we effectively do not need to worry about the S_y since it will not affect any of the motion as it is perpendicular to the
    # B field at all locations.But it is however needed to calculate the S_x since they are linearly dependent.

    S_x = np.random.choice([-1, 1], N) * np.sqrt(1 - S_y**2 - S_z**2)
    # calculate the force in the z direction, see griffiths page 182 for more info
    f_z = gamma * alpha * S_z
    f_x = gamma * alpha * S_x

    # force is constant in the z direction while in the field, thus there is a constant acceleration. Calculate using F=ma
    a_z    = f_z    / mass
    a_x = f_x / mass

    # F = 0 in the y direction, thus we can calculate the
    # time it takes for the atom to go from the beginning of the
    # magnetic field to the end
    v0x = np.random.uniform(vx-.02, vx+.02, N)
    v0y = np.random.uniform(vy,   vy+2,   N)
    v0z = np.random.uniform(vz-.02, vz+.02, N)
    
    #time to leave the field
    tbf = .19
    t = B_end / v0y
    x_xi = v0x*tbf
    x_zi = v0z * tbf
    # Calculate the z,x position as the atom leaves the magnetic field
    # lf = leaving field
    z_lf = x_zi + v0z*t + .5 * a_z * t**2
    x_lf = x_xi + v0x*t + .5 * a_x * t**2


    # The magnetic field last 20 units, lets make the screen 10 more units away
    # in these moments, there will be no acceleration at all, we neeed to recalculate
    # the velocities in each direction and maintain them through the end

    v_znew     = v0z + a_z*t
    v_x_new = v0x + a_x*t

    # calculate the time from the leaving the field to the screen
    t_new = (Y_end - B_end)/v0y

    z_f = z_lf + v_znew*t_new
    x_f = x_lf + v_x_new*t_new


    return z_f, x_f


if __name__ == '__main__':
    parameters = {
        'mass':  1,     #Mass of atom (kg)
        'N':     5000, #Number of atom
        'alpha': 1,     #Small deviation from homogeneity
        'gamma': 1,     #Gyromagnetic constant
        'vy':    100, #Velocity in the y-direction (m/s)
        'vz':    0,  #velocity in the z direction
        'vx':    0,     #Velocity in the x-direction in (m/s)
        'B_end': 20,    #y distance particle will travel
        'Y_end': 30,    #The screen location after the field
    }

    z, x = dynamics(**parameters)

    plt.scatter(x ,z)
    plt.xlabel('Unit Length')
    plt.ylabel('Unit Length')
    plt.title('Stern-Gerlach Classical Solution for 5000 Silver Atoms' )
    plt.savefig('Classical.png')
    plt.show()
