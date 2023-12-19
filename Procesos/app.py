from flask import Flask, request, jsonify
# Importar la función principal del módulo LLM. 
from LLM import main  
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
CORS(app)

@app.route('/api/generar_respuesta', methods=['POST'])
def generar_respuesta():
    try:
        # Extraer el campo 'consulta' de la solicitud JSON entrante.
        consulta = request.json['consulta']
        # Llamar a la función principal (importada de LLM) con consulta como argumento y almacenar el resultado en respuesta.
        respuesta = main(consulta)
        # Devolver la 'respuesta' en formato JSON.
        return jsonify({'respuesta': respuesta})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)

















