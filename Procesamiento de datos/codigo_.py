import json

def convertir_ipynb_a_txt(ruta_ipynb, ruta_txt):
    try:
        # Abrir y cargar el archivo .ipynb
        with open(ruta_ipynb, 'r', encoding='utf-8') as archivo_ipynb:
            contenido = json.load(archivo_ipynb)

        # Extraer el contenido de las celdas
        texto = ""
        for celda in contenido.get("cells", []):
            if celda.get("cell_type") in ["code", "markdown"]:
                texto += ''.join(celda.get("source", [])) + '\n\n'

        # Guardar el contenido en un archivo .txt
        with open(ruta_txt, 'w', encoding='utf-8') as archivo_txt:
            archivo_txt.write(texto)

        print(f"Archivo convertido y guardado en: {ruta_txt}")

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Ruta del archivo .ipynb
ruta_ipynb = r"D:\OneDrive - Universidad Católica de Chile\AAA Puc\AAA Semestre 10\Capstone\capstone_g11_2024-2\Procesamiento de datos\procesamiento - copia.ipynb"

# Ruta del archivo .txt de salida
ruta_txt = r"D:\OneDrive - Universidad Católica de Chile\AAA Puc\AAA Semestre 10\Capstone\capstone_g11_2024-2\Procesamiento de datos\procesamiento - copia.txt"

# Convertir
convertir_ipynb_a_txt(ruta_ipynb, ruta_txt)
