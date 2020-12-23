---
title: Elementos Finitos
layout: page
usemathjax: true
---

## Elementos Finitos

### Malladores

Lo primero en un código de Elementos Finitos es definir una geometría discreta (una malla).
El código puede hacer lo siguiente: 
- Definir una nube de puntos y mallar mediante scipy.spatial.Delaunay
- Definir una geometría y construir una malla mediante dmesh.
- Encontrar los nodos de borde de una triangulación.

### Interpolación y cuadratura

Tenemos definidas las siguientes bases de Lagrange:
* En un triángulo
    * Elementos Lineales
* En un rectángulo
    * Por ahora nada

junto con las cuadraturas:
- Exactas para $$\mathcal{P}_2$$ en un triángulo

### Formas débiles

El código calcula integrales locales de la forma:

$$ \int_T \nabla \phi_i \nabla \phi_j dx $$

y luego las ensambla en una matriz global.

### Condiciones de borde

El código implementa condiciones de borde de Dirichlet homogéneas,
marcando los nodos de borde y añadiendo la ecuación a la matriz global.

### Álgebra Lineal

Finalmente se resuelve el problema lineal mediante numpy.linalg.solve

