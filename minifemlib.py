import numpy as np
from scipy.spatial import Delaunay

def Elements( Egeom, order ):
    # Devuelve bases de Lagrange y cuadraturas en el elemento de referencia

    if ( Egeom == 'triangular' and order==1 ):
        def phi(j,Xnodes):
            if (j==0): return 1-Xnodes[:,0]-Xnodes[:,1]
            elif (j==1): return Xnodes[:,0]
            else: return Xnodes[:,1]            
        def gradphi(j,Xnodes):
            if (j==0): return np.ones(np.shape(Xnodes))*np.array([-1,-1])
            elif (j==1): return np.ones(np.shape(Xnodes))*np.array([1,0])
            else: return np.ones(np.shape(Xnodes))*np.array([0,1])
        Xnodes = np.array([[0.5,0],[0,0.5],[0.5,0.5]])
        quadw = np.array([1/6,1/6,1/6])
    
    return phi, gradphi, Xnodes, quadw

# Geometría de ejemplo: rectángulo. Devuelve triangulación de Delaunay.
def rect_mesh(xlim,ylim,I,J):
    x = np.linspace(xlim[0],xlim[1],I)
    y = np.linspace(ylim[0],ylim[1],J)
    X,Y = np.meshgrid(x,y)
    P = np.array([X.flatten(),Y.flatten()]).T
    T = Delaunay(P)
    return T


# Función que encuentra el borde de una triangulación
def Boundary(T):
    boundary = set()
    for i in range(len(T.neighbors)):
        for k in range(3):
            if (T.neighbors[i][k] == -1):
                nk1,nk2 = (k+1)%3, (k+2)%3 
                boundary.add(T.simplices[i][nk1])
                boundary.add(T.simplices[i][nk2])
    return boundary


def StiffnessLaplacian(T,Egeom,order):
    # Matriz de rigidez del laplaciano.
    
    # Reservamos espacio
    n_nodes = len(T.points)
    n_elem = len(T.simplices)
    A = np.zeros([n_nodes,n_nodes])
    
    # Construimos bases de Lagrange y nodos de cuadratura
    phi, gradphi, Xnodes, quadw = Elements(Egeom,order)
    
    # Pre-calcular matriz local: int_T0 gradphi_i gradphi_j dx
    S = np.zeros([3,3])
    for i in range(3):
        for j in range(3):
            S[i,j] = np.sum(np.sum(gradphi(i,Xnodes)*gradphi(j,Xnodes),1)*quadw)
        
    # Matriz global, recorriendo los elementos
    for i in range(n_elem):
        # Índices de los vértices del triángulo i-ésimo (T_i)
        vertex_index = T.simplices[i]
        
        # Contribución a la matriz de rigidez
        A[np.ix_(vertex_index,vertex_index)] = A[np.ix_(vertex_index,vertex_index)] + S
    
    return A
    
def LoadVector(rhs, T, Egeom, order):
    # Vector del lado derecho \int_\Omega f v
    
    # Reservamos espacio    
    n_nodes = len(T.points)
    n_elem = len(T.simplices)
    F = np.zeros(n_nodes)
    Fint = np.zeros(3)
    
    # Construimos bases de Lagrange y nodos de cuadratura
    phi, gradphi, Xnodes, quadw = Elements(Egeom,order)    
    
    for i in range(n_elem):
        # Índices de los vértices del triángulo i-ésimo (T_i)
        vertex_index = T.simplices[i]
        
        # Vertices del triángulo T_i
        vertices = [ T.points[T.simplices[i][j]] for j in range(3) ]
        
        # Transformación afin del triángulo de referencia al T_i
        B = np.array([vertices[1] - vertices[0], vertices[2] - vertices[0]])
        detB = abs(np.linalg.det(B))
        
        # Nodos de cuadratura dentro de T_i
        Xtriangle = np.array([np.matmul(B,Xnodes[j]) + vertices[0] for j in range(3)])
        
        # Evaluamos lado derecho * phi_j en los nodos e integramos
        for j in range(3):
            integrand = phi(j,Xnodes) * rhs(Xtriangle[:,0],Xtriangle[:,1])
            Fint[j] = np.sum( integrand*quadw ) * detB
        
        # Sumamos contribución al lado derecho
        F[vertex_index] = F[vertex_index] + Fint    
    
    return F
