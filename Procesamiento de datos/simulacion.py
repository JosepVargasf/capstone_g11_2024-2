import pandas as pd
import numpy as np

# Cargar datos
df_clientes = pd.read_csv("Informacion_Clientes.csv")
df_treatment = pd.read_csv("assigned_treatments_intuitivo_4/assignation_20241116_212213/assigned_treatments_intuitivo4.csv")
df_cluster = pd.read_csv("assigned_treatments_intuitivo_4/assignation_20241116_212213/cluster_info_intuitivo4.csv")

# Renombrar categoria_clusterizacion_numerica a cluster
df_cluster = df_cluster.rename(columns={'categoria_clusterizacion_numerica': 'cluster'})

print(f" df_cluster columns are {df_cluster.columns}")

# Seleccionar solo las columnas adicionales de df_cluster
cluster_additional_cols = [col for col in df_cluster.columns if col not in df_treatment.columns and col != 'cluster']

# Realizar el merge utilizando solo las columnas adicionales
df_combined = df_treatment.merge(
    df_cluster[['cluster'] + cluster_additional_cols],  # cluster y columnas adicionales
    on='cluster', 
    how='left'
)

# Dividir tasa_optima por 100 directamente en df_combined
df_combined['tasa_optima'] = df_combined['tasa_optima'] / 100

# Calcular Monto_Simulado en df_clientes
df_clientes['Monto_Simulado'] = (
    -866900 
    + 0.8845 * df_clientes['Renta'] 
    + 0.7231 * df_clientes['Oferta_Consumo'] 
    - 0.105 * df_clientes['Deuda_CMF']
)

# Añadir Monto_Simulado y Probabilidad_No_Pago a df_combined
df_combined = df_combined.merge(
    df_clientes[['rut', 'Monto_Simulado', 'Probabilidad_No_Pago']], 
    on='rut', 
    how='left'
)

# Reemplazar valores negativos en Monto_Simulado con 0
df_combined['Monto_Simulado'] = df_combined['Monto_Simulado'].clip(lower=0)

df_combined['Plazo_Esperado'] = (df_combined['Plazo_Simulado_min'] + df_combined['Plazo_Simulado_max'] + df_combined['Plazo_Simulado_mode'])/3

# Calcular RC
df_combined['RC'] = (
    (df_combined['Plazo_Esperado'] * df_combined['Monto_Simulado'] * df_combined['tasa_optima'] *
     ((1 + df_combined['tasa_optima']) ** df_combined['Plazo_Esperado'])) /
    (((1 + df_combined['tasa_optima']) ** df_combined['Plazo_Esperado']) - 1)
    - df_combined['Monto_Simulado']
)

# Guardar resultado final
df_combined.to_csv("info_final.csv", index=False)

####################################################################################################
# Carga el archivo CSV en un DataFrame
df = pd.read_csv('info_final.csv')
df = df.rename(columns={'Probabilidad_No_Pago_x': 'Probabilidad_No_Pago'})
####################################################################################################

# Check if 'probabilidad_aceptacion_optima' exists in the DataFrame
if 'probabilidad_aceptacion_optima' not in df.columns:
    print("Column 'probabilidad_aceptacion_optima' does not exist in the DataFrame.")
else:
    # Check for NaN values
    num_nans = df['probabilidad_aceptacion_optima'].isnull().sum()
    print(f"Number of NaN values in 'probabilidad_aceptacion_optima': {num_nans}")

    # Remove rows with NaN in 'probabilidad_aceptacion_optima'
    df = df.dropna(subset=['probabilidad_aceptacion_optima'])
    
    # Display the number of NaNs after removal to confirm
    num_nans_after = df['probabilidad_aceptacion_optima'].isnull().sum()
    print(f"Number of NaNs in 'probabilidad_aceptacion_optima' after removal: {num_nans_after}")

    # Check for values less than 0
    num_less_than_0 = (df['probabilidad_aceptacion_optima'] < 0).sum()
    print(f"Number of values < 0 in 'probabilidad_aceptacion_optima': {num_less_than_0}")

    # Check for values greater than 1
    num_greater_than_1 = (df['probabilidad_aceptacion_optima'] > 1).sum()
    print(f"Number of values > 1 in 'probabilidad_aceptacion_optima': {num_greater_than_1}")

# Definimos tambien el costo de los correos
costosms = 100

# Mapeo del número de correos por tratamiento
correos_por_tratamiento = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 0,
    7: 1,
    8: 2
}

# Agregar una columna con el número de correos de acuerdo al tratamiento
df['num_correos'] = df['assigned_treatment'].map(correos_por_tratamiento)

####################################################################################################
# PENDIENTE: EVALUAR SI TRABAJAR SIMPLEMENTE CON RC o para cada cluster definir como tratar los 
# montos y plazos simulados

####################################################################################################
# SIMULACIÓN y KPIS:
# 1.Calcular el valor esperado de ganancias
# 2.Calcular el numero promedio de correos enviados
# 3.Simular las ventas segun las variables aleatorias (sacar creditos cursados y valor promedio ganancias)
# 4.Sacar desviación estandar 

#####################################################################################################
# 1. Valor esperado ganancias (cambiar al tener el estudio de montos y plazos)
# Calcular la ganancia esperada para cada fila considerando los costos de correos
df['ganancia_esperada_fila'] = (
    df['RC'] * 
    df['probabilidad_de_simular'] * 
    df['probabilidad_aceptacion_optima'] * 
    (1 - df['Probabilidad_No_Pago']) -
    (df['num_correos'] * costosms)
)

# Calcular la ganancia_esperada total
ganancia_esperada_total = df['ganancia_esperada_fila'].sum()

print("Ganancia esperada total:", ganancia_esperada_total)
####################################################################################################
# 2. Numero de correos enviados:

# Calcular el número promedio de correos enviados
promedio_correos = df['num_correos'].mean()

# Calcular el total de correos enviados
total_correos_enviados = df['num_correos'].sum()

# Mostrar los resultados
print("Total de correos enviados:", total_correos_enviados)
print("Número promedio de correos enviados:", promedio_correos)

####################################################################################################
# 3 y 4. Simulación
import numpy as np
# Configuración de la simulación
num_simulaciones = 100
ganancias_simuladas = []
tasas_creditos_aceptados = []

# Realizar la simulación
for _ in range(num_simulaciones):
    # Generar plazos simulados con distribución triangular
    plazos_simulados = np.random.triangular(
        df['Plazo_Simulado_min'],
        df['Plazo_Simulado_mode'],
        df['Plazo_Simulado_max']
    )

    # Calcular RC dinámico basado en los plazos simulados
    rc_simulado = (
        (plazos_simulados * df['Monto_Simulado'] * df['tasa_optima'] *
         ((1 + df['tasa_optima']) ** plazos_simulados)) /
        (((1 + df['tasa_optima']) ** plazos_simulados) - 1) -
        df['Monto_Simulado']
    )

    # Simular variables aleatorias (binomiales)
    sim_probabilidad_de_simular = np.random.binomial(1, df['probabilidad_de_simular'])
    sim_probabilidad_aceptacion_optima = np.random.binomial(1, df['probabilidad_aceptacion_optima'])
    sim_Probabilidad_No_Pago = np.random.binomial(1, df['Probabilidad_No_Pago'])

    # Calcular el total de créditos simulados y aceptados
    total_creditos_simulados = sim_probabilidad_de_simular.sum()
    total_creditos_aceptados = (sim_probabilidad_de_simular * sim_probabilidad_aceptacion_optima).sum()
    
    # Calcular la tasa de créditos aceptados
    tasa_creditos_aceptados = (
        total_creditos_aceptados / total_creditos_simulados
        if total_creditos_simulados > 0 else 0
    )

    # Calcular la ganancia esperada para cada fila en esta simulación
    ganancia_simulada_fila = (
        rc_simulado *
        sim_probabilidad_de_simular *
        sim_probabilidad_aceptacion_optima *
        (1 - sim_Probabilidad_No_Pago) -
        (df['num_correos'] * costosms)
    )
    
    # Calcular la ganancia total de esta simulación y almacenarla
    ganancia_total_simulada = ganancia_simulada_fila.sum()
    ganancias_simuladas.append(ganancia_total_simulada)
    tasas_creditos_aceptados.append(tasa_creditos_aceptados)

# Calcular el promedio y la desviación estándar de las ganancias simuladas
promedio_ganancias = np.mean(ganancias_simuladas)
desviacion_ganancias = np.std(ganancias_simuladas)

# Calcular el promedio de la tasa de créditos aceptados
promedio_tasa_creditos_aceptados = np.mean(tasas_creditos_aceptados)

# Mostrar resultados
print("Promedio de ganancias simuladas:", promedio_ganancias)
print("Desviación estándar de ganancias simuladas:", desviacion_ganancias)
print("Tasa promedio de créditos aceptados:", promedio_tasa_creditos_aceptados)