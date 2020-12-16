import numpy as np
import matplotlib.pyplot as plt
import minifemlib as fem

# Evaluamos la geometría        
T = fem.rect_mesh([0,1],[0,1], 41, 41)
boundary = fem.Boundary(T)

# Definimos una solución exacta y un lado derecho
def exact(x,y):    
	return x*y + x**2 * y**2 - x*y**2 - x**2*y

def rhs(x,y):    
	return -2*y**2 + 2*y - 2*x**2 + 2*x

# Construimos matrices de rigidez y vector de cargas
order = 1
A = fem.StiffnessLaplacian(T,'triangular', order)
F = fem.LoadVector(rhs,T,'triangular', order)

# Agregamos condiciones de borde Dirichlet homogeneas como ecuaciones
for i in boundary:
    A[i,:] = np.zeros(A.shape[1])
    A[i,i] = 1
    F[i] = 0

# Resolvemos el problema lineal
sol_num = np.linalg.solve(A, F)

fig, (ax1, ax2) = plt.subplots(1, 2)
tpc = ax1.tripcolor(T.points[:,0], T.points[:,1],T.simplices, sol_num)
ax1.set_title('Solución numérica')

# Evaluamos solución exacta
sol_exact = exact(T.points[:,0],T.points[:,1])

tpc = ax2.tripcolor(T.points[:,0], T.points[:,1],T.simplices, sol_exact)
ax2.set_title('Solución exacta')
plt.show()
