import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
parameters = {'mass': 1, #mass of atom kg
              'N': 1000, # Number of atom
              'alpha': 1, #small deviation from homogeneity
               'gamma': 1, #gyromagnetic constant 
              'vy': 500, #velocity in the y-direction in m / s
              'vx': 20, # velocity in the x-direction in m / s
              'y_end': 20 #this is the location that we are stopping in the y direction
             }

def dynamics(N = parameters['N'],mass = parameters['mass'], y_end = parameters['y_end'], vy = parameters['vy'],gamma = parameters['gamma'], alpha = parameters['alpha']):
    #We are making a range of values between -1/2 and 1/2 for possible spin values in the z direction
    L_z =  np.random.uniform(-1,1,N)
    L_x = np.sqrt(1-L_z**2)
    L_x2 =-np.sqrt(1-L_z**2)

    #calculate the force in the z direction, see griffiths page 182 for more info
    f_z = gamma * alpha*L_z
    f_x = gamma * alpha*L_x
    f_x2 = gamma * alpha*L_x2
    
    #force is constant in the z direction, thus there is a constant acceleration. Calculate using F=ma
    a_z = f_z / mass
    a_x = f_x / mass
    a_x2 = f_x2 / mass
    
    #F = 0 in the y direction, thus we can calculate the time it takes for the atom to go from the beginning of the
    #magnetic field to the end. 
    t = y_end/vy
    
    #calculate the final z position
    z_final = .5 * a_z * t**2  
    x_final = .5 * a_x * t**2
    x_final2 = .5 * a_x2 * t**2

    return z_final, x_final, x_final2
z,x,x2  = dynamics()
plt.scatter(x,z)
plt.scatter(x2,z)
plt.show()
