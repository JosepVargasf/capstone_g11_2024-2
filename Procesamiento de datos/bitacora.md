En primer lugar voy a correr un algoritmo de clusterizacion k-means. Esto basado en el paper que leí en donde k-means es el más utilizado para problemas relacionado al merketing

En segundo lugar la definición de comportamiento va a ser renta(que agrupa monto simulado, deuda y oferta consumo)

Tenemos dos cosas relevantes aqui, las caracteristicas y los comportamientos. Las caracteristicas se encuentran en el data frame de informacion de clientes
mientras que el comportamiento son las ventas y las simulaciones. La gran pregunta es, clusterizar por las caracteristicas solamente o por las caracteristicas y el comportamiento.

Dentro de las caracteristicas y comportamiento se selecionaran las siguientes variables para clusterizar
selected_columns = ['Genero', 'Categoria_Digital', 'Elasticidad_Precios', 'Propension', 'Probabilidad_No_Pago', 
                    'Edad', 'Renta', 'cantidad simulaciones', 'tasa de concresion']


'Categoria_Digital': Entre usuarios que son digitales o no es relevante si se les da un trato digital (mail) o no digital(ejecutivo)
'Elasticidad_Precios': Se vio en la visualizacion de datos que se separan en ciertos grupos segun su elasticidad
'Propension'[Después debe ser probabilidad de curse]: Indicada por el profesor guia
'Probabilidad_No_Pago': Indicada por el profesor guia
'Renta': Habla de un comportamiento clave según que tanto credito pedirá el cliente (monto simulado)
'Cantidad simulaciones': Habla de un comportamiento clave de cuantas simulaciones hace el cliente
'Tasa de concresion': Habla de un comportamiento clave de cuantas simulaciones concreta en ventas


08-10-2024

Más que elegir un buen algoritmo de clustering creo que el enfoque debe ser distinto. Debemos enfocarnos más en el problema(separar los datos con algo que nos permita identificar
el comportamiento y algunas caracteristicas de interés) con esto quizas tiene más sentido definir politicas de separacion por variables y concatenarlas para obtener los clusters.
Elegir un algoritmo de clustering puede ser interesante a niveles de programacion y todo eso, pero nos aleja de poder obtener una buena explicacion de los datos.

Esto es, por ejemplo, definir 3 cortes de la renta. Si estas bajo x valor tienes renta baja, si estás entre x e y valor tienes renta media y si tienes sobre y tienes renta alta. Luego algo
similar con la probabilidad de pago. Si tienes renta alta y eres buen pagador nos interesa como banco que simules y tomes un credito con nosotros. Esto tiene la ventaja de que es
muy rapido de correr y permite ir actualizando las politicas muchas veces hasta encontrar alguna que sea adecuada. Además podemos definir a priori una cantidad de politicas que permitan que
el problema sea manejable en terminos del tratamiento que le podemos otorgar. 

Este modelo de clusterizacion debe ser capaz de poder responder dos preguntas. En primer lugar, ¿Vale la pena esforzarse en intentar incentivar al cliente a simular en terminos de las ganancias
potenciales que este puede proporcionarnos? Y en segundo lugar ¿Es rentable dedicar esfuerzos para incentivar al cliente a realizar simulaciones, considerando hasta qué punto podemos influir en su comportamiento a través de correos electrónicos o la intervención de nuestros ejecutivos?

Para abordar esta cuestión, necesitamos ser capaces de segmentar a los clientes según características que reflejen tanto su potencial de ganancias como su susceptibilidad a ser incentivados para simular, es decir, su respuesta(en termino de simulaciones) a nuestras estrategias de acercamiento.

Ahora bien, vale la pena preguntarse, ¿que variables nos interesan?. A priori diría que para las características del cliente que nos habla de la potencial ganancia que nos puede
otorgar ese cliente una vez le hemos aceptado un credito son: sobre todo la Renta y la Probabilidad de no pago. Si tomamos solo estas dos variables quedaríamos con (Cantidad de cortes en renta definido por la politica + 1 * Cantidad de cortes en probabilidad no pago definido por la politica + 1) clusters de características.


