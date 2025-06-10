# app.py
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Banco de dados em memória para exemplo (será substituído pelo banco real depois)
livros_memoria = []

# ====================
# Rota inicial da API
# ====================
@app.route('/')
def home():
    return jsonify({'mensagem': 'API REST Mini-Curso está rodando!'}), 200

# ==================================================
# Consome API pública para demonstrar uso de request
# ==================================================
@app.route('/api/users', methods=['GET'])
def get_users():
    # Captura o parâmetro ?page opcional
    page = request.args.get('page', 1)
    response = requests.get(f'https://jsonplaceholder.typicode.com/users')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Erro ao acessar API externa'}), response.status_code

# ===========================
# CRUD em memória (Livro)
# ===========================

# GET - Listar todos os livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    return jsonify(livros_memoria), 200

# POST - Adicionar um livro
@app.route('/livros', methods=['POST'])
def adicionar_livro():
    dados = request.get_json()
    # Validação básica
    if not dados.get('titulo') or not dados.get('autor'):
        return jsonify({'erro': 'Título e autor são obrigatórios'}), 400

    livro = {
        'id': len(livros_memoria) + 1,
        'titulo': dados['titulo'],
        'autor': dados['autor'],
        'ano': dados['ano'],
        'genero': dados['genero']
    }
    livros_memoria.append(livro)
    return jsonify(livro), 201

# PUT - Atualizar livro existente
@app.route('/livros/<int:id>', methods=['PUT'])
def atualizar_livro(id):
    dados = request.get_json()
    for livro in livros_memoria:
        if livro['id'] == id:
            livro['titulo'] = dados.get('titulo', livro['titulo'])
            livro['autor'] = dados.get('autor', livro['autor'])
            livro['ano'] = dados.get('ano', livro['ano'])
            livro['genero'] = dados.get('genero', livro['genero'])

            return jsonify(livro), 200
    return jsonify({'erro': 'Livro não encontrado'}), 404

# DELETE - Remover livro
@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    for livro in livros_memoria:
        if livro['id'] == id:
            livros_memoria.remove(livro)
            return jsonify({'mensagem': 'Livro removido com sucesso'}), 200
    return jsonify({'erro': 'Livro não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
