# Seguimiento de objetos con filtro de partículas

### **Rodrigo Quiroz Reyes** & **Christopher Luis Miranda Vanegas** & **Esteban Manrique de Lara Sirvent**

El seguimiento de objetos es una aplicación de _Deep Learning_, en la que el programa toma un conjunto inicial de detecciones de objetos y desarrolla una identificación única para cada una de las detecciones iniciales y luego rastrea los objetos detectados a medida que se mueven por los fotogramas de un video.

En otras palabras, el seguimiento de objetos es la tarea de identificar automáticamente objetos en un video e interpretarlos como un conjunto de trayectorias con alta precisión.

A menudo, hay una indicación alrededor del objeto que se está rastreando, por ejemplo, un cuadrado circundante que sigue al objeto y muestra al usuario dónde se encuentra el objeto en la pantalla (Meel, 2022)

![](/images/Aspose.Words.11243613-d597-4d66-a52d-133f55183816.002.jpeg)

_Figura 1. Ejemplo de filtro de partículas, sobre un cuadro de un video._

# Antecedentes

La visión computacional o por computador, es un campo de la inteligencia artificial (IA) el cual permite que las computadoras y los sistemas obtengan información significativa a través de imágenes digitales, videos y otras entradas visuales, y tomen medidas o hagan recomendaciones basadas en esa información. En otras palabras, la visión computacional tiene como objetivo brindar a las computadoras una comprensión visual del mundo y de aquí nacen poderosos algoritmos. Hoy en día, se usa machine learning (ML) y deep learning (DL), con el fin de reconocer (clasificar) los objetos que aparecen en imágenes digitales y videos. La visión computacional en general funciona siguiendo los siguientes tres pasos básicos (Dynatec, 2009):

1. **Adquirir una imagen:** las imágenes, incluso los conjuntos grandes, se pueden adquirir en tiempo real a través de videos, fotos o tecnología 3D para su análisis.
1. **Procesando la imagen:** los modelos de aprendizaje profundo automatizan gran parte de este proceso, y se entrenan al ser alimentados primero con miles de imágenes etiquetadas o identificadas previamente.
1. **Entendiendo la imagen:** el paso final es el paso interpretativo, donde se identifica o clasifica un objeto.

El seguimiento de objetos es una de las tareas más importantes en la visión artificial. Los rastreadores de objetos son una parte integral de muchas aplicaciones de visión computacional que procesan el flujo de video de las cámaras. Hoy en día existen diversos algoritmos y filtros, cada uno con diferentes usos y características, un ejemplo es el filtro de partículas.

En 1993, D. Salmond, A. Smith y N. Gordon propusieron el filtro bootstrap o filtro de partículas, con el fin de implementar filtros bayesianos recursivos mediante el método de Monte Carlo. Dicho filtro se compone de un conjunto de muestras (en este caso, las partículas) y pesos o valores, asociados a cada una de las partículas. Estas representan muestras del espacio de posibles estados del proceso, y los pesos simbolizan presencias dentro de una función de densidad de probabilidad (f.d.p). Dicha función es realizada sobre estados de estados futuros. Al filtro de partículas le siguen los siguientes cuatro pasos:

1. **Inicialización:** en esta etapa el filtro crea partículas al azar en un conjunto de puntos sobre el plano de la imagen.
1. **Actualización:** de acuerdo con la similitud del estado de partícula con el estado de referencia, se le pondrá un peso o valor a cada una de estas.
1. **Estimación:** a partir de los pesos o valores anteriores, se creará un nuevo conjunto de partículas que constituirá la estimación previa del estado en el siguiente instante de tiempo. En esta etapa, se usan métodos de remuestreo probabilísticos, considerando la probabilidad previa de cada partícula, buscando dar paso a las nuevas partículas donde la probabilidad sea mayor.
1. **Predicción:** con el nuevo conjunto de partículas para el nuevo instante momentáneo, se modifica el estado de cada una metiendo algún tipo de ruido aditivo que aporte variabilidad.

Al finalizar la última etapa, el resultado es el nuevo conjunto de partículas el cuál vuelven a pasar por la etapa de actualización hasta que se termine la secuencia de datos.

