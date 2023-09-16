from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/mensaje', methods=['GET'])

def get_data():
    mensaje = {'mensaje': 'Hola desde tu API Flask'}
    return jsonify(mensaje)

@app.route('/api/cargar_csv', methods=['POST'])

def cargar_csv():
    archivo_csv = request.files['archivo_csv']
    
    # Procesa el archivo CSV (ejemplo con la biblioteca csv de Python)
    import csv
    datos_csv = []
    for linea in archivo_csv:
        fila = linea.decode().strip().split(',')
        datos_csv.append(fila)
    
    # Realiza acciones con los datos del CSV aquí
    
    return 'Archivo CSV cargado exitosamente.'


if __name__ == '__main__':
    app.run(debug=True)
