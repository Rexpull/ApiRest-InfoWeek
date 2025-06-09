# API REST - Sistema de Biblioteca

Este projeto contém três implementações diferentes de uma API REST para gerenciamento de livros:

## 📁 Estrutura do Projeto

```
api/
├── app_rest_completo.py     # API com HATEOAS completo
├── app_rest_simples.py      # API REST simples (sem HATEOAS)
├── app_rest_db.py          # API REST com banco SQLAlchemy
├── models.py               # Modelos SQLAlchemy
├── database.py             # Configuração do banco
├── requirements.txt        # Dependências Python
└── README.md              # Esta documentação
```

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Escolha uma das APIs

#### API REST Simples (sem HATEOAS)
```bash
python app_rest_simples.py
```
- **Porta:** 5002
- **Banco:** Em memória (listas Python)
- **Features:** CRUD básico, autenticação JWT

#### API REST com Banco de Dados
```bash
python app_rest_db.py
```
- **Porta:** 5003  
- **Banco:** SQLite + SQLAlchemy
- **Features:** CRUD completo, paginação, filtros, relacionamentos

#### API REST Completa com HATEOAS
```bash
python app_rest_completo.py
```
- **Porta:** 5001
- **Banco:** Em memória
- **Features:** HATEOAS, content negotiation, middlewares avançados

## 🛠 Gerenciamento do Banco de Dados (SQLAlchemy)

### Inicializar o banco
```bash
python database.py init
```

### Resetar o banco
```bash
python database.py reset
```

### Ver informações do banco
```bash
python database.py info
```

## 📊 Usuários Padrão

### API Simples
- **Admin:** admin@user.com / admin
- **Cliente:** customer@user.com / customer

### API com Banco
- **Admin:** admin@biblioteca.com / admin123
- **Cliente:** cliente@biblioteca.com / cliente123

## 🔗 Endpoints Principais

### Autenticação
```
POST /login           # Login
POST /register        # Registro (só na versão com banco)
```

### Livros
```
GET    /livros         # Listar livros
POST   /livros         # Criar livro (requer token)
GET    /livros/{id}    # Obter livro específico
PUT    /livros/{id}    # Atualizar livro (requer token)
DELETE /livros/{id}    # Deletar livro (requer token)
GET    /livros/buscar  # Buscar livros (?q=termo)
```

### Administração (apenas versão com banco)
```
GET /usuarios         # Listar usuários (admin)
PUT /usuarios/{id}    # Atualizar usuário (admin)
GET /categorias       # Listar categorias
POST /categorias      # Criar categoria (admin)
GET /stats           # Estatísticas (admin)
```

## 📝 Exemplos de Uso

### Login
```bash
curl -X POST http://localhost:5003/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@biblioteca.com", "password": "admin123"}'
```

### Criar Livro
```bash
curl -X POST http://localhost:5003/livros \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "titulo": "1984",
    "autor": "George Orwell",
    "ano": 1949,
    "genero": "Ficção Científica",
    "descricao": "Distopia clássica"
  }'
```

### Listar Livros com Filtros
```bash
curl "http://localhost:5003/livros?genero=Romance&pagina=1&por_pagina=5"
```

### Buscar Livros
```bash
curl "http://localhost:5003/livros/buscar?q=1984"
```

## 🔧 Diferenças entre as Versões

| Feature | Simples | Com Banco | Completo |
|---------|---------|-----------|----------|
| Banco de dados| Memória | SQLite | Memória |
| HATEOAS             | ❌ | ❌ | ✅ |
| Paginação           | ❌ | ✅ | ❌ |
| Filtros             | ❌ | ✅ | ❌ |
| Registro            | ❌ | ✅ | ❌ |
| Admin panel         | ❌ | ✅ | ❌ |
| Estatísticas        | ❌ | ✅ | ❌ |
| Content negotiation | ❌ | ❌ | ✅ |

## 🏗 Arquitetura

### API Simples
- Flask básico com autenticação JWT
- Dados em listas Python
- Ideal para protótipos e testes

### API com Banco
- SQLAlchemy ORM
- SQLite local
- Relacionamentos entre entidades
- Validações robustas
- Sistema de permissões

### API Completa
- Implementa padrões REST avançados
- HATEOAS (Hypertext Application Language)
- Content negotiation
- Middlewares personalizados

## 🔒 Segurança

- Autenticação JWT
- Hash de senhas (versão com banco)
- Validação de entrada
- Controle de acesso por roles
- CORS habilitado

## 📦 Modelos de Dados (Versão com Banco)

### User
- id, email, password_hash, role, nome
- criado_em, ativo

### Book  
- id, titulo, autor, ano, genero, isbn
- descricao, paginas, disponivel
- criado_em, atualizado_em, criado_por

### Category
- id, nome, descricao, ativa, criado_em

## 🐛 Logs e Debug

Todas as APIs incluem logging detalhado:
- Requisições e respostas
- Queries SQL (versão com banco)
- Erros e exceções

## 🎯 Casos de Uso

- **API Simples:** Prototipagem rápida, demos, testes
- **API com Banco:** Aplicações reais, desenvolvimento completo
- **API Completa:** Estudos de REST, implementações enterprise

## 📧 Suporte

Qualquer dúvida sobre a implementação ou uso das APIs, consulte a documentação inline no código. 