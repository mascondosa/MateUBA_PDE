import numpy as np
import matplotlib.pyplot as plt
import minifemlib as fem

# Evaluamos la geometría        
T = fem.rect_mesh([0,1],[0,1],11,11)

boundary = fem.Boundary(T)

# Ploteamos la malla y el borde
plt.triplot(T.points[:,0], T.points[:,1], T.simplices)
plt.plot(T.points[:,0], T.points[:,1], 'o')
plt.plot(T.points[list(boundary),0], T.points[list(boundary),1], 'or')
plt.show()
