## Here we want to solve Schrodinger eqn for an electron 
## in an inhomogenous magnetic field.

## We first analyze the indepent solution first where
## the exponent that depends on time is set to 1.

## We use units where hbar = 1, so that p = k

import numpy as np
import matplotlib.pyplot as plt



## we first define the gaussian function that depends on momentum from the literature eqn 10.10


def gaussian(px,py,pz,kx,beta,n):
    
    ## the wave is strongly peaked around k, beta is the Gaussian RMS width, and n
    ## is the dimensions of the gaussian function 
    
    g = ((2*np.pi) / beta**(2))**(n/2) *np.exp(-(2*beta**(2))**(-1)*((px-kx)**(2)+py**(2)+pz**(2)))
    
    return g

def spinor_in(gaussian):
    
    ## Here we are defining the spinor function of the electron 
    ## before it enters the space containing the inhomogeneous magnetic field
    
    ## the spinor_in is the inverse fourier transform of the gaussian function
    ## as the width of the gaussian function's width increases the spinor function's
    ## width decreases and becomes sharply peaked at the center.
    
    return np.fft.ifft(gaussian)

def psi_in(spinor_in):
    
    ## define the spin up spin down coefficients  
    c_u = 1/2
    c_d = -1/2
    
    ## place the spinor function in the the spin up sin dwon basis 
    ## to define psi in which is a complex function.
    
    return np.array([c_u*spinor_in, c_d*spinor_in])
    
    
    
def plot_spinor_in(spinor_in,N, figname="plot_of_spinor_in.pdf" ):
    
    """Plot of spinor_in."""
    x = np.fft.fftfreq(N) # defines the sample positions for the inverse fourier transform
    xs = np.fft.ifftshift(x) # shifts the zero position to the center
    
    y=(1/N)*(np.abs(np.fft.ifftshift(spinor_in)))**2 # the spionor function is complex
    fig = plt.figure()                               # so we take the absolute value squared and divide by 1/N
    ax = fig.add_subplot(111)
    ax.plot(xs,y)
    
    ax.set_xlabel('position')
    ax.set_ylabel(r'$|\chi_i|^2$')
   
    

    if figname:
        fig.savefig(figname)
        print("Wrote figure to {}".format(figname))
    
    

def plot_gaussian(p,gaussian, figname="plot_of_gaussian.pdf"):
    """Plot of the gaussian."""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(p,gaussian)
    
    ax.set_xlabel('momentum')
    ax.set_ylabel('gaussian')
   
    

    if figname:
        fig.savefig(figname)
        print("Wrote figure to {}".format(figname))

    