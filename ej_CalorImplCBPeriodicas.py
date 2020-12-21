import MateUBA_PDE as pde
import matplotlib.pyplot as plt
import numpy as np
import imageio
import matplotlib
import scipy.sparse as sparse
import scipy.sparse.linalg as sps_linalg
from matplotlib import cm
from matplotlib import animation


#
#   Código para resolver la ecuación del calor con un método implícito
#   y condiciones de borde periódicas.
#
#   Autores: Federico Choque. 21 de Dic 2020.
#


# Leemos las condiciones iniciales de un archivo
im = imageio.imread('MateUBA_PDE.png')
F = im[:,:,0]
F = -(F - 255)/255.0

# Dimensiones del problema
Nx = np.shape(F)[0]
Ny = np.shape(F)[1]
Lx = Nx / 100
Ly = Ny / 100
sizeF = np.size(F)

# Grillas espaciales: queremos solo unos de los bordes (Condiciones periódicas)
x = pde.Mesh([0,Lx], Nx, 'closed')[1:]
y = pde.Mesh([0,Ly], Ny, 'closed')[1:]
X, Y = np.meshgrid(y,x)

# Parámetros para las iteraciones
hx = Lx / (Nx + 1)
hy = Ly / (Ny + 1)
deltat = 0.0005
Tf = 0.5
Nt = int(Tf / deltat) + 1
laplacianoModificado = pde.MatrizAInvertir_Implicito_RectanguloCB(Nx, Ny, hx, hy, deltat)
B = sparse.csc_matrix(sparse.identity(np.shape(laplacianoModificado)[0]) - laplacianoModificado)
B=sps_linalg.splu(B)  ###Usamos descomposicion LU para que no sea tan lento

def CalorImplicitoCBPeriodicas2D( F ):
    F = B.solve(np.reshape(F, sizeF))
    return np.reshape(F, (Nx, Ny))


#
# Iteraciones temporales y animación
#


def VerAnim ( iterFunc ):
    fig, axs = plt.subplots()
    imfr = axs.imshow(F, cmap=cm.coolwarm)   
    axs.set_title('Método implícito con condiciones de borde para la ecuación del calor')

    def init():
        imfr.set_data(F)
        return [imfr]

    # Función de animación que se llama en un loop
    def animate(i):
        global F

        # Actualizo el cálculo según el método implícito

        F = iterFunc( F )

        # Actualizo el título para mostrar el tiempo
        axs.set_title('Animacion a tiempo t=' + '{:.5}'.format(i*deltat) )

        # Actualizo el gráfico
        imfr.set_array(F)

        return [imfr]

    # Loop para llamar a la animación
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=Nt, interval=10, blit=False)

    # Mostrar animación
    plt.show()


# Mostramos la animación en pantalla
VerAnim( CalorImplicitoCBPeriodicas2D )
###
