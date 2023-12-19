import os
import re
from langchain.document_loaders import PyPDFLoader

# Leer los enlaces de PDF desde un archivo
with open("InformacionRecolectada/LinkPDFs.txt", "r") as f:
    urls = [url.strip() for url in f.readlines()]

# Crear el directorio para los datos extraídos si no existe
os.makedirs('DatosExtraidos', exist_ok=True)

# Iterar a través de cada enlace de PDF
for i, url in enumerate(urls):
    # Construir el nombre de archivo para verificar si ya se procesó
    filename = f'DatosExtraidos/pdf{i+1}.txt'
    
    # Verificar si el archivo ya existe para evitar la extracción repetida
    if not os.path.exists(filename):
        # Cargar el documento PDF
        loader = PyPDFLoader(url)
        pages = loader.load()

        # Unir el contenido de todas las páginas
        all_text = "\n".join(page.page_content for page in pages)

       
        cleaned_text = re.sub('[^A-Za-z0-9áéíóúÁÉÍÓÚñÑ\s]+', '', all_text)  # Eliminar caracteres no alfanuméricos excepto espacios y acentos en español
        cleaned_text = re.sub('\s+', ' ', cleaned_text).strip()   # Reemplazar múltiples espacios con un solo espacio

        # Guardar el contenido en un archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        print(f"El documento PDF {i+1} ha sido procesado.")