# Planteamiento

El planteamiento inicial, generado por los miembros del equipo, consistía de cuatro principales fases:

- Generación de las partículas a ser utilizadas y mostradas a lo largo de todo el proceso de seguimiento.
- Cálculo de delta/cambio de velocidad y posición (x,y) de dichas partículas, conforme el objeto se fueran moviendo. **(Iterativo por cada frame del video)**
- Aplicación de dichas diferencias de rapidez y colocación de las partículas en pantalla. **(Iterativo por cada frame del video)**
- Despliegue de las partículas con sus respectivos cambios y generación de video

“resultado” con el seguimiento completo del objeto.

Para el primer paso de este planteamiento, se buscaba una forma de generar las partículas. Por ende, se tenía pensado dibujar, en pantalla y sobre los frames de los vídeos, círculos de pequeño tamaño, con el objetivo de “simular” las partículas y su movimiento conforme se fueran movilizando a lo largo del video. La librería de Opencv (cv2) fue propuesta como la indicada para la generación de estos “círculos”.

En torno al cambio de velocidad y posición de las partículas previamente mencionadas, se buscaba qué conforme fueran avanzando los frames/cuadros del video, se generarán dos comportamientos principales: el primero de ellos en donde aquellas qué se ubiquen sobre píxeles o secciones del video con el color siendo buscado se mantengan o sufran muy poco cambio de aceleración/posición. La segunda de las tendencias buscadas estaba más orientada hacia el acercamiento de las partículas más alejadas a píxeles considerados como “objetivos de búsqueda”; para realizar ésto, se pensaba poder calcular una métrica, ya sea una especie de error o distancia entre lo deseado y lo actual, identificando con base en umbrales, a las partículas qué no se encuentren lo suficientemente cercanas a los objetos bajo seguimiento.

Consecuentemente, para la aplicación de los cambios de rapidez y colocación, se tenía la intención de modificar directamente cada una de las partículas modeladas en la primera fase de esta resolución. Para lograr esto, se planteó qué cada partícula se tendría qué producir como una lista o una clase, lo qué permitiría modificar de manera modular los atributos de velocidad y aceleración. Asimismo, estos cambios deberían verse reflejados con el paso de cada uno de los cuadros del video siendo analizado.

Finalmente, los cambios realizados a cada una de las partículas serían visualizados en cada uno de los frames, gracias a que éstas serían representadas con círculos pequeños generados por cv2. Al terminar el análisis de todos los cuadros del video, se generaría otro video “resultado”, en el cual se mostrarían los cambios de posición de las moléculas, y por ende, el seguimiento del color elegido al inicio del programa.

# Solución

A continuación se explica, paso a paso y de la manera más simplificada posible, las acciones y métodos utilizados para la solución del problema propuesto en este proyecto:

