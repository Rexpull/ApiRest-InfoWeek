from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import json
import jwt
import datetime
from functools import wraps
import logging

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do JWT
JWT_SECRET = "123"  # Em produção, use uma chave segura
JWT_ALGORITHM = "HS256"

# 🔐 Autenticação JWT: Visão Geral
# JWT (JSON Web Token) é um padrão de autenticação sem estado, onde o servidor gera um token assinado contendo informações sobre o usuário. Esse token é enviado ao cliente, que o inclui nos headers das requisições futuras para provar sua identidade.

# 🔑 JWT_SECRET: "123"
# Essa variável é a chave secreta usada para assinar o token JWT. Com ela, o servidor:

# Gera o token (durante o login)

# Valida o token (nas rotas protegidas)

# ⚠️ Importante: Em ambiente de produção, NUNCA use uma chave simples como "123". Use uma string forte e armazenada em um ambiente seguro (ex: variável de ambiente).

# ⚙️ Geração do Token (Login)
# No login, o token é criado com as seguintes informações:


# token = jwt.encode({
#     'sub': usuario['id'],            # ID do usuário (Subject)
#     'role': usuario['role'],         # Papel (admin/customer)
#     'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expiração
# }, JWT_SECRET, algorithm=JWT_ALGORITHM)
# Este token é retornado ao cliente, que deve incluí-lo em cada requisição protegida no header:

# Authorization: Bearer SEU_TOKEN_JWT
# 🧱 Validação do Token – Decorator token_required
# Esse decorator garante que apenas usuários autenticados consigam acessar certas rotas:


# @wraps(f)
# def decorated(*args, **kwargs):
# O que são esses termos?
# 🔁 @wraps(f)
# Mantém o nome e a documentação da função original (f) ao aplicar o decorator.

# Ex: ajuda o Flask a entender qual rota está decorada, além de manter __name__ e __doc__.

# 🧩 *args e **kwargs
# Permitem que a função decorada aceite quaisquer parâmetros posicionais (*args) e nomeados (**kwargs).

# Assim o decorator pode ser usado com qualquer rota, mesmo com argumentos como id em @app.route('/livros/<int:id>').

# 🔐 Trecho-chave da verificação:
# python
# Copiar
# Editar
# auth_header = request.headers.get('Authorization')
# if not auth_header:
#     return jsonify({'erro': 'Token de autorização necessário'}), 401

# token = auth_header.split(' ')[1]
# decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
# request.user_id = decoded['sub']
# Extrai o token do header.

# Decodifica o token usando a chave secreta.

# Armazena o user_id no objeto request, caso precise no restante da execução.



# ==============================================
# Middlewares e Decorators
# ==============================================
def log_request():
    """Middleware para logar todas as requisições"""
    logger.info(f"Request - [{datetime.datetime.now().isoformat()}] {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")

def log_response(response):
    """Middleware para logar todas as respostas"""
    logger.info(f"Response - [{datetime.datetime.now().isoformat()}] {request.method} {request.url} {response.status_code}")
    logger.info(f"Response Headers: {dict(response.headers)}")
    return response

def validate_content_type():
    """Middleware para validar Content-Type"""
    if not request.headers.get('Content-Type'):
        return None

    allowed_content_types = [
        'application/json',
        'application/x-www-form-urlencoded'
    ]

    if request.headers.get('Content-Type') not in allowed_content_types:
        return jsonify({
            'erro': 'Tipo de conteúdo não suportado',
            'status': 415,
            'detalhes': 'Use application/json ou application/x-www-form-urlencoded'
        }), 415

    return None

def token_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        protected_routes = ['/admin', '/orders', '/livros']
        if not any(request.path.startswith(route) for route in protected_routes):
            return f(*args, **kwargs)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'erro': 'Token de autorização necessário'}), 401

        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user_id = decoded['sub']
        except Exception as e:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated

# ==============================================
# Banco de dados em memória para exemplo
# ==============================================
livros = []
usuarios = [
    {
        'id': 1,
        'email': 'admin@user.com',
        'name': 'Administrador',
        'password': 'admin',
        'role': 'admin'
    },
    {
        'id': 2,
        'email': 'customer@user.com',
        'name': 'Customer de Livros',
        'password': 'customer',
        'role': 'customer'
    }
]

# ==============================================
# Rotas da API
# ==============================================
@app.before_request
def before_request():
    """Middleware executado antes de cada requisição"""
    log_request()
    
    # Validação de Content-Type
    content_type_error = validate_content_type()
    if content_type_error:
        return content_type_error

@app.after_request
def after_request(response):
    """Middleware executado depois de cada requisição"""
    return log_response(response)

@app.route('/')
def home():
    """Rota inicial"""
    return jsonify({
        'mensagem': 'API REST - Sistema de Livros',
        'versao': '1.0',
        'status': 'ativo'
    }), 200

