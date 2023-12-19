from pytube import YouTube
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

# Carga las variables de entorno
load_dotenv(find_dotenv())
os.environ["OPENAI_API_KEY"] = os.environ['OPENAI_API_KEY']
openai.api_key = os.environ["OPENAI_API_KEY"]

# Directorio para guardar los audios y textos descargados
saveDir = 'DatosExtraidos/'

# Lee el archivo que contiene las URLs de los videos
with open("InformacionRecolectada/LinkYouTube.txt", "r") as f:
    video_urls = f.readlines()

# Procesa cada URL
for videoURL in video_urls:
    videoURL = videoURL.strip()  # Elimina espacios y saltos de línea
    print(f"\nProcesando {videoURL}...")
    
    # Obtiene el título del video usando pytube
    yt = YouTube(videoURL)
    video_title = yt.title
    print(f"Título del video: {video_title}")
    
    # Reemplaza los caracteres no deseados en el título para hacerlo un nombre de archivo válido
    valid_title = "".join(c for c in video_title if c.isalnum() or c.isspace()).rstrip()
    
    # Verifica si el archivo ya existe
    if os.path.exists(f"{saveDir}/{valid_title}.txt"):
        print(f"El video '{valid_title}' ya ha sido procesado, pasando al siguiente.")
        continue
    
    # Carga y procesa el audio del video
    print("Iniciando la carga y procesamiento del audio...")
    loader = GenericLoader(YoutubeAudioLoader([videoURL], saveDir), OpenAIWhisperParser())
    docs = loader.load()
    
    # Para propósitos de depuración: imprime el contenido del documento
    print("Contenido del documento:", docs[0].page_content)
    
    # Guarda el contenido del video en un archivo .txt con el título del video como nombre de archivo
    with open(f"{saveDir}/{valid_title}.txt", "w") as f:
        f.write(docs[0].page_content)
