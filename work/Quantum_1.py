
import numpy as np
from matplotlib import pyplot as plt

m = .01

dx = .1
dz = .1
dt = .02

# Non-physical axis lengths, see below
x0, x1 = -10, 10
z0, z1 = -10, 10
T = 1000

# To use or not use X diffusion term
# If false, it will only move in 1D (though it will diffuse in 2d)
# and produce a nicer looking, physically consistent result :)
FULL_EQ = True

alpha = .2  # Z factor
B0 = .2     # X factor
m = 40      # Diffusion coefficient (~1/m)

Nx = round(1 + (x1 - x0) / dx)
Nz = round(1 + (z1 - z0) / dz)
Nt = round(1 + T / dt)

x_range = np.linspace(x0, x1, Nx)
x_sq = 2*np.meshgrid(np.zeros(Nx-2), x_range[1:-1])[1] / (x1-x0)
z_range = np.linspace(z0, z1, Nz)
z_sq = 2*np.meshgrid(z_range[1:-1], np.zeros(Nz-2))[0] / (z1-z0)

# These axis lengths are not related to the above ones
# (though they should be). These modify the influence of
# the alpha term in the X and Z directions.
# It is currently set up to have maximum influence at x,z=0
# and decay to 0 at the boundaries.
Ax = np.linspace(0, .5, (Nx-1)//2)
Az = np.linspace(0, 1, (Nz-1)//2)
x_sq, z_sq = np.meshgrid(np.hstack((Ax, Ax[-2::-1])), np.hstack((Az, Az[-2::-1])))
# x_sq, z_sq = np.meshgrid(Ax, Az)

Psi1 = np.zeros((Nz, Nx), dtype=complex)
Psi2 = np.zeros((Nz, Nx), dtype=complex)
Psi_next = np.zeros((Nz, Nx), dtype=complex)

for i, xi in enumerate(x_range):
    for j, zj in enumerate(z_range):
        p = np.exp(-(xi**2 + zj**2)*2)
        Psi1[j, i] = p
        Psi2[j, i] = p

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
        1j * (B0 + alpha*x_sq) * dt/(2*dx) * (Psi2[1:-1, :-2] - Psi2[1:-1, 2:]) * FULL_EQ

    Psi2[1:-1, 1:-1] = Psi2[1:-1, 1:-1] + 1j/(2*m) * (dt * (
        (Psi2[2:  , 1:-1] - 2*Psi2[1:-1, 1:-1] + Psi2[ :-2, 1:-1])/dz**2  +
        (Psi2[1:-1, 2:  ] - 2*Psi2[1:-1, 1:-1] + Psi2[1:-1,  :-2])/dx**2)) + \
        z_sq*alpha*dt/(2*dz) * (Psi2[:-2, 1:-1] - Psi2[2:, 1:-1]) + \
        1j * (B0 + alpha*x_sq) * dt/(2*dx) * (Psi1[1:-1, :-2] - Psi1[1:-1, 2:]) * FULL_EQ
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
