from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps
import logging
import jwt
import os

# Importa os modelos e configuração do banco
from models import db, User, Book, Category
from database import create_app, init_database

# Cria a aplicação usando a factory function
app = create_app()

# Configuração avançada do CORS
CORS(app, 
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # URLs do frontend
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],         # Métodos permitidos
     allow_headers=["Content-Type", "Authorization"],             # Headers permitidos
     supports_credentials=True                                    # Permite cookies/credenciais
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do JWT
JWT_SECRET = os.environ.get('JWT_SECRET', "1231")  # Prioriza variável de ambiente
JWT_ALGORITHM = "HS256"
JWT_CUSTOM_SECRET = None  # Permite chave personalizada via API

# ==============================================
# Funções auxiliares para JWT
# ==============================================
def get_jwt_secret():
    """Retorna a chave JWT atual (personalizada ou padrão)"""
    return JWT_CUSTOM_SECRET or JWT_SECRET

def set_custom_jwt_secret(new_secret):
    """Define uma nova chave JWT personalizada"""
    global JWT_CUSTOM_SECRET
    if new_secret and len(new_secret) >= 8:
        JWT_CUSTOM_SECRET = new_secret
        return True
    return False

# ==============================================
# Middlewares e Decorators
# ==============================================
def log_request():
    """Middleware para logar todas as requisições"""
    logger.info(f"Request - [{datetime.now().isoformat()}] {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")

def log_response(response):
    """Middleware para logar todas as respostas"""
    logger.info(f"Response - [{datetime.now().isoformat()}] {request.method} {request.url} {response.status_code}")
    return response

def validate_json():
    """Middleware para validar JSON em requisições POST/PUT"""
    if request.method in ['POST', 'PUT'] and not request.is_json:
        return jsonify({
            'erro': 'Tipo de conteúdo inválido',
            'status': 415,
            'detalhes': 'Content-Type deve ser application/json'
        }), 415
    return None

def token_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'erro': 'Token de autorização necessário'}), 401

        try:
            token = auth_header.split(' ')[1]
            decoded = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
            current_user = User.query.get(decoded['sub'])
            if not current_user or not current_user.ativo:
                return jsonify({'erro': 'Usuário inválido ou inativo'}), 401
            request.current_user = current_user
        except Exception as e:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator para rotas que requerem privilégios de administrador"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if request.current_user.role != 'admin':
            return jsonify({'erro': 'Acesso negado - privilégios de administrador necessários'}), 403
        return f(*args, **kwargs)
    return decorated

# ==============================================
# Rotas da API
# ==============================================
@app.before_request
def before_request():
    """Middleware executado antes de cada requisição"""
    log_request()
    
    # Validação de JSON para POST/PUT
    json_error = validate_json()
    if json_error:
        return json_error

@app.after_request
def after_request(response):
    """Middleware executado depois de cada requisição"""
    return log_response(response)

@app.route('/')
def home():
    """Rota inicial da API"""
    return jsonify({
        'mensagem': 'API REST - Sistema de Biblioteca',
        'versao': '2.0',
        'database': 'SQLAlchemy + SQLite',
        'status': 'ativo',
        'cors': {
            'enabled': True,
            'origins': ["http://localhost:3000", "http://127.0.0.1:3000"],
            'methods': ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        },
        'endpoints': {
            'autenticacao': '/login',
            'livros': '/livros',
            'usuarios': '/usuarios',
            'categorias': '/categorias',
            'jwt_config': '/jwt/configure',
            'jwt_info': '/jwt/info'
        }
    }), 200

@app.route('/options-info')
def options_info():
    """Explica como funciona o método OPTIONS"""
    return jsonify({
        'metodo': 'OPTIONS',
        'proposito': 'Verificar quais métodos e headers são permitidos',
        'cors_preflight': {
            'descricao': 'Requisição automática feita pelo navegador antes de requests complexos',
            'quando_acontece': [
                'Métodos diferentes de GET, POST simples',
                'Headers personalizados como Authorization',
                'Content-Type application/json'
            ],
            'headers_verificados': [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods', 
                'Access-Control-Allow-Headers'
            ]
        },
        'exemplo_uso': {
            'curl': 'curl -X OPTIONS http://localhost:5003/livros -H "Origin: http://localhost:3000"',
            'javascript': 'fetch("http://localhost:5003/livros", { method: "OPTIONS" })'
        }
    }), 200

