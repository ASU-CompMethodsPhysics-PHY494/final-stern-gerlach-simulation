
import numpy as np
from matplotlib import pyplot as plt

def gaussian(px, pz, kx, kz, beta, n):
    ## the wave is strongly peaked around k, beta is the Gaussian RMS width, and n
    ## is the dimensions of the gaussian function
    return (2 * np.pi / beta**2)**(n/2) * \
            np.exp(-1/(2 * beta**2) * \
            ((px-kx)**2 + (pz-kz)**2))

m = .01

dx = .1
dz = .1
dt = .02

x0, x1 = -10, 10
z0, z1 = -10, 10
T = 1000

B0 = .1
alpha = .5  # Z velocity factor
m = 50  # Diffusion coefficient

Nx = round(1 + (x1 - x0) / dx)
Nz = round(1 + (z1 - z0) / dz)
Nt = round(1 + T / dt)

x_range = np.linspace(x0, x1, Nx)
x_sq = 2*np.meshgrid(np.zeros(Nx-2), x_range[1:-1])[1] / (x1-x0)
z_range = np.linspace(z0, z1, Nz)
z_sq = 2*np.meshgrid(z_range[1:-1], np.zeros(Nz-2))[0] / (z1-z0)

Psi1 = np.zeros((Nz, Nx), dtype=complex)
Psi2 = np.zeros((Nz, Nx), dtype=complex)
Psi_next = np.zeros((Nz, Nx), dtype=complex)

for i, xi in enumerate(x_range):
    for j, zj in enumerate(z_range):
        Psi1[j, i] = np.exp(-(xi**2 + zj**2)*2)
        Psi2[j, i] = Psi1[j, i]

plt.ion()
P = Psi1
im = plt.imshow(P.real, extent=[x0, x1, z0, z1])
cb = plt.colorbar(im)
for k in range(Nt):
    # Solve this Hamiltonian: http://mathurl.com/zwzt59e.png
    Psi_next[1:-1, 1:-1] = Psi1[1:-1, 1:-1] + 1j/(2*m) * (dt * (
        (Psi1[2:  , 1:-1] - 2*Psi1[1:-1, 1:-1] + Psi1[ :-2, 1:-1])/dz**2  +
        (Psi1[1:-1, 2:  ] - 2*Psi1[1:-1, 1:-1] + Psi1[1:-1,  :-2])/dx**2)) + \
        -z_sq*alpha*dt/(2*dz) * (Psi1[:-2, 1:-1] - Psi1[2:, 1:-1]) - \
        1j * (B0 + alpha*x_sq) * dt/(2*dx) * (Psi2[1:-1, :-2] - Psi2[1:-1, 2:])
    Psi2[1:-1, 1:-1] = Psi2[1:-1, 1:-1] + 1j/(2*m) * (dt * (
        (Psi2[2:  , 1:-1] - 2*Psi2[1:-1, 1:-1] + Psi2[ :-2, 1:-1])/dz**2  +
        (Psi2[1:-1, 2:  ] - 2*Psi2[1:-1, 1:-1] + Psi2[1:-1,  :-2])/dx**2)) + \
        z_sq*alpha*dt/(2*dz) * (Psi2[:-2, 1:-1] - Psi2[2:, 1:-1]) + \
        1j * (B0 + alpha*x_sq) * dt/(2*dx) * (Psi1[1:-1, :-2] - Psi1[1:-1, 2:])
    Psi1[:, :] = Psi_next

    # Solve matrix equation
    # DOESN'T WORK
    # Psi_next[:, :] = Psi1 + \
    #             -1j * dt * ((B0 + alpha*z_range)*Psi1 - alpha*Psi2)
    # Psi2[:, :] = Psi2 + \
    #             1j * dt * ((B0 + alpha*z_range)*Psi2 + alpha*Psi1)
    # Psi1[:, :] = Psi_next


    if k % 50 == 0:
        P = Psi1 + Psi2
        im.set_data(np.sqrt(P.real**2 + P.imag**2))
        # im.autoscale()
        plt.draw()
        plt.pause(.01)

        if k % 100 == 0:
            P_mag = np.sum(P.real**2 + P.imag**2)
            print('Psi magnitude: ', P_mag)
