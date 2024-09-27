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



