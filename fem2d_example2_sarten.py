import numpy as np
import matplotlib.pyplot as plt
import minifemlib as fem
import triangulation

# Evaluamos la geometría        
T = triangulation.sartenTriangulation(2,0.15)
boundary = fem.Boundary(T)

# Definimos un lado derecho
def rhs(x,y):    
	return np.exp(-(x**2+y**2))

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

fig, ax1 = plt.subplots(1, 1)
tpc = ax1.tripcolor(T.points[:,0], T.points[:,1],T.simplices, sol_num, shading='gouraud')
ax1.set_title('Solución numérica')

plt.show()