# ==============================================
# Rotas de Configuração JWT
# ==============================================
@app.route('/jwt/configure', methods=['POST'])
def configure_jwt():
    """Configura uma chave JWT personalizada"""
    dados = request.get_json()
    
    if not dados.get('secret'):
        return jsonify({
            'erro': 'Chave secreta necessária',
            'status': 400,
            'detalhes': 'Campo "secret" é obrigatório'
        }), 400
    
    new_secret = dados['secret']
    
    if len(new_secret) < 8:
        return jsonify({
            'erro': 'Chave muito fraca',
            'status': 400,
            'detalhes': 'A chave deve ter pelo menos 8 caracteres'
        }), 400
    
    if set_custom_jwt_secret(new_secret):
        return jsonify({
            'mensagem': 'Chave JWT configurada com sucesso',
            'secret_length': len(new_secret),
            'configurado_em': datetime.utcnow().isoformat()
        }), 200
    else:
        return jsonify({
            'erro': 'Erro ao configurar chave',
            'status': 500
        }), 500

@app.route('/jwt/info', methods=['GET'])
def jwt_info():
    """Retorna informações sobre a configuração JWT atual"""
    current_secret = get_jwt_secret()
    return jsonify({
        'algorithm': JWT_ALGORITHM,
        'secret_source': 'custom' if JWT_CUSTOM_SECRET else 'default',
        'secret_length': len(current_secret),
        'is_strong': len(current_secret) >= 32,
        'recommendations': {
            'minimum_length': 32,
            'include_special_chars': True,
            'use_environment_variable': True
        }
    }), 200

# ==============================================
# Rotas de Autenticação
# ==============================================
@app.route('/login', methods=['POST'])
def login():
    """Rota de autenticação com banco de dados"""
    dados = request.get_json()
    
    if not dados.get('email') or not dados.get('password'):
        return jsonify({
            'erro': 'Dados incompletos',
            'status': 400,
            'detalhes': 'Email e senha são obrigatórios'
        }), 400

    usuario = User.query.filter_by(email=dados['email']).first()
    
    if not usuario or not usuario.check_password(dados['password']):
        return jsonify({
            'erro': 'Credenciais inválidas',
            'status': 401,
            'detalhes': 'Email ou senha incorretos'
        }), 401
    
    if not usuario.ativo:
        return jsonify({
            'erro': 'Conta inativa',
            'status': 401,
            'detalhes': 'Sua conta foi desativada'
        }), 401

    token = jwt.encode({
        'sub': usuario.id,
        'role': usuario.role,
        'email': usuario.email,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, get_jwt_secret(), algorithm=JWT_ALGORITHM)

    return jsonify({
        'token': token,
        'usuario': usuario.to_dict()
    }), 200

@app.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    dados = request.get_json()
    
    # Validação dos campos obrigatórios
    campos_obrigatorios = ['email', 'password', 'nome']
    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return jsonify({
                'erro': 'Dados incompletos',
                'status': 400,
                'detalhes': f'Campo {campo} é obrigatório'
            }), 400
    
    # Verifica se o email já existe
    if User.query.filter_by(email=dados['email']).first():
        return jsonify({
            'erro': 'Email já cadastrado',
            'status': 409,
            'detalhes': 'Este email já está em uso'
        }), 409
    
    # Cria o novo usuário
    novo_usuario = User(
        email=dados['email'],
        nome=dados['nome'],
        role=dados.get('role', 'customer')
    )
    novo_usuario.set_password(dados['password'])
    
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário criado com sucesso',
            'usuario': novo_usuario.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro': 'Erro ao criar usuário',
            'status': 500,
            'detalhes': str(e)
        }), 500

# ==============================================
# Rotas de Livros
# ==============================================
@app.route('/livros', methods=['GET'])
def listar_livros():
    """Lista todos os livros com paginação e filtros"""
    # Parâmetros de paginação
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)
    
    # Parâmetros de filtro
    autor = request.args.get('autor')
    genero = request.args.get('genero')
    ano = request.args.get('ano', type=int)
    disponivel = request.args.get('disponivel')
    
    # Query base
    query = Book.query
    
    # Aplica filtros
    if autor:
        query = query.filter(Book.autor.ilike(f'%{autor}%'))
    if genero:
        query = query.filter(Book.genero.ilike(f'%{genero}%'))
    if ano:
        query = query.filter(Book.ano == ano)
    if disponivel is not None:
        disponivel_bool = disponivel.lower() in ['true', '1', 'sim']
        query = query.filter(Book.disponivel == disponivel_bool)
    
    # Ordena por título
    query = query.order_by(Book.titulo)
    
    # Paginação
    livros_paginados = query.paginate(
        page=pagina, 
        per_page=por_pagina, 
        error_out=False
    )
    
    return jsonify({
        'livros': [livro.to_dict() for livro in livros_paginados.items],
        'paginacao': {
            'pagina_atual': livros_paginados.page,
            'total_paginas': livros_paginados.pages,
            'total_itens': livros_paginados.total,
            'por_pagina': livros_paginados.per_page,
            'tem_proxima': livros_paginados.has_next,
            'tem_anterior': livros_paginados.has_prev
        }
    }), 200

@app.route('/livros', methods=['POST'])
@token_required
def criar_livro():
    """Cria um novo livro"""
    dados = request.get_json()
    
    # Validação dos campos obrigatórios
    if not dados.get('titulo') or not dados.get('autor'):
        return jsonify({
            'erro': 'Dados inválidos',
            'status': 400,
            'detalhes': 'Título e autor são obrigatórios'
        }), 400
    
    # Verifica se o ISBN já existe (se fornecido)
    if dados.get('isbn'):
        if Book.query.filter_by(isbn=dados['isbn']).first():
            return jsonify({
                'erro': 'ISBN já cadastrado',
                'status': 409,
                'detalhes': 'Este ISBN já está em uso'
            }), 409

    novo_livro = Book(
        titulo=dados['titulo'],
        autor=dados['autor'],
        ano=dados.get('ano'),
        genero=dados.get('genero'),
        isbn=dados.get('isbn'),
        descricao=dados.get('descricao'),
        paginas=dados.get('paginas'),
        criado_por=request.current_user.id
    )
    
    try:
        db.session.add(novo_livro)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Livro criado com sucesso',
            'livro': novo_livro.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro': 'Erro ao criar livro',
            'status': 500,
            'detalhes': str(e)
        }), 500

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    """Obtém um livro específico"""
    livro = Book.query.get(id)
    
    if not livro:
        return jsonify({
            'erro': 'Livro não encontrado',
            'status': 404,
            'detalhes': f'Livro com ID {id} não existe'
        }), 404

    return jsonify({
        'livro': livro.to_dict()
    }), 200

@app.route('/livros/<int:id>', methods=['PUT'])
@token_required
def atualizar_livro(id):
    """Atualiza um livro específico"""
    livro = Book.query.get(id)
    
    if not livro:
        return jsonify({
            'erro': 'Livro não encontrado',
            'status': 404,
            'detalhes': f'Livro com ID {id} não existe'
        }), 404
    
    # Verifica se o usuário pode editar (admin ou criador)
    if request.current_user.role != 'admin' and livro.criado_por != request.current_user.id:
        return jsonify({
            'erro': 'Acesso negado',
            'status': 403,
            'detalhes': 'Você só pode editar livros que criou'
        }), 403

    dados = request.get_json()
    
    # Verifica ISBN duplicado (se alterado)
    if dados.get('isbn') and dados['isbn'] != livro.isbn:
        if Book.query.filter_by(isbn=dados['isbn']).first():
            return jsonify({
                'erro': 'ISBN já cadastrado',
                'status': 409,
                'detalhes': 'Este ISBN já está em uso'
            }), 409
    
    # Atualiza os campos fornecidos
    campos_editaveis = ['titulo', 'autor', 'ano', 'genero', 'isbn', 'descricao', 'paginas', 'disponivel']
    for campo in campos_editaveis:
        if campo in dados:
            setattr(livro, campo, dados[campo])
    
    try:
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Livro atualizado com sucesso',
            'livro': livro.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro': 'Erro ao atualizar livro',
            'status': 500,
            'detalhes': str(e)
        }), 500

@app.route('/livros/<int:id>', methods=['DELETE'])
@token_required
def deletar_livro(id):
    """Remove um livro específico"""
    livro = Book.query.get(id)
    
    if not livro:
        return jsonify({
            'erro': 'Livro não encontrado',
            'status': 404,
            'detalhes': f'Livro com ID {id} não existe'
        }), 404
    
    # Verifica se o usuário pode deletar (admin ou criador)
    if request.current_user.role != 'admin' and livro.criado_por != request.current_user.id:
        return jsonify({
            'erro': 'Acesso negado',
            'status': 403,
            'detalhes': 'Você só pode deletar livros que criou'
        }), 403

    try:
        db.session.delete(livro)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Livro removido com sucesso',
            'id': id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro': 'Erro ao deletar livro',
            'status': 500,
            'detalhes': str(e)
        }), 500

@app.route('/livros/buscar', methods=['GET'])
def buscar_livros():
    """Busca livros por título, autor ou descrição"""
    termo = request.args.get('q', '').strip()
    
    if not termo:
        return jsonify({
            'erro': 'Termo de busca necessário',
            'status': 400,
            'detalhes': 'Use o parâmetro "q" para buscar'
        }), 400
    
    # Busca por título, autor ou descrição
    livros = Book.query.filter(
        db.or_(
            Book.titulo.ilike(f'%{termo}%'),
            Book.autor.ilike(f'%{termo}%'),
            Book.descricao.ilike(f'%{termo}%')
        )
    ).order_by(Book.titulo).all()
    
    return jsonify({
        'livros': [livro.to_dict() for livro in livros],
        'total': len(livros),
        'termo_buscado': termo
    }), 200

