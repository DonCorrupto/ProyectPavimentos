from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
#import retro_calculo as data

app = Flask(__name__)
CORS(app)

@app.route('/api/get_data', methods=['GET'])

def get_data():
    mensaje = {'mensaje': 'Obtener datos'}
    return jsonify(mensaje)

@app.route('/api/cargar_csv', methods=['POST'])

def cargar_csv():
    archivo_csv = request.files['archivo_csv']
    
    # Procesa el archivo CSV utilizando pandas
    df = pd.read_csv(archivo_csv)

    df.to_pickle('dataframe.pkl')

    return jsonify({'mensaje': 'Datos del CSV procesados correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
