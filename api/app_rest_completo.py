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
            'title': 'Unsupported Media Type',
            'status': 415,
            'detail': 'Unsupported Media Type. Please use application/json or application/x-www-form-urlencoded'
        }), 415

    return None

def validate_accept_header():
    """Middleware para validar Accept header"""
    accept_header = request.headers.get('Accept')
    if not accept_header:
        return None

    # Aceita qualquer tipo de conteúdo se for */*
    if accept_header == '*/*':
        return None

    # Aceita application/json
    if 'application/json' in accept_header:
        return None

    allowed_accept_types = {
        '/admin/products': {
            'GET': ['text/csv']
        }
    }

    route = next((r for r in allowed_accept_types.keys() if request.path.startswith(r)), None)
    if route and request.method in allowed_accept_types[route]:
        if accept_header in allowed_accept_types[route][request.method]:
            return None

    return jsonify({
        'title': 'Not Acceptable',
        'status': 406,
        'detail': f'Not Acceptable format requested: {accept_header}, only application/json and text/csv are supported'
    }), 406

def token_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        protected_routes = ['/admin', '/orders']
        if not any(request.path.startswith(route) for route in protected_routes):
            return f(*args, **kwargs)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Unauthorized'}), 401

        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user_id = decoded['sub']
        except Exception as e:
            return jsonify({'message': 'Unauthorized'}), 401

        return f(*args, **kwargs)
    return decorated

# ==============================================
# Configuração de Content Negotiation
# ==============================================
def get_best_response_format():
    """
    Implementa content negotiation baseado nos headers Accept e Content-Type
    Retorna o formato preferido pelo cliente (json, xml, etc)
    """
    accept_header = request.headers.get('Accept', 'application/json')
    content_type = request.headers.get('Content-Type', 'application/json')
    
    if 'application/json' in accept_header:
        return 'json'
    elif 'application/xml' in accept_header:
        return 'xml'
    return 'json'

# ==============================================
# Implementação de HATEOAS (Hypermedia)
# ==============================================
def add_hal_links(data, resource_type):
    """
    Adiciona links HATEOAS seguindo o padrão HAL (Hypertext Application Language)
    """
    base_url = request.host_url.rstrip('/')
    
    if isinstance(data, list):
        return {
            '_embedded': {
                resource_type: data
            },
            '_links': {
                'self': {'href': f'{base_url}/{resource_type}'},
                'create': {'href': f'{base_url}/{resource_type}', 'method': 'POST'}
            }
        }
    else:
        return {
            **data,
            '_links': {
                'self': {'href': f'{base_url}/{resource_type}/{data["id"]}'},
                'update': {'href': f'{base_url}/{resource_type}/{data["id"]}', 'method': 'PUT'},
                'delete': {'href': f'{base_url}/{resource_type}/{data["id"]}', 'method': 'DELETE'}
            }
        }