@app.route('/login', methods=['POST'])
def login():
    """Rota de autenticação"""


    dados = request.get_json()
    
    if not dados.get('email') or not dados.get('password'):
        return jsonify({
            'erro': 'Dados incompletos',
            'status': 400,
            'detalhes': 'Email e senha são obrigatórios'
        }), 400

    usuario = next((u for u in usuarios if u['email'] == dados.get('email')), None)
    
    if not usuario or usuario['password'] != dados.get('password'):
        return jsonify({
            'erro': 'Credenciais inválidas',
            'status': 401,
            'detalhes': 'Email ou senha incorretos'
        }), 401

    token = jwt.encode({
        'sub': usuario['id'],
        'role': usuario['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify({
        'token': token,
        'usuario': {
            'id': usuario['id'],
            'email': usuario['email'],
            'role': usuario['role'],
            'name': usuario['name'],
        }
    }), 200

@app.route('/livros', methods=['GET'])
def listar_livros():
    """Lista todos os livros"""
    return jsonify({
        'livros': livros,
        'total': len(livros)
    }), 200

@app.route('/livros', methods=['POST'])
@token_required
def criar_livro():
    """Cria um novo livro"""
    if not request.is_json:
        return jsonify({
            'erro': 'Tipo de conteúdo inválido',
            'status': 415,
            'detalhes': 'Content-Type deve ser application/json'
        }), 415

    dados = request.get_json()
    
    if not dados.get('titulo'):
        return jsonify({
            'erro': 'Dados inválidos',
            'status': 400,
            'detalhes': 'Título é obrigatório'
        }), 400

    novo_livro = {
        'id': len(livros) + 1,
        'titulo': dados['titulo'],
        'autor': dados.get('autor', 'Desconhecido'),
        'ano': dados.get('ano'),
        'genero': dados.get('genero'),
        'criado_em': datetime.datetime.now().isoformat()
    }
    
    livros.append(novo_livro)
    
    return jsonify({
        'mensagem': 'Livro criado com sucesso',
        'livro': novo_livro
    }), 201

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    """Obtém um livro específico"""
    livro = next((l for l in livros if l['id'] == id), None)
    
    if not livro:
        return jsonify({
            'erro': 'Livro não encontrado',
            'status': 404,
            'detalhes': f'Livro com ID {id} não existe'
        }), 404

    return jsonify({
        'livro': livro
    }), 200

@app.route('/livros/<int:id>', methods=['PUT'])
@token_required
def atualizar_livro(id):
    """Atualiza um livro específico"""
    if not request.is_json:
        return jsonify({
            'erro': 'Tipo de conteúdo inválido',
            'status': 415,
            'detalhes': 'Content-Type deve ser application/json'
        }), 415

    livro = next((l for l in livros if l['id'] == id), None)
    
    if not livro:
        return jsonify({
            'erro': 'Livro não encontrado',
            'status': 404,
            'detalhes': f'Livro com ID {id} não existe'
        }), 404

    dados = request.get_json()
    
    # Atualiza apenas os campos fornecidos
    if 'titulo' in dados:
        livro['titulo'] = dados['titulo']
    if 'autor' in dados:
        livro['autor'] = dados['autor']
    if 'ano' in dados:
        livro['ano'] = dados['ano']
    if 'genero' in dados:
        livro['genero'] = dados['genero']
    
    livro['atualizado_em'] = datetime.datetime.now().isoformat()
    
    return jsonify({
        'mensagem': 'Livro atualizado com sucesso',
        'livro': livro
    }), 200

@app.route('/livros/<int:id>', methods=['DELETE'])
@token_required
def deletar_livro(id):
    """Remove um livro específico"""
    livro = next((l for l in livros if l['id'] == id), None)
    
    if not livro:
        return jsonify({
            'erro': 'Livro não encontrado',
            'status': 404,
            'detalhes': f'Livro com ID {id} não existe'
        }), 404

    livros.remove(livro)
    
    return jsonify({
        'mensagem': 'Livro removido com sucesso',
        'id': id
    }), 200

@app.route('/livros/buscar', methods=['GET'])
def buscar_livros():
    """Busca livros por título ou autor"""
    termo = request.args.get('termo', '').lower()
    
    if not termo:
        return jsonify({
            'erro': 'Termo de busca necessário',
            'status': 400,
            'detalhes': 'Use o parâmetro "termo" para buscar'
        }), 400
    
    livros_encontrados = [
        livro for livro in livros 
        if termo in livro['titulo'].lower() or termo in livro['autor'].lower()
    ]
    
    return jsonify({
        'livros': livros_encontrados,
        'total': len(livros_encontrados),
        'termo_buscado': termo
    }), 200

# ==============================================
# Error Handlers
# ==============================================
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'erro': 'Requisição inválida',
        'status': 400,
        'detalhes': str(error)
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'erro': 'Não autorizado',
        'status': 401,
        'detalhes': str(error)
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'erro': 'Não encontrado',
        'status': 404,
        'detalhes': str(error)
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'erro': 'Método não permitido',
        'status': 405,
        'detalhes': str(error)
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'erro': 'Erro interno do servidor',
        'status': 500,
        'detalhes': 'Ocorreu um erro inesperado'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)