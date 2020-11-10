import numpy as np
import scipy as sc
from scipy.sparse import csc_matrix


def Tridiag(d,N):
# ~ Matriz con diagonal d=[dsub,dmid,dsub] y dimensión N
    diagSub = np.diag(np.repeat(d[0],N-1),-1)
    diagMid = np.diag(np.repeat(d[1],N),0)
    diagSup = np.diag(np.repeat(d[2],N-1),1)
    return diagSub + diagMid + diagSup


def Mesh(Xlim, N, opt):
	# ~ Genera una malla uniforme de Xlim[0] a Xlim[1], con N puntos en el interior.
	# ~ la variable 'opt' indica si queremos el intervalo abierto o el cerrado.
    x = np.linspace(Xlim[0],Xlim[1],N+2)
    return x[1:-1] if ( opt == 'open' ) else x


def Solve(A,b):
    if not(isinstance(A, sc.sparse.csc.csc_matrix)):
        print("Advertencia: la matriz es mayor a 1000 y no es rala, se recomienda convertirla mediante csc_matrix")
        A = csc_matrix(A)
        return sc.sparse.linalg.spsolve(A,b)
    else:
        return sc.sparse.linalg.spsolve(A,b)


# Agustin Arias
def MatrizAInvertir_Implicito(tamaño, paso):
    # tamaño es el tamaño de la matriz, paso es h
    A = Tridiag([1, -2, 1], tamaño)
    Identidad = sc.sparse.identity(tamaño)  # necesario para poder aplicar kron

    matAInv = sc.sparse.kron(A, Identidad) + sc.sparse.kron(Identidad, A)
    matAInv = matAInv/(paso**2)

    return matAInv.toarray()


# Tilman Goebel
def MatrizAInvertir_Implicito_Rectangulo(tamañoX, tamañoY, pasoX, pasoY, dt):
    # tamañoX es la cantidad de filas, tamañoY la cantidad de columnas y pasoX y pasoY son hx y hy
    AX = Tridiag([1, -2, 1], tamañoX)
    AY = Tridiag([1, -2, 1], tamañoY)
    IdentidadX = sc.sparse.identity(tamañoX)
    IdentidadY = sc.sparse.identity(tamañoY)

    matAInv = sc.sparse.kron(AX, IdentidadY)/(pasoX**2) + sc.sparse.kron(IdentidadX, AY)/(pasoY**2)
    matAInv = dt * matAInv

    return matAInv

def MatricesCBPer2D( Nx,Ny ):
    Dx2 = Tridiag([1,-2,1],Nx)
    Dx2[0,-1] = 1 #condiciones periódicas
    Dx2[-1,0] = 1
    Dy2 = Tridiag([1,-2,1],Ny)
    Dy2[0,-1] = 1 #condiciones periódicas
    Dy2[-1,0] = 1
    return Dx2,Dy2
