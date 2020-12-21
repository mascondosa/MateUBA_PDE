import minifemlib
from minifemlib import Elements
import triangulation
from triangulation import Triangulation
import dmsh
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import scipy.linalg
from matplotlib import rcParams
from matplotlib import animation
import matplotlib.cm as cm



def condIniciales(n):
    if (n == 1):
        def g1(x,y):
            return(x<y)
        return g1
    elif (n == 2):
        def g2(x,y):
            return(x<0)
        return g2
    elif (n == 3):
        def g3(x,y):
            return(x<(3/4))*(x>(1/4))
        return g3
    elif (n == 4):
        def g4(x,y):
            return((x^2)+(y^2)<(1/4))
        return g4
    else:
        def g5(x,y):
            return((x^2)+(y^2)>(1/3))*((x^2)+(y^2)<(2/3))
        return g5
    
#Terminos de acople:

def F(u,v):
    return(0.1*np.ones(len(u))-u+(u**2)*v)

def G(u,v):
    return(1*np.ones(len(u))-(u**2)*v)

#StiffnessLaplacian de Martin retocado
def StiffnessLaplacian2(T,Egeom,order):
    # Matriz de rigidez del laplaciano.
    
    # Reservamos espacio
    n_nodes = len(T.points)
    n_elem = len(T.simplices)
    A = np.zeros([n_nodes,n_nodes])
    B = np.zeros([n_nodes,n_nodes])
    
    # Construimos bases de Lagrange y nodos de cuadratura
    phi, gradphi, Xnodes, quadw = Elements(Egeom,order)
    
    # Pre-calcular matriz local: int_T0 gradphi_i gradphi_j dx
    S = np.zeros([3,3])
    R = np.zeros([3,3])
    for i in range(3):
        for j in range(3):
            S[i,j] = np.sum(np.sum(gradphi(i,Xnodes)*gradphi(j,Xnodes),1)*quadw)
            R[i,j] = np.sum(np.array(phi(i,Xnodes)*phi(j,Xnodes))*quadw)
    
    # Matriz global, recorriendo los elementos
    for i in range(n_elem):
        
        # Índices de los vértices del triángulo i-ésimo (T_i)
        vertex_index = T.simplices[i]
        
        # Contribución a la matriz de rigidez
        A[np.ix_(vertex_index,vertex_index)] = A[np.ix_(vertex_index,vertex_index)] + R
        B[np.ix_(vertex_index,vertex_index)] = B[np.ix_(vertex_index,vertex_index)] + S
    
    return A, B


def matrizTuring(T,Egeom,order,u0,tiempo,dt,d,gamma,f,g):
    n_nodes = len(T.points)
    n_elem = len(T.simplices)
    phi, gradphi, Xnodes, quadw = Elements(Egeom,order)
    A, B = StiffnessLaplacian2(T,Egeom,order)
    t=np.arange(0,dt+tiempo,dt)
    Lt=len(t)
    u=np.zeros((n_nodes,Lt))
    v=np.zeros((n_nodes,Lt))
    for d in range(0,n_nodes):
        ci=condIniciales(u0)
        u[d,0]=ci(T.points[d,0],T.points[d,1]);
        v[d,0]=1-u[d,0];
    
    #Ciclo temporal

    M=scipy.linalg.block_diag(A+dt*B,A+dt*d*B)
    vector=np.zeros(2*n_nodes)
    
    for l in range(0,Lt-1):
        vector[0:n_nodes]=np.dot(A,u[:,l])+dt*gamma*np.dot(A,f(u[:,l],v[:,l]))
        vector[n_nodes:2*n_nodes]=np.dot(A,v[:,l])+dt*gamma*np.dot(A,g(u[:,l],v[:,l]))
        aux=np.linalg.solve(M,vector)
        u[:,l+1]=aux[0:n_nodes]
        v[:,l+1]=aux[n_nodes:2*n_nodes]
    
    U=np.zeros((n_nodes,Lt))
    for l in range(0,Lt):
        p=sum(u[:,l])/n_nodes
        for q in range(0,n_nodes):
            U[q,l]=(u[q,l]>p)
  
    frames = [] 
    fig = plt.figure()
    for n in range(0,Lt):
        im=plt.tripcolor(T.points[:,0], T.points[:,1],T.simplices, U[:,n].flatten())
        frames.append([im])

    ani = animation.ArtistAnimation(fig, frames, interval=300, blit=True,repeat_delay=1000)
    # ani.save('movie.mp4')
    plt.show()


c = dmsh.Circle([0, 0], 1)
points, cells = dmsh.generate(c, 0.1)
T=Triangulation(points, cells)
matrizTuring(T,'triangular',1,1,1,0.0025,10,200,F,G)