---
layout: default
title: Home
nav_order: 1
usemathjax: true
description: "Códigos elementales para la resolución de Ecuaciones en Derivadas Parciales, escritos con fines educativos, como parte de un curso de Análisis Numérico de la Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires."
permalink: /
---

# Métodos de Diferencias Finitas y Elementos Finitos
{: .fs-9 }

$$ \left\lbrace 
\begin{array}{cc} 
\Delta u = f & x\in\Omega \\
u = 0 & x\in\partial\Omega
\end{array}
\right. $$

Códigos elementales para la resolución de Ecuaciones en Derivadas Parciales, escritos con fines educativos, como parte de un curso de Análisis Numérico de la Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires.
{: .fs-6 .fw-300 }

[Comenzar](#comenzar){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } 
[Ver en GitHub](https://github.com/pmarsceill/just-the-docs){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Comenzar

Para contribuir código al proyecto, es necesario tener una cuenta de GitHub.

Luego, ir a la página del proyecto y hacer click en "Fork". Entonces
tendremos una copia personal del repositorio bajo nuestro nombre en el servidor
de Github. Para descargarlo, el comando que necesitamos es 

{% highlight console %}
git clone https://github.com/your.github.username/MateUBA_PDE.git
{% endhighlight %}

(modificando your.github.username por el nombre de usuario que hayamos registrado).

Después de trabajar localmente con el código, cuando querramos subir una copia al servidor, hacer

{% highlight console %}
git add file1.py file2.py
{% endhighlight %}

donde file1.py file2.py son los archivos que hemos modificado o añadido. Alternativamente,
se puede hacer

{% highlight console %}
git add --all
{% endhighlight %}
para añadir todos los archivos del directorio de trabajo (usar esto con cuidado).

Este comando (add) añade los archivos a la lista de archivos del repositorio. Para prepararnos para subir
la contribución, hacer

{% highlight console %}
git commit -m "mensaje"
{% endhighlight %}
donde "mensaje" incluye un texto con la descripción de los cambios. Finalmente, con

{% highlight console %}
git push
{% endhighlight %}
se hace la transferencia de datos hacia el servidor de Github.

Ahora bien, si queremos que nuestros cambios sean incorporados a la versión oficial del proyecto, hay que ir a la
página de Github del mismo y pedir un "pull request". El administrador así podrá revisar nuestros cambios
y decidir si los acepta.
