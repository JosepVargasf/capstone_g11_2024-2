# -------------------------------
# Procesamiento y preprocesamiento de datos
# -------------------------------

# Definir la carpeta base y el mapeo de tratamientos
base_folder = "cluster_data_20241106_020021/"  # Carpeta donde se encuentran los archivos de datos
tratamiento_map = {  # Mapeo de los tratamientos específicos a identificadores numéricos
    "Ejecutivo=0, Correos=0": 1, "Ejecutivo=0, Correos=1": 2,
    "Ejecutivo=0, Correos=2": 3, "Ejecutivo=0, Correos=3": 4,
    "Ejecutivo=0, Correos=4": 5, "Ejecutivo=1, Correos=0": 6,
    "Ejecutivo=1, Correos=1": 7, "Ejecutivo=1, Correos=2": 8
}

# Definir las rutas de los archivos
probabilities_file = os.path.join(base_folder, "probabilities_treatment.csv")
rut_info_file = os.path.join(base_folder, "rut_info.csv")
cluster_info_file = os.path.join(base_folder, "cluster_info.csv")

# Parámetros
costosms = 100  # Costo de cada mensaje SMS
capacidad_ejecutivos = 205000  # Capacidad máxima en términos de tiempo de los ejecutivos

# Paso 1: Cargar y mapear 'tratamiento_id' en los datos de probabilidades
print("Loading and processing probabilities data...")
df_probabilities = df_probabilities_treatment
df_probabilities['tratamiento_id'] = df_probabilities['Tratamiento'].map(tratamiento_map)

# Paso 2: Crear lista de tratamientos y combinar con rut_info
print("Merging probabilities with rut_info...")
df_probabilities['tratamientos'] = df_probabilities[['probabilidad_simular', 'tratamiento_id']].values.tolist()
grouped_prob = df_probabilities.groupby('categoria_clusterizacion_numerica')['tratamientos'].apply(list).reset_index()

df_rut_info = df_rut_info
df_rut_info = df_rut_info.merge(grouped_prob, on='categoria_clusterizacion_numerica', how='left')

# Paso 3: Combinar rut_info con cluster_info
print("Merging rut_info with cluster_info...")
df_cluster_info = df_cluster_info
df_rut_info = df_rut_info.merge(df_cluster_info, on='categoria_clusterizacion_numerica', how='left')

# Paso 3.5: Agrupar información por cluster en 'rut_info'
# Agrupar por 'categoria_clusterizacion_numerica' y agregar según lo especificado
df_grouped = df_rut_info.groupby('categoria_clusterizacion_numerica').agg({
    'Probabilidad_No_Pago': 'mean',  # Promedio de probabilidad de no pago
    'tratamientos': lambda x: list(x),  # Lista de opciones de tratamiento únicas en cada cluster
    'Monto_Simulado_mean': 'mean',
    'Plazo_Simulado_mean': 'mean',
    'probabilidad_aceptacion_optima': 'mean',
    'tasa_optima': 'mean',
    'rut': 'count'  # Conteo del número de clientes ('rut') en cada cluster
}).rename(columns={'rut': 'n_clientes'}).reset_index()

# Paso 4: Calcular 'RC' (Revenue calculado)
print("Calculating RC...")
df_grouped['tasa_optima'] /= 100  # Convertir tasa óptima a decimal
df_grouped['RC'] = (
    (df_grouped['Plazo_Simulado_mean'] * df_grouped['Monto_Simulado_mean'] * df_grouped['tasa_optima'] *
     ((1 + df_grouped['tasa_optima']) ** df_grouped['Plazo_Simulado_mean'])) /
    (((1 + df_grouped['tasa_optima']) ** df_grouped['Plazo_Simulado_mean']) - 1)
) - df_grouped['Monto_Simulado_mean']

# -------------------------------
# Preparación de datos para optimización
# -------------------------------

# Convertir 'tratamientos' a un arreglo de numpy para mejorar la indexación
# Desarrollar y preparar 'tratamientos' para indexación adecuada
profits = np.array([
    [
        row['n_clientes'] * (row['RC'] * (1 - row['Probabilidad_No_Pago']) * row['probabilidad_aceptacion_optima'] * row['tratamientos'][0][t][0]) - 
        (row['tratamientos'][0][t][1] * costosms)
        for t in range(8)
    ]
    for _, row in df_grouped.iterrows()
])

# Inicializar el modelo de optimización
model = Model("Maximizar_Ganancias")
model.ModelSense = GRB.MAXIMIZE

# Crear variables de decisión y definir el objetivo
n_clients, n_treatments = profits.shape
variables = {}

for i in range(n_clients):
    variables[i] = {}
    for t in range(n_treatments):
        if profits[i, t] > 0:
            variables[i][t] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{t}")

model.setObjective(
    quicksum(variables[i][t] * profits[i, t] for i in variables for t in variables[i])
)

# Restricción: Cada cliente recibe exactamente un tratamiento
for i in variables:
    model.addConstr(quicksum(variables[i].values()) == 1, name=f"OneTreatmentPerClient_{i}")

# Restricción de capacidad para ejecutivos
model.addConstr(
    quicksum(variables[i][t] * df_grouped.loc[i, 'n_clientes'] for i in variables for t in variables[i] if t in [5, 6, 7]) <= capacidad_ejecutivos,
    name="CapacityConstraint"
)

# Consistencia de cluster: los clientes dentro del mismo cluster deben recibir el mismo tratamiento
clusters = df_grouped.groupby("categoria_clusterizacion_numerica").indices
for cluster_id, indices_cluster in clusters.items():
    indices_list = list(indices_cluster)
    leader_index = indices_list[0]
    for t in variables[leader_index]:
        leader_var = variables[leader_index][t]
        for i in indices_list[1:]:
            if t in variables[i]:
                model.addConstr(variables[i][t] == leader_var, name=f"ClusterConsistency_{cluster_id}_{t}")

# Optimizar el modelo
model.optimize()

# Verificar si la optimización fue exitosa
if model.Status == GRB.OPTIMAL:
    # -------------------------------
    # Extracción y visualización de resultados
    # -------------------------------

    print("Extracting results...")

    # Asignar tratamientos por cluster basado en los resultados de la optimización
    resultados_por_cluster = {}
    for cluster_id, indices_cluster in clusters.items():
        leader_index = list(indices_cluster)[0]
        for t in variables[leader_index]:
            if variables[leader_index][t].X > 0.5:
                resultados_por_cluster[cluster_id] = t + 1
                break

    # Calcular las ganancias totales
    ganancias_totales = model.ObjVal

    # Mostrar resultados
    print("\nTratamientos asignados por cluster:")
    for cluster_id, tratamiento in resultados_por_cluster.items():
        print(f"Cluster {cluster_id}: Tratamiento {tratamiento}")

    print(f"\nGanancias totales: {ganancias_totales:.2f}")

    # Calcular el número de ejecutivos usados y restantes
    executives_used = sum(
        df_grouped.loc[i, 'n_clientes'] for i in variables for t in variables[i]
        if t in [5, 6, 7] and variables[i][t].X > 0.5
    )
    executives_remaining = capacidad_ejecutivos - executives_used

    # Mostrar resumen de uso de ejecutivos
    print(f"\nExecutives used: {executives_used}")
    print(f"Executives remaining: {executives_remaining}")
else:
    print("Optimization did not reach an optimal solution.")
print("Optimization complete.")
