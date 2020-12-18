import dmsh
import numpy as np
import matplotlib.pyplot as plt
import minifemlib as fem
from scipy.spatial import Delaunay
import triangulation

####Creamos la llave doble con dmsh 

#Cabeza
forma1 = dmsh.Polygon(
    [
        [0.0, 0.0],
        [1, 0.5],
        [1, 2.5],
        [-1, 2.5],
        [-1, 0.5]
    ]
)

forma2 = dmsh.Difference(dmsh.Circle([0.0, 0.3], 1.6), forma1)

#Unimos el mango
forma3 = dmsh.Union([forma2, dmsh.Rectangle(-0.6,+0.6,-9.1,+0.1)])

#Unimos la otra cabeza
forma4 = dmsh.Polygon(
    [
        [0.0, -9.0],
        [1, -9.5],
        [1, -11.5],
        [-1, -11.5],
        [-1, -9.5]
    ]
)

forma5 = dmsh.Difference(dmsh.Circle([0.0,-9.3],1.6), forma4)

forma6= dmsh.Union([forma5,forma3])

#Tomamos h=0.25
X, cells = dmsh.generate(forma6, 0.25)

#Gráfico de la triangulación
print('Gráfico de la triangulación')
dmsh.helpers.show(X, cells,forma6)

####Ejemplo con la fuente de calor cerca de cada cabeza de la llave (ver rhs(x,y))

# Evaluamos la geometría        
T = triangulation.Triangulation(X,cells)
boundary = fem.Boundary(T)

# Definimos un lado derecho
def rhs(x,y):  
	return np.exp(-0.1*(x**2+(y+8.9)**2)) + np.exp(-0.1*(x**2+(y+0.1)**2))

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

plt.xlim([-5,5])
plt.ylim([-15,5])
plt.show()