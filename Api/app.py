from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import retro_calculo as data
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/get_data', methods=['GET'])

def get_data():
    geofonos = data.geofonos()
    normalizacion_unidades = data.normalizacion_unidades()
    normalizacion_carga = data.normalizacion_carga()
    temperatura = data.obtener_temperatura_desde_archivo()
    mensaje = {'geofonos': geofonos, 'normalizacion_unidades': normalizacion_unidades, 'normalizacion_carga': normalizacion_carga, 'normalizacion_temperatura': temperatura}
    return mensaje


@app.route('/api/get_modulo_resiliente', methods=['GET'])

def get_modulo_resiliente():
    modulo_resiliente = data.modulo_resiliente()
    return modulo_resiliente

@app.route('/api/tabla_inge', methods=['GET'])
def tabla_inge():
    tabla_inge = data.retro_calculo_inge()
    return tabla_inge

    
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