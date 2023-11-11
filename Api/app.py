from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import retro_calculo as data
import os

app = Flask(__name__)
CORS(app)


@app.route('/api/get_image', methods=['GET'])
def get_image():
    # Ruta a la imagen en tu servidor
    image_path = 'images/image1.png'

    # Verificar si la imagen existe
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return 'Imagen no encontrada', 404
    


@app.route('/api/get_data', methods=['GET'])

def get_data():
    geofonos = data.geofonos()
    mensaje = {'geofonos': geofonos}
    return mensaje


@app.route('/api/get_tabla', methods=['GET'])

def get_tabla():
    tabla = data.tabla()
    return tabla

    
@app.route('/api/cargar_csv', methods=['POST'])

def cargar_csv():
    archivo_csv = request.files['archivo_csv']
    temperatura = request.form.get('temperatura')

    with open('temperatura.txt', 'w') as file:
        file.write(temperatura)
    
    # Procesa el archivo CSV utilizando pandas
    df = pd.read_csv(archivo_csv)

    df.to_pickle('dataframe.pkl')

    return jsonify({'mensaje': 'Datos del CSV procesados correctamente'})


@app.route('/api/distancia_geofono', methods=['POST'])

def distancia_geofono():
    distancia_D = request.form.get('distancia_D')
    with open('distancia_D.txt', 'w') as file:
        file.write(distancia_D)

    return jsonify({'mensaje': 'Distancia_D correctamente'})

if __name__ == '__main__':
    app.run(debug=True)