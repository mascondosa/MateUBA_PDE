---
layout: default
---

## Introducción

### Instalación

Se puede bajar el zip desde aquí.

### Cómo contribuir

Para contribuir código al proyecto, es necesario tener una cuenta de GitHub.

Luego, ir a la página del proyecto y hacer click en "fork repository". Entonces
tendremos una copia personal del repositorio bajo nuestro nombre en el servidor
de Github. Para descargarlo, hacer 

{% highlight ruby %}
git clone
{% endhighlight %}

Después de trabajar localmente con el código, y queremos subir una copia al servidor, hacer

{% highlight ruby %}
git add file1.py file2.py
{% endhighlight %}

donde file1.py file2.py son los archivos que hemos modificado o añadido. Alternativamente,
se puede hacer

{% highlight ruby %}
git add --all
{% endhighlight %}

Este comando añade los archivos a la lista de archivos del repositorio. Para prepararnos para subir
la contribución, hacer

{% highlight ruby %}
git commit -m "mensaje"
{% endhighlight %}

donde "mensaje" incluye un texto con la descripción de los cambios. Finalmente, con

{% highlight ruby %}
git push
{% endhighlight %}

se hace la transferencia de datos.

Si queremos que nuestros cambios sean incorporados a la versión oficial del proyecto, hay que ir a la
página de Github del mismo y pedir un "pull request". El administrador así podrá revisar nuestros cambios
y decidir si los acepta.

## Diferencias Finitas

### Matrices de diferencias

### Iteraciones temporales

### Visualizar una animación


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
