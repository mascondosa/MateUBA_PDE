import MateUBA_PDE as pde
import matplotlib.pyplot as plt
import numpy as np
import imageio
import matplotlib
import scipy.sparse as sparse
import scipy.sparse.linalg as sps_linalg
from matplotlib import cm
from matplotlib import animation
import copy as c

#
#   Código para resolver el sistema no lineal de reaccion - difusion con un método implícito
#   y condiciones de borde periodicas
#
#   Autor: Federico Choque, 21 de Dic 2020.
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


# Parametros de la ecuacion
Du = 2e-5
Dv = 1e-5


# Parámetros para las iteraciones
hx = Lx / (Nx + 1)
hy = Ly / (Ny + 1)
deltat = 10
laplacianoModificado = pde.MatrizAInvertir_Implicito_RectanguloCB(Nx, Ny, hx, hy, deltat)
Au = sparse.csc_matrix(sparse.identity(np.shape(laplacianoModificado)[0]) - Du*laplacianoModificado)
Av = sparse.csc_matrix(sparse.identity(np.shape(laplacianoModificado)[0]) - Dv*laplacianoModificado)

Au_lu=sps_linalg.splu(Au)
Av_lu=sps_linalg.splu(Av)


def ReacDifImplicito( U,V ):
	
	UU = c.copy(U)
	
	b_u=deltat*(-U*(V**2)+F*(1-U))+U
	b_v=deltat*(UU*(V**2)-(F+k)*V)+V
	
	U=Au_lu.solve(np.reshape(b_u, np.size(b_u)))
	V=Av_lu.solve(np.reshape(b_v, np.size(b_v)))
  
	U=np.reshape(U,(Nx,Ny));
	V=np.reshape(V,(Nx,Ny));
	
	return U,V
	

##
# Iteraciones temporales y animación
#

def VerAnim ( iterFunc ):
    fig, axs = plt.subplots()
    imfr = axs.imshow(U, cmap=cm.coolwarm)   
    axs.set_title('Método implícito para Reaccion-Difusion')

    def init():
        imfr.set_data(U)
        return [imfr]

    # Función de animación que se llama en un loop
    def animate(i):
        global U,V

        # Actualizo el cálculo segun el metodo implicito
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

VerAnim( ReacDifImplicito )
### 
