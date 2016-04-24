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

def spinor_in(gaussian):
    
    ## Here we are defining the spinor function of the electron 
    ## before it enters the space containing the inhomogeneous magnetic field
    
    ## inverse fourier transform of the gaussian
    
    return np.fft.ifft(gaussian)
    
def plot_spinor_in(spinor_in,N, figname="plot_of_spinor_in.pdf" ):
    
    """Plot of spinor_in."""
    x = np.fft.fftfreq(N) # defines the sample positions for the inverse fourier transform
    xs = np.fft.ifftshift(x) # shifts the zero position to the center
    
    y=(1/N)*(np.abs(np.fft.ifftshift(spinor_in)))**2 # the spionor function is complex
    fig = plt.figure()                               # so we take the absolute value squared and divide by 1/N
    ax = fig.add_subplot(111)
    ax.plot(xs,y)
    
    ax.set_xlabel('position')
    ax.set_ylabel(r'$\Chi_in')
   
    

    if figname:
        fig.savefig(figname)
        print("Wrote figure to {}".format(figname))
    
    

def plot_gaussian(gaussian, figname="plot_of_gaussian.pdf"):
    """Plot of the gaussian."""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(p,gaussian)
    
    ax.set_xlabel('momentum')
    ax.set_ylabel('gaussian')
   
    

    if figname:
        fig.savefig(figname)
        print("Wrote figure to {}".format(figname))

    