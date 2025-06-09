from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """Modelo para usuários do sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='customer')
    nome = db.Column(db.String(100), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Define a senha do usuário com hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'nome': self.nome,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'ativo': self.ativo
        }
    
    def __repr__(self):
        return f'<User {self.email}>'

class Book(db.Model):
    """Modelo para livros"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    ano = db.Column(db.Integer, nullable=True)
    genero = db.Column(db.String(100), nullable=True)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    paginas = db.Column(db.Integer, nullable=True)
    disponivel = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com usuário que criou o livro
    criado_por = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    criador = db.relationship('User', backref=db.backref('livros_criados', lazy=True))
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'ano': self.ano,
            'genero': self.genero,
            'isbn': self.isbn,
            'descricao': self.descricao,
            'paginas': self.paginas,
            'disponivel': self.disponivel,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
            'criado_por': self.criado_por
        }
    
    def __repr__(self):
        return f'<Book {self.titulo}>'

class Category(db.Model):
    """Modelo para categorias de livros"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ativa = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ativa': self.ativa,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None
        }
    
    def __repr__(self):
        return f'<Category {self.nome}>'
