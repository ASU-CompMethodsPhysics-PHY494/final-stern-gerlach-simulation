## Here we want to solve Schrodinger eqn for an electron 
## in an inhomogenous magnetic field.

## We first analyze the indepent solution first where
## the exponent that depends on time is set to 1.

## We use units where hbar = 1, so that p = k

import numpy as np
import matplotlib.pyplot as plt



## we first define the gaussian function that depends on momentum from the literature eqn 10.10


def gaussian(p,k,beta,n):
    
    ## the wave is strongly peaked around k, beta is the Gaussian RMS width, and n
    ## is the dimensions of the gaussian function 
    
    g = ((2*np.pi) / beta**(2))**(n/2) *np.exp(-(2*beta**(2))**(-1)*(p-k)**(2))
    
    return g

def plot_gaussian(gaussian,p, figname="plot_of_gaussian.pdf"):
    """Plot of the gaussian."""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(p,gaussian)
    
    ax.set_xlabel('p')
    ax.set_ylabel('g')
    

    if figname:
        fig.savefig(figname)
        print("Wrote figure to {}".format(figname))

    