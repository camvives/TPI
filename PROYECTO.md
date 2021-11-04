# FaceMask Detector
## Descripción del proyecto
En este proyecto se hará uso de la librería OpenCV para Python. OpenCV usa algoritmos de machine learning para buscar rostros dentro de una imagen. La forma de lograr esto es reconociendo cientos de pequeños patrones y características que deben coincidir durante el procesamiento de imágenes.
A partir de esto, el objetivo principal del programa es, dada una imagen, reconocer en primer lugar si existe un rostro humano dentro de ella, y si ese es el caso, detectar si la persona está usando cubrebocas. Teniendo en cuenta que un video es una serie ordenada de imágenes, es posible extender esta aplicación, y de esta forma poder lograr que el programa reconozca en videos a tiempo real si la persona que aparece en él está haciendo uso del cubrebocas o no. 
Adicionalmente, el programa guardará en una base de datos  los estados ‘con máscara’ o ‘sin máscara’ detectados en tiempo real, junto con la fecha y hora de ocurrencia. Ésto permitirá realizar estadísticas diarias, semanales, y mensuales, que serán mostradas a través de gráficas a modo de reportes.

## Bosquejo de Arquitectura

![](Md_img\arquitectura.png "Arquitectura")
## Modelo funcional

![](Md_img\modelo_funcional.png "Funcionamiento")
## Requerimientos

### Funcionales

- El sistema debe extraer una imagen (frame) a partir de un video a tiempo real, en el cual una persona esté situada de frente a la cámara. 
- El sistema debe detectar un rostro humano dentro de una imagen extraída e identificarla como área de interés (ROI).
- El sistema debe dibujar un recuadro en la zona de interés (ROI) del video, coloreado según la clasificación de la imagen.
- El sistema debe almacenar en una base de datos el registro de la fecha y hora, y la clasificación provenientes de la imagen analizada.
- El sistema debe permitir al cliente consultar los datos históricos a partir de estadísticas diarias, semanales y mensuales del sistema.

### No Funcionales
- El sistema debe ejecutarse desde un único archivo .py llamado app.py. (Portability)
- El sistema debe diseñarse con la arquitectura en 3 capas. (Maintainability)
- El sistema debe utilizar control de versiones mediante GIT. (Maintainability)
- El sistema debe estar programado en Python 3.8 o superior. (Maintainability)
- El sistema debe detectar el uso de la máscara el 90% de las veces. (Reliability)
- El sistema debe funcionar en un equipo hogareño estándar. (Performance)
- El sistema deberá cumplir con un tiempo de respuesta menor a 1 segundo. (Performance)
- El sistema debe utilizar una base de datos SQL o NoSQL (Flexibility)

## Stack Tecnológico
### Capa de Datos
En la capa de datos se utilizó SQLite. SQLite es una herramienta de software libre, que permite almacenar información en distintos dispositivos  de una forma sencilla, eficaz, potente y rápida. La elección de esta tecnología tiene que ver con la sencillez de los datos a registrar y con la velocidad de escritura que requieren los mismos. Además, al no manejar ningún dato sensible dentro de la aplicación,  no se requiere un mayor nivel de seguridad que el que provee este motor de base de datos.

### Capa de Negocio

En la capa de negocios se emplea el lenguaje Python con las siguientes librerías:
- MatPlotLib: Es una librería especializada en la creación de gráficos en dos dimensiones. Permite crear y personalizar los tipos de gráficos más comunes, entre ellos histogramas, diagramas de barra, diagramas de líneas, etc.
- Tensor Flow: Es una librería de código abierto para cálculo numérico, usando como forma de programación grafos de flujo de datos. Con esta librería somos capaces, entre otras operaciones, de construir y entrenar redes neuronales para detectar correlaciones y descifrar patrones, análogos al aprendizaje y razonamiento usados por los humanos.
- Numpy: Es una librería especializada en el cálculo numérico y el análisis de datos, especialmente para un gran volumen de datos. Incorpora una nueva clase de objetos llamados arrays que permite representar colecciones de datos de un mismo tipo en varias dimensiones, y funciones muy eficientes para su manipulación.
- OpenCV: Es una biblioteca libre de visión artificial originalmente desarrollada por Intel. OpenCV significa Open Computer Vision (Visión Artificial Abierta). Entre otras cosas, permite la detección de movimiento, reconocimiento de objetos, reconstrucción 3D a partir de imágenes, reconocimiento facial, etc.

Es importante aclarar que para poder entrenar al modelo que detecta si una persona tiene máscara o no, se utilizó la herramienta Teacheble Machine de Google (https://teachablemachine.withgoogle.com/).
Para esto, se ingresó en la aplicación un Dataset que contenía aproximadamente 1400 imágenes subdivididas en dos categorías: rostros con máscara y rostros sin máscara. De esta forma, el software de Google nos dió como resultado un conjunto de archivos .py que contienen los algoritmos que clasifican una imagen dada, según las características de la misma. 

### Capa de Presentación
Para la presentación se hizo uso de la biblioteca gráfica TKinter, utilizando el paradigma orientado a objetos que permite la misma. El uso de esta biblioteca tiene que ver con la sencillez de la interfaz que provee. De esta manera, se puede integrar correctamente a OpenCV sin consumir demasiados recursos gráficos, altamente necesarios en el caso de esta aplicación, ya que muestra videos a tiempo real. 
