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
	
