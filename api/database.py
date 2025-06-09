import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Book, Category

def create_app():
    """Factory para criar a aplicação Flask com configuração do banco"""
    app = Flask(__name__)
    
    # Configuração do banco de dados SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "biblioteca.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # Log das queries SQL
    
    # Inicializa o banco com a aplicação
    db.init_app(app)
    
    return app

def init_database(app):
    """Inicializa o banco de dados e cria as tabelas"""
    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        
        # Verifica se já existem usuários
        if User.query.count() == 0:
            create_default_users()
        
        print("✅ Banco de dados inicializado com sucesso!")

def create_default_users():
    """Cria usuários padrão para testes"""
    # Usuário administrador
    admin = User(
        email='admin@biblioteca.com',
        role='admin',
        nome='Administrador do Sistema'
    )
    admin.set_password('admin123')
    
    # Usuário cliente
    cliente = User(
        email='cliente@biblioteca.com', 
        role='customer',
        nome='Cliente Teste'
    )
    cliente.set_password('cliente123')
    
    # Adiciona os usuários ao banco
    db.session.add(admin)
    db.session.add(cliente)
    
    # Cria algumas categorias padrão
    categorias = [
        Category(nome='Ficção', descricao='Livros de ficção em geral'),
        Category(nome='Romance', descricao='Livros românticos'),
        Category(nome='Mistério', descricao='Livros de mistério e suspense'),
        Category(nome='Biografia', descricao='Biografias e autobiografias'),
        Category(nome='Tecnologia', descricao='Livros sobre tecnologia'),
        Category(nome='História', descricao='Livros históricos'),
    ]
    
    for categoria in categorias:
        db.session.add(categoria)
    
    # Adiciona alguns livros de exemplo
    livros_exemplo = [
        Book(
            titulo='Dom Casmurro',
            autor='Machado de Assis',
            ano=1899,
            genero='Romance',
            isbn='978-85-359-0277-5',
            descricao='Clássico da literatura brasileira',
            paginas=256,
            criado_por=1
        ),
        Book(
            titulo='O Cortiço',
            autor='Aluísio Azevedo',
            ano=1890,
            genero='Naturalismo',
            isbn='978-85-359-0123-4',
            descricao='Romance naturalista brasileiro',
            paginas=304,
            criado_por=1
        ),
        Book(
            titulo='Clean Code',
            autor='Robert C. Martin',
            ano=2008,
            genero='Tecnologia',
            isbn='978-0-13-235088-4',
            descricao='Manual de boas práticas para desenvolvimento de software',
            paginas=464,
            criado_por=1
        )
    ]
    
    for livro in livros_exemplo:
        db.session.add(livro)
    
    # Salva no banco
    try:
        db.session.commit()
        print("✅ Dados padrão criados com sucesso!")
        print("📧 Admin: admin@biblioteca.com / Senha: admin123")
        print("📧 Cliente: cliente@biblioteca.com / Senha: cliente123")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao criar dados padrão: {e}")

def reset_database(app):
    """Reseta o banco de dados (apaga tudo e recria)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_default_users()
        print("🔄 Banco de dados resetado com sucesso!")

def get_database_info(app):
    """Retorna informações sobre o banco de dados"""
    with app.app_context():
        info = {
            'total_usuarios': User.query.count(),
            'total_livros': Book.query.count(),
            'total_categorias': Category.query.count(),
            'usuarios_ativos': User.query.filter_by(ativo=True).count(),
            'livros_disponiveis': Book.query.filter_by(disponivel=True).count()
        }
        return info

# Utilitários para desenvolvimento
if __name__ == '__main__':
    app = create_app()
    
    import sys
    
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == 'init':
            init_database(app)
        elif comando == 'reset':
            reset_database(app)
        elif comando == 'info':
            info = get_database_info(app)
            print("📊 Informações do Banco de Dados:")
            for chave, valor in info.items():
                print(f"   {chave}: {valor}")
        else:
            print("Comandos disponíveis:")
            print("  python database.py init  - Inicializa o banco")
            print("  python database.py reset - Reseta o banco")
            print("  python database.py info  - Mostra informações")
    else:
        print("Uso: python database.py [init|reset|info]")
