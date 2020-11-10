import MateUBA_PDE as pde
import matplotlib.pyplot as plt
import numpy as np
import imageio
from matplotlib import cm
from matplotlib import animation
import copy as c

#
#   Codigo para resolver la ecuacion de reaccion difusion
#   y condiciones de borde periodicas.
#
#   Autores: Sol Acuña y Maria Galante, 10 de Nov 2020.
#

# Dimensiones del problema
Nx = 256
Ny = 256
Lx = Nx / 100
Ly = Ny / 100

#Condiciones iniciales
U = np.ones([Nx,Ny])
V = np.zeros([Nx,Ny])
centroX = Nx//2
centroY = Ny//2
U[centroX-10:centroX+10,centroY-10:centroY+10] = 1/2
V[centroX-10:centroX+10,centroY-10:centroY+10] = 1/4

#Perturbo estas condiciones con un ruido random del +/- 1% para romper la simetría
U = U + U * 0.01* (np.random.rand(np.shape(U)[0],np.shape(U)[1])*2-1)
V = V + V * 0.01* (np.random.rand(np.shape(V)[0],np.shape(V)[1])*2-1)

# Parámetros para las iteraciones
hx = Lx / (Nx + 1)
hy = Ly / (Ny + 1)
deltat = 1

# Parametros de la ecuacion
Du = 2e-5
Dv = 1e-5

Dx2,Dy2 = pde.MatricesCBPer2D( Nx,Ny )

def CalorExplCBPeridicas2D( F,alpha ):
     return alpha * deltat * ( np.matmul(Dx2,F)/hx**2 + np.matmul(F, Dy2)/hy**2 ) + F

def ReaccionDifusionSistemaNoLineal( U,V ):
    UU = c.copy(U)
    U = CalorExplCBPeridicas2D(U,Du) - deltat* U*(V**2) + deltat * F*(1-U) 
    V = CalorExplCBPeridicas2D(V,Dv) + deltat* UU*(V**2) - deltat * V*(F+k) 
    return U,V

##
# Iteraciones temporales y animación
#

def VerAnim ( iterFunc ):
    fig, axs = plt.subplots()
    imfr = axs.imshow(U, cmap=cm.coolwarm)   
    axs.set_title('Método explícito para Reaccion-Difusion')
        
    def init():
        imfr.set_data(U)
        return [imfr]

    # Función de animación que se llama en un loop
    def animate(i):
        global U,V
        
        # Actualizo el cálculo según el método explícito
        U,V = iterFunc( U,V )
        
        # Actualizo el título para mostrar el tiempo}
        axs.set_title('Animacion a tiempo t=' + '{:}'.format(i*deltat) )
        
        # Actualizo el gráfico
        imfr.set_array(U)
        
        return [imfr]

    # Loop para llamar a la animación
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=int(1e3), interval=1, blit=False)

    # Mostrar animación
    plt.show()

###

#### Test 1 : Epsilon del paper
k = 0.05
F = 0.01

#### Test 2 : Eta
# k = 0.061
# F = 0.028

#### Test 3 : Gamma
# k = 0.056
# F = 0.025

#### Test 4 : Kappa
# k = 0.063
# F = 0.04

#### Test 5 : 
# k = 0.068
# F = 0.04

VerAnim( ReaccionDifusionSistemaNoLineal )
###