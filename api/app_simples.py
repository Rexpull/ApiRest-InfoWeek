# app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Endpoint GET para consumir API pública com parâmetros
@app.route('/api/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1)
    response = requests.get(f'https://jsonplaceholder.typicode.com/users')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Erro ao acessar API externa'}), response.status_code

# Rota teste simples
@app.route('/')
def home():
    return jsonify({'mensagem': 'API REST Mini-Curso está rodando!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
