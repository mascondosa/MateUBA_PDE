import MateUBA_PDE as pde
import matplotlib.pyplot as plt
import numpy as np
import imageio
from matplotlib import cm
from matplotlib import animation

#
#   Código para resolver la ecuación del calor con un método explícito
#   y condiciones de borde periodicas
#
#   Autores: Sol Acuña y Maria Galante, 10 de Nov 2020.
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
x = pde.Mesh([0,Lx], Nx, 'close')[1:]
y = pde.Mesh([0,Ly], Ny, 'close')[1:]
X, Y = np.meshgrid(y,x)

# Parámetros para las iteraciones
hx = Lx / (Nx + 1)
hy = Ly / (Ny + 1)
deltat = min([hx,hy])**2 / 8 # condición de estabilidad para el método explícito
Tf = 0.005
Nt = int(Tf / deltat) + 1

def CalorExplCBPeridicas2D( F,alpha ):
     return alpha * deltat * ( np.matmul(Dx2,F)/hx**2 + np.matmul(F, Dy2)/hy**2 ) + F

#
# Iteraciones temporales y animación
#

def VerAnim ( iterFunc ):
    fig, axs = plt.subplots()
    imfr = axs.imshow(F, cmap=cm.coolwarm)   
    axs.set_title('Método explícito para la ecuación del calor')
        
    def init():
        imfr.set_data(F)
        return [imfr]

    # Función de animación que se llama en un loop
    def animate(i):
        global F
        
        # Actualizo el cálculo según el método explícito
        F = iterFunc( F,1 )
        
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

Dx2,Dy2 = pde.MatricesCBPer2D( Nx,Ny )
VerAnim( CalorExplCBPeridicas2D )

# ~ # Guardar el video a un archivo
# ~ matplotlib.use("Agg")
# ~ Writer = animation.writers['ffmpeg']
# ~ writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800)
# ~ anim.save('im.mp4', writer=writer)



