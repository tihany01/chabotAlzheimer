import os
import re
from langchain.document_loaders import WebBaseLoader

# Leer el archivo que contiene los enlaces
with open("InformacionRecolectada/LinkSitiosWeb.txt", "r") as f:
    urls = [url.strip() for url in f.readlines()]  # Eliminar cualquier espacio en blanco o nueva línea al final

# Crear el directorio si no existe
os.makedirs('DatosExtraidos', exist_ok=True)

# Iterar a través de cada enlace
for i, url in enumerate(urls):
    # Cargar la página web
    loader = WebBaseLoader(url)
    docs = loader.load()

     # Limpiar el texto
    cleaned_text = re.sub('<.*?>', '', docs[0].page_content)  # Eliminar las etiquetas HTML
    cleaned_text = re.sub('[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', '', cleaned_text)  # Eliminar caracteres no alfanuméricos excepto espacios y acentos en español
    cleaned_text = re.sub('\s+', ' ', cleaned_text).strip()   # Reemplazar múltiples espacios con un solo espacio

    # Contar palabras
    word_count = len(cleaned_text.split())
    
    # Verificar si el archivo ya existe para evitar repetición
    filename = f'DatosExtraidos/sitioweb{i+1}.txt'
    if not os.path.exists(filename):
        # Guardar el contenido en un archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        print(f"El documento {i+1} tiene {word_count} palabras.")