# ==============================================
# Banco de dados em memória para exemplo
# ==============================================
livros = []
usuarios = [
    {
        'id': 1,
        'email': 'admin@user.com',
        'password': 'admin',
        'role': 'admin'
    },
    {
        'id': 2,
        'email': 'customer@user.com',
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
    
    # Validação de Accept
    accept_error = validate_accept_header()
    if accept_error:
        return accept_error

@app.after_request
def after_request(response):
    """Middleware executado depois de cada requisição"""
    return log_response(response)

@app.route('/')
def home():
    """Rota inicial que demonstra content negotiation"""
    response_format = get_best_response_format()
    
    if response_format == 'json':
        return jsonify({
            'mensagem': 'API REST com HATEOAS',
            '_links': {
                'livros': {'href': '/livros'},
                'documentacao': {'href': '/docs'}
            }
        }), 200
    else:
        return make_response(
            '<root><mensagem>API REST com HATEOAS</mensagem></root>',
            200,
            {'Content-Type': 'application/xml'}
        )

@app.route('/login', methods=['POST'])
def login():
    """Rota de autenticação"""
    if not request.is_json:
        return jsonify({
            'title': 'Unsupported Media Type',
            'status': 415,
            'detail': 'Content-Type deve ser application/json'
        }), 415

    dados = request.get_json()
    usuario = next((u for u in usuarios if u['email'] == dados.get('email')), None)
    
    if not usuario or usuario['password'] != dados.get('password'):
        return jsonify({
            'title': 'Unauthorized',
            'status': 401,
            'detail': 'Credenciais inválidas'
        }), 401

    token = jwt.encode({
        'sub': usuario['id'],
        'role': usuario['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify({
        'token': token,
        '_links': {
            'self': {'href': '/login', 'method': 'POST'}
        }
    }), 200

@app.route('/livros', methods=['GET', 'OPTIONS'])
def listar_livros():
    """Lista todos os livros com suporte a HATEOAS"""
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization')
        return response

    response_format = get_best_response_format()
    livros_com_links = add_hal_links(livros, 'livros')
    
    if response_format == 'json':
        return jsonify(livros_com_links), 200
    else:
        return make_response(
            '<livros>' + ''.join(f'<livro><id>{l["id"]}</id><titulo>{l["titulo"]}</titulo></livro>' for l in livros) + '</livros>',
            200,
            {'Content-Type': 'application/xml'}
        )

@app.route('/livros', methods=['POST'])
@token_required
def criar_livro():
    """Cria um novo livro com validação e HATEOAS"""
    if not request.is_json:
        return jsonify({
            'title': 'Unsupported Media Type',
            'status': 415,
            'detail': 'Content-Type deve ser application/json'
        }), 415

    dados = request.get_json()
    
    if not dados.get('titulo'):
        return jsonify({
            'title': 'Bad Request',
            'status': 400,
            'detail': 'Título é obrigatório'
        }), 400

    novo_livro = {
        'id': len(livros) + 1,
        'titulo': dados['titulo'],
        'autor': dados.get('autor', 'Desconhecido')
    }
    
    livros.append(novo_livro)
    livro_com_links = add_hal_links(novo_livro, 'livros')
    
    return jsonify(livro_com_links), 201

@app.route('/livros/<int:id>', methods=['GET', 'PUT', 'DELETE', 'OPTIONS'])
@token_required
def gerenciar_livro(id):
    """Gerencia operações em um livro específico"""
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Accept, Authorization')
        return response

    livro = next((l for l in livros if l['id'] == id), None)
    
    if not livro:
        return jsonify({
            'title': 'Not Found',
            'status': 404,
            'detail': 'Livro não encontrado',
            '_links': {
                'listar': {'href': '/livros', 'method': 'GET'}
            }
        }), 404

    if request.method == 'GET':
        livro_com_links = add_hal_links(livro, 'livros')
        return jsonify(livro_com_links), 200

    elif request.method == 'PUT':
        if not request.is_json:
            return jsonify({
                'title': 'Unsupported Media Type',
                'status': 415,
                'detail': 'Content-Type deve ser application/json'
            }), 415

        dados = request.get_json()
        livro['titulo'] = dados.get('titulo', livro['titulo'])
        livro['autor'] = dados.get('autor', livro['autor'])
        
        livro_com_links = add_hal_links(livro, 'livros')
        return jsonify(livro_com_links), 200

    elif request.method == 'DELETE':
        livros.remove(livro)
        return jsonify({
            'title': 'OK',
            'status': 200,
            'detail': 'Livro removido com sucesso',
            '_links': {
                'listar': {'href': '/livros', 'method': 'GET'}
            }
        }), 200

# ==============================================
# Error Handlers
# ==============================================
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'title': 'Bad Request',
        'status': 400,
        'detail': str(error)
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'title': 'Unauthorized',
        'status': 401,
        'detail': str(error)
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'title': 'Not Found',
        'status': 404,
        'detail': str(error)
    }), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'title': 'Internal Server Error',
        'status': 500,
        'detail': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 