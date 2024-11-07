# Análisis y Optimización de Estrategias de Crédito Bancario

Este proyecto tiene como objetivo analizar y optimizar las estrategias de oferta de créditos de consumo de un banco, utilizando técnicas de análisis de datos, clustering, modelado estadístico y optimización matemática.

## Contenido del Proyecto

El notebook está estructurado en las siguientes secciones:

1. **Importación de Librerías**
2. **Carga de Datos**
3. **Unión de Datos**
4. **Clustering por Políticas**
5. **Estimación de Curvas de Elasticidad por Cluster**
6. **Estimación de Respuesta a Tratamiento por Cluster**
7. **Modelo de Asignación**

---

## 1. Importación de Librerías

Se importan las librerías necesarias para el análisis y modelado:

- **Análisis de Datos**: `numpy`, `pandas`
- **Modelado Estadístico**: `statsmodels`
- **Optimización**: `gurobipy`
- **Operaciones del Sistema**: `os`, `datetime`
- **Utilidades**: `collections.Counter`

## 2. Carga de Datos

Se cargan los datos desde archivos CSV proporcionados. Estos incluyen:

- **Información de Clientes (`Informacion_Clientes.csv`)**: Datos demográficos y financieros de los clientes.
- **Simulaciones de Clientes (`Simulaciones_Clientes.csv`)**: Registros de simulaciones de créditos realizadas por los clientes en la página web del banco.
- **Tratamiento (`Tratamiento.csv`)**: Información sobre las interacciones del banco con los clientes (número de correos enviados, asignación de ejecutivos).
- **Ventas (`Ventas.csv`)**: Registros de ventas efectivamente realizadas a los clientes.

> **Nota**: Se elimina la columna `Tiempo_como_cliente` de `Informacion_Clientes.csv` por considerarse irrelevante para el análisis.

## 3. Unión de Datos

Se realiza la consolidación de los datasets mediante operaciones de merge en pandas, creando un DataFrame unificado que contiene toda la información relevante de los clientes, simulaciones, ventas y tratamientos.

- Se crean columnas indicadoras como `simulo` y `venta` para marcar si el cliente realizó una simulación o una compra en una fecha determinada.
- Se extrae el período (mes) de la fecha para facilitar análisis temporales.

## 4. Clustering por Políticas

Se segmenta la base de clientes en clusters utilizando variables demográficas y comportamentales:

- **Variables Utilizadas**:
  - **Categoría Digital**
  - **Edad**
  - **Género**
  - **Propensión**
  - **Probabilidad de No Pago**
  - **Renta**

- **Proceso de Clustering**:
  - Se discretizan las variables continuas en categorías utilizando cuantiles y cortes definidos.
  - Se crea una categoría combinada (`categoria_clusterizacion`) concatenando las categorías individuales.
  - Se asigna un código numérico único a cada cluster para facilitar su identificación.

## 5. Estimación de Curvas de Elasticidad por Cluster

Para cada cluster:

- **Modelo de Regresión Logística**:
  - Se ajusta un modelo para predecir la probabilidad de aceptación de un crédito en función de la tasa de interés.
  - Se utilizan los datos de simulaciones y ventas para entrenar el modelo.

- **Optimización de Tasa**:
  - Se calcula la tasa de interés que maximiza el revenue esperado.
  - Se considera la probabilidad de aceptación, el monto y plazo simulado, y la probabilidad de no pago.

- **Resultados Registrados**:
  - Tasa óptima por cluster.
  - Revenue esperado máximo.
  - Número de clientes y simulaciones en el cluster.
  - Probabilidad de aceptación en la tasa óptima.
  - Número esperado de créditos aceptados.

## 6. Estimación de Respuesta a Tratamiento por Cluster

Se analiza cómo diferentes tratamientos afectan la probabilidad de que un cliente realice una simulación:

- **Tratamientos Considerados**:
  - Número de correos enviados.
  - Asignación de un ejecutivo.

- **Cálculo de Probabilidades**:
  - Se calcula la probabilidad de simulación para cada combinación de cluster y tratamiento.
  - Se utiliza la proporción de casos favorables (clientes que simularon) sobre el total de casos.

- **Resultados**:
  - Se genera una tabla con las probabilidades de simulación por tratamiento y cluster.
  - Esta información se utilizará en el modelo de optimización para asignar tratamientos.

## 7. Modelo de Asignación

Se construye un modelo de optimización para asignar tratamientos a los clusters, con el objetivo de maximizar el revenue esperado:

- **Variables de Decisión**:
  - Asignación de tratamientos a clusters o clientes.

- **Restricciones**:
  - Cada cliente o cluster recibe un único tratamiento.
  - Capacidad limitada de los ejecutivos.
  - Consistencia de tratamiento dentro de cada cluster.

- **Modelo de Optimización**:
  - Se utiliza Gurobi para resolver el modelo de programación entera.
  - El objetivo es maximizar las ganancias totales considerando costos y restricciones.

- **Resultados**:
  - Tratamientos óptimos asignados a cada cluster.
  - Ganancias totales estimadas.
  - Uso de capacidad de ejecutivos.

---

## Cómo Utilizar el Proyecto

### Requerimientos Previos

- **Python 3.x**
- **Librerías**:
  - `numpy`
  - `pandas`
  - `statsmodels`
  - `gurobipy` (se requiere una licencia de Gurobi)
  - `os`
  - `datetime`
  - `collections`

### Ejecución

1. **Instalación de Dependencias**:

   ```bash
   pip install numpy pandas statsmodels gurobipy
