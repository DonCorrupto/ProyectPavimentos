from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/mensaje', methods=['GET'])

def get_data():
    mensaje = {'mensaje': 'Hola desde tu API Flask'}
    return jsonify(mensaje)


if __name__ == '__main__':
    app.run(debug=True)
