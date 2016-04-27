
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
dt = .01

x0, x1 = -5, 5
z0, z1 = -5, 5
T = 10

B0 = .1
alpha = 1

Nx = round(1 + (x1 - x0) / dx)
Nz = round(1 + (z1 - z0) / dz)
Nt = round(1 + T / dt)

x_range = np.linspace(x0, x1, Nx)
z_range = np.linspace(z0, z1, Nz)

Psi1 = np.zeros((Nz, Nx), dtype=complex)
Psi2 = np.zeros((Nz, Nx), dtype=complex)

for i, xi in enumerate(x_range):
    for j, zj in enumerate(z_range):
        Psi1[j, i] = gaussian(xi, zj, 0, 2, .5, 5)
        Psi2[j, i] = Psi1[j, i]

plt.ion()
im = plt.imshow(Psi1.real, extent=[x0, x1, z0, z1])
cb = plt.colorbar(im)
for k in range(Nt):

    # Directly solve http://mathurl.com/zwzt59e.png
    Psi1[1:-1, 1:-1] = Psi1[1:-1, 1:-1] - alpha*dt/(2*dz) * \
                        (Psi1[:-2, 1:-1] - Psi1[2:, 1:-1]) #+ \
                    -1j * dt/(2*m) * (
                    (Psi1[:-2, 1:-1] - 2*Psi1[1:-1, 1:-1] + Psi1[2:, 1:-1])/dz**2 +
                    (Psi1[1:-1, :-2] - 2*Psi1[1:-1, 1:-1] + Psi1[1:-1, 2:])/dx**2)

    Psi2[1:-1, 1:-1] = Psi2[1:-1, 1:-1] - alpha*dt/(2*dz) * \
                        (Psi2[2:, 1:-1] - Psi2[:-2, 1:-1])

    if k % 10 == 0:
        im.set_data(Psi1.real)
        # im.autoscale()
        plt.draw()
        plt.pause(.01)
