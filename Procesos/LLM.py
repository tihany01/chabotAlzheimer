import os
import glob
import numpy as np
from dotenv import load_dotenv, find_dotenv
import openai
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings.openai import OpenAIEmbeddings  

# Cargar las variables de entorno
load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]

# Función para generar una respuesta usando el modelo GPT-3
def generar_respuesta_gpt3(pregunta):
    try:
        # Especificar el modelo a utilizar
        modelo = "gpt-3.5-turbo"
        # Generar una respuesta usando GPT-3 de OpenAI
        respuesta_gpt3 = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {
                    "role": "system", 
                    "content": "Este asistente está especializado en la prevención del Alzheimer. Por favor, verifica si la consulta del usuario está relacionada con este tema."
                },
                {
                    "role": "user", 
                    "content": pregunta
                },
                {
                    "role": "assistant", 
                    "content": "¿Tu pregunta está relacionada con la prevención del Alzheimer? Si no es así, te recomendaría buscar información más relevante para tu consulta."
                }

            ]
        )
        # Devolver la respuesta generada
        return respuesta_gpt3['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error al generar respuesta con GPT-3: {e}")
        return None

# Función para cargar todos los vectores del directorio 'vectores'
def cargar_todos_vectores():
    # Inicializar una lista vacía para almacenar los vectores
    vectores = []
    # Recorrer todos los archivos .npy y cargar los vectores
    for npy_file in glob.glob("vectores/*.npy"):
        try:
            vector = np.load(npy_file)
            vectores.append((npy_file, vector))
        except Exception as e:
            # Registrar cualquier error que ocurra
            print(f"Error al cargar el archivo {npy_file}: {e}")
    # Devolver la lista de vectores
    return vectores

# Función para encontrar el vector más similar de una lista
def encontrar_vector_similar(vector_consulta, vectores):
    # Calcular la similitud del coseno entre el vector de consulta y todos los vectores cargados
    vectores_nombre = [x[0] for x in vectores]
    vectores_valores = np.array([x[1] for x in vectores])
    
    similitudes = cosine_similarity([vector_consulta], vectores_valores)[0]
    media_similitud = np.mean(similitudes)
    std_similitud = np.std(similitudes)
    
    # Establecer el umbral de similitud de manera dinámica
    umbral_similitud = media_similitud + (0.9 * std_similitud)
    # Devolver el vector más similar, su similitud y el umbral
    indice_max_similitud = np.argmax(similitudes)
    return vectores_nombre[indice_max_similitud], similitudes[indice_max_similitud], umbral_similitud
# Función para buscar el fragmento de texto correspondiente a un vector
def buscar_fragmento(nombre_archivo_vector):
    # Extraer el ID del fragmento del nombre del archivo
    fragmento_id = os.path.basename(nombre_archivo_vector).replace("_embedding.npy", ".txt")
    fragmento_texto = f"fragmentos/{fragmento_id}"
    # Leer el fragmento de texto correspondiente del directorio 'fragmentos'
    try:
        with open(fragmento_texto, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(fragmento_texto, 'r', encoding='latin-1') as f:
            return f.read()
# Función para procesar la consulta del usuario y generar una respuesta
def procesar_consulta(vector_consulta, vectores, consulta_usuario):
    if vector_consulta is None or not vectores:
        return "Lo siento, hubo un error al procesar tu consulta."
    # Encontrar el vector más similar
    nombre_archivo_vector, max_similitud, umbral_similitud = encontrar_vector_similar(vector_consulta, vectores)

    # Verificar si la similitud máxima está por encima del umbral
    if max_similitud < umbral_similitud:
        return "Lo siento, no pude encontrar información relevante sobre tu consulta."
    
    fragmento = buscar_fragmento(nombre_archivo_vector)
    if fragmento:
        # Imprimir el nombre del archivo del fragmento
        print(f"Respondiendo con el fragmento: {nombre_archivo_vector}")
        # Generar un prompt más explícito para GPT-3
        prompt = f"El usuario preguntó: '{consulta_usuario}'. Basándote en la siguiente información que encontré: '{fragmento}', ¿podrías proporcionar una respuesta?"
        respuesta = generar_respuesta_gpt3(prompt)
        return respuesta if respuesta else "Lo siento, no pude encontrar la información relacionada."
    else:
        return "Lo siento, no pude encontrar la información relacionada."


# Función principal que orquesta las funciones anteriores
def main(consulta_usuario):
    # Cargar todos los vectores
    vectores = cargar_todos_vectores()
    consulta_usuario = consulta_usuario.lower()
    embeddings = OpenAIEmbeddings()
    vector_consulta = embeddings.embed_query(consulta_usuario)
    respuesta = procesar_consulta(vector_consulta, vectores, consulta_usuario)
    return respuesta