# ==============================================
# Rotas de Usuários (Admin)
# ==============================================
@app.route('/usuarios', methods=['GET'])
@admin_required
def listar_usuarios():
    """Lista todos os usuários (apenas admin)"""
    usuarios = User.query.order_by(User.nome).all()
    
    return jsonify({
        'usuarios': [usuario.to_dict() for usuario in usuarios],
        'total': len(usuarios)
    }), 200

@app.route('/usuarios/<int:id>', methods=['PUT'])
@admin_required
def atualizar_usuario(id):
    """Atualiza um usuário (apenas admin)"""
    usuario = User.query.get(id)
    
    if not usuario:
        return jsonify({
            'erro': 'Usuário não encontrado',
            'status': 404,
            'detalhes': f'Usuário com ID {id} não existe'
        }), 404

    dados = request.get_json()
    
    # Atualiza os campos fornecidos
    campos_editaveis = ['nome', 'email', 'role', 'ativo']
    for campo in campos_editaveis:
        if campo in dados:
            setattr(usuario, campo, dados[campo])
    
    # Atualiza senha se fornecida
    if dados.get('password'):
        usuario.set_password(dados['password'])
    
    try:
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Usuário atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro': 'Erro ao atualizar usuário',
            'status': 500,
            'detalhes': str(e)
        }), 500

# ==============================================
# Rotas de Categorias
# ==============================================
@app.route('/categorias', methods=['GET'])
def listar_categorias():
    """Lista todas as categorias"""
    categorias = Category.query.filter_by(ativa=True).order_by(Category.nome).all()
    
    return jsonify({
        'categorias': [categoria.to_dict() for categoria in categorias],
        'total': len(categorias)
    }), 200

@app.route('/categorias', methods=['POST'])
@admin_required
def criar_categoria():
    """Cria uma nova categoria (apenas admin)"""
    dados = request.get_json()
    
    if not dados.get('nome'):
        return jsonify({
            'erro': 'Dados inválidos',
            'status': 400,
            'detalhes': 'Nome é obrigatório'
        }), 400
    
    # Verifica se a categoria já existe
    if Category.query.filter_by(nome=dados['nome']).first():
        return jsonify({
            'erro': 'Categoria já existe',
            'status': 409,
            'detalhes': 'Uma categoria com este nome já existe'
        }), 409

    nova_categoria = Category(
        nome=dados['nome'],
        descricao=dados.get('descricao')
    )
    
    try:
        db.session.add(nova_categoria)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Categoria criada com sucesso',
            'categoria': nova_categoria.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro': 'Erro ao criar categoria',
            'status': 500,
            'detalhes': str(e)
        }), 500

# ==============================================
# Rotas de Estatísticas
# ==============================================
@app.route('/stats', methods=['GET'])
@admin_required
def estatisticas():
    """Retorna estatísticas do sistema (apenas admin)"""
    stats = {
        'total_livros': Book.query.count(),
        'livros_disponiveis': Book.query.filter_by(disponivel=True).count(),
        'total_usuarios': User.query.count(),
        'usuarios_ativos': User.query.filter_by(ativo=True).count(),
        'total_categorias': Category.query.filter_by(ativa=True).count(),
        'livros_por_genero': {}
    }
    
    # Contagem por gênero
    generos = db.session.query(Book.genero, db.func.count(Book.id)).filter(
        Book.genero.isnot(None)
    ).group_by(Book.genero).all()
    
    for genero, count in generos:
        stats['livros_por_genero'][genero] = count
    
    return jsonify(stats), 200

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

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'erro': 'Acesso proibido',
        'status': 403,
        'detalhes': str(error)
    }), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'erro': 'Não encontrado',
        'status': 404,
        'detalhes': str(error)
    }), 404

@app.errorhandler(409)
def conflict(error):
    return jsonify({
        'erro': 'Conflito',
        'status': 409,
        'detalhes': str(error)
    }), 409

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'erro': 'Erro interno do servidor',
        'status': 500,
        'detalhes': 'Ocorreu um erro inesperado'
    }), 500

# ==============================================
# Inicialização da aplicação
# ==============================================
if __name__ == '__main__':
    # Inicializa o banco de dados
    with app.app_context():
        init_database(app)
    
    print("🚀 API REST com banco de dados iniciada!")
    print("📊 Banco: SQLite com SQLAlchemy")
    print("🔗 URL: http://localhost:5003")
    print("📧 Admin: admin@biblioteca.com / Senha: admin123")
    print("📧 Cliente: cliente@biblioteca.com / Senha: cliente123")
    
    app.run(debug=True, port=5003)