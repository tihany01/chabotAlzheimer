from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Definir el directorio donde se encuentran los archivos de texto preprocesados
directorio_preprocesado = 'DatosExtraidos/'

# Definir el directorio donde se guardaran los fragmentos
directorio_fragmentos = 'fragmentos/'

# Crear el directorio si no existe
if not os.path.exists(directorio_fragmentos):
    os.makedirs(directorio_fragmentos)

# Definir el tamanio del fragmento y la superposicion
tamanio_fragmento = 1800   #Puedes ajustar este valor segun tus necesidades
solapamiento = 80  # Puedes ajustar este valor segun tus necesidades

# Inicializar el divisor de texto
splitter = RecursiveCharacterTextSplitter(chunk_size=tamanio_fragmento, chunk_overlap=solapamiento)

# Recorrer cada archivo en el directorio preprocesado
for archivo in os.listdir(directorio_preprocesado):
    if archivo.endswith('.txt'):
        # Verificar si ya existen archivos divididos para este archivo de texto
        existen_archivos_divididos = any(nombre.startswith(archivo[:-4]) and nombre.endswith('.txt') for nombre in os.listdir(directorio_fragmentos))
        
        # Si existen archivos divididos, omitir este archivo de texto
        if existen_archivos_divididos:
            print(f"Los archivos divididos para '{archivo}' ya existen, omitiendo...")
            continue

        texto = None
        try:
            with open(os.path.join(directorio_preprocesado, archivo), 'r', encoding='utf-8') as f:
                texto = f.read().lower()  # Convertir el texto a minusculas
        except UnicodeDecodeError:
            try:
                with open(os.path.join(directorio_preprocesado, archivo), 'r', encoding='latin-1') as f:
                    texto = f.read().lower()  # Convertir el texto a minusculas
            except Exception as e:
                print(f"Error al decodificar el archivo {archivo} con UTF-8 y latin-1. Omitiendo... Error: {e}")
                continue

        if texto:
            # Dividir el texto en fragmentos
            fragmentos = splitter.split_text(texto)
            
            # Guardar cada fragmento en un nuevo archivo
            for i, fragmento in enumerate(fragmentos):
                nombre_fragmento = f"{archivo[:-4]}_parte_{i+1}.txt"
                with open(os.path.join(directorio_fragmentos, nombre_fragmento), 'w', encoding='utf-8') as f:
                    f.write(fragmento)


