1. Se obtiene el nombre del video a ser analizado, mediante el uso de argumentos de consola. Se utiliza la librería _getopt_ para la obtención del nombre del video. Adicionalmente, el usuario podrá escoger el color (o dejar el predefinido) a ser seguido por las moléculas. Las funciones que realizan este primer paso son **myfunc() y colorPicker()**.
1. Se procede a obtener las dimensiones (largo y ancho) del video a ser analizado. Adicionalmente, se obtiene el número de cuadros de dicho video. Lo anterior, con el objetivo de poner un sleep entre cuadros del video, al momento de realizar los demás pasos del algoritmo. La función qué realiza este paso es **set_video_dimensions()**.
1. Se genera un arreglo de partículas. Cada una de ellas es un arreglo de 4 posiciones, qué contiene la posición de “x” y “y”, al igual que las velocidades en dichos ejes. Los valores iniciales son aleatorios. La función **initialize_particles()** es la encargada de este paso.
1. Se procede a aplicar un cambio de velocidad constante a las partículas. Lo anterior con el objetivo de que conforme vayan transcurriendo los frames, las partículas no permanezcan estáticas y sean lo suficientemente rápidas para moverse. El método responsable de este paso es **speed()**.
1. Después, las partículas deben ser contenidas dentro del espacio “visible” del video. En otras palabras, se requieren poner límites, usando las dimensiones previamente obtenidas del video, que eviten que las partículas salgan del video. Los límites son: **[0, ancho del video - 1]** y **[0, alto del video -1]**. Las funciones responsables de este paso son **xBoundaries()** y **yBoundaries()**.
1. Habiendo realizado los pasos anteriores, se procede a checar la posición y color sobre el cual se encuentran cada una de las partículas del sistema. Para esto, se obtienen los valores de los tres canales del color del pixel sobre donde se encuentre la partícula. Posteriormente, se compara con el color “objetivo” o a ser seguido por las mismas. Con ésto, se obtiene un valor que permite saber la “distancia” o similitud entre el color bajo la partícula y el color deseado. La función encargada de este paso del algoritmo es **particleColors()**.
1. Se aplica una “normalización” a aquellas partículas que se encuentren en los extremos del video. Lo anterior, con el objetivo de que al momento de calcular el cambio de dirección de las partículas, no se dirijan hacia los bordes del cuadro del video en turno. El método que realiza este paso es **getRelevantIndicators()**
1. Mediante los valores obtenidos en el Paso 6 y la normalización del paso 7, se puede generar un nuevo conjunto de partículas (usando probabilidad y un muestreo con base en dicha probabilidad). Se espera que las partículas resultantes estén más cercanas al color “objetivo”. Adicionalmente, se aplican los cambios de velocidad y posición pertinentes para la mejor de sus posiciones. Las dos funciones responsables de este segmento del algoritmo son **createParticlesSample()** y **applyParticleModifications()**.
1. Como último paso, se desplegará cada una de las partículas resultantes del Paso 8 en el frame siendo analizado durante esta iteración de la solución. Lo anterior es posible gracias a qué se tienen las coordenadas de las partículas, al igual que el método **cv2.circle()**. La función qué cumple con este último segmento del algoritmo es **displayFrame()**.

   10.El resultado final del proyecto se constituye de dos principales evidencias:

1. Una muestra, cuadro por cuadro, del cómo las partículas se van ajustando y moviendo éstas respecto al color u objeto siendo seguido.
1. Un video, con nombre **“output.mp4”**, que concatena cada uno de los frames del inciso a) y permite mostrar el ajuste y movimiento de las partículas en forma de video.

**\*\*NOTA**: Los pasos comprendidos entre el Paso 4 y el Paso 9 se realizan de manera cíclica por cada uno de los cuadros del vídeo previamente indicado por el usuario en el primer paso de la solución.

# Referencias

Moya, A. (2009). Estudio Del Filtro De Partículas Aplicado Al Seguimiento De Objetos

En Secuencias De Imágenes. Recuperado de: [https://e-archivo.uc3m.es/bitstream/handle/10016/11173/PFC%20Alvaro%20Rodr ](https://e-archivo.uc3m.es/bitstream/handle/10016/11173/PFC%20Alvaro%20Rodriguez.pdf;jsessionid=7BB01168C8D53A5B7D19ED3676EBB1ED?sequence=1)[iguez.pdf;jsessionid=7BB01168C8D53A5B7D19ED3676EBB1ED?sequence=1](https://e-archivo.uc3m.es/bitstream/handle/10016/11173/PFC%20Alvaro%20Rodriguez.pdf;jsessionid=7BB01168C8D53A5B7D19ED3676EBB1ED?sequence=1)

Meel, V. (2022). Object Tracking in Computer Vision (Complete Guide). Viso.ai.

Recueperado de: <https://viso.ai/deep-learning/object-tracking/>

IBM. (2022). What is Computer Vision?. IBM. Recuperado de:

<https://www.ibm.com/topics/computer-vision>

Dynatec. (2021). Computer Visión: la visión artificial y sus aplicaciones. Dynatec.

` `Recuperado de:

[https://dynatec.es/2021/07/24/computer-vision-la-vision-artificial-y-sus-aplicacion ](https://dynatec.es/2021/07/24/computer-vision-la-vision-artificial-y-sus-aplicaciones/)[es/](https://dynatec.es/2021/07/24/computer-vision-la-vision-artificial-y-sus-aplicaciones/)
