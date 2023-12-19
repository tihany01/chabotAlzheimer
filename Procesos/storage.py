import os
import numpy as np
from dotenv import load_dotenv, find_dotenv
import openai
from chromadb.api.types import Embeddings
from langchain.embeddings.openai import OpenAIEmbeddings

# Cargar las variables de entorno
load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = os.environ['OPENAI_API_KEY']
openai.api_key = os.environ["OPENAI_API_KEY"]

# Definir el directorio donde se guardarán los archivos de vectores
vector_directory = 'vectores/'

# Crear el directorio si no existe
if not os.path.exists(vector_directory):
    os.makedirs(vector_directory)

# Definir el directorio donde se encuentran los archivos de texto fragmentados
chunks_directory = 'fragmentos/'

# Inicializar los embeddings de OpenAI
embeddings = OpenAIEmbeddings()

# Recorrer cada archivo en el directorio de fragmentos
for file in os.listdir(chunks_directory):
    if file.endswith('.txt'):
        # Verificar si ya existen archivos de vectores para este archivo de texto fragmentado
        vector_files_exist = any(fname.startswith(file[:-4]) and fname.endswith('.npy') for fname in os.listdir(vector_directory))
        
        # Si existen archivos de vectores, omitir este archivo de texto fragmentado
        if vector_files_exist:
            print(f"Vector files for '{file}' already exist, skipping...")
            continue

        text = None
        try:
            # Intentar abrir y leer el archivo con codificación UTF-8
            with open(os.path.join(chunks_directory, file), 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            try:
                # Si falla la decodificación UTF-8, intentar abrir y leer el archivo con codificación latin-1
                with open(os.path.join(chunks_directory, file), 'r', encoding='latin-1') as f:
                    text = f.read()
            except Exception as e:
                # Si ambas decodificaciones fallan, imprimir un mensaje de error y omitir el archivo
                print(f"Error decoding file {file} with UTF-8 and latin-1. Skipping... Error: {e}")
                continue

        if text:
            # Obtener los embeddings para el fragmento de texto
            embedding = embeddings.embed_query(text)
            
            # Guardar el embedding en un nuevo archivo
            embedding_name = f"{file[:-4]}_embedding.npy"
            np.save(os.path.join(vector_directory, embedding_name), embedding)
