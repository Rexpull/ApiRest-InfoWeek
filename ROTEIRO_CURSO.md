# 🎬 ROTEIRO DO MINI-CURSO: API REST + Frontend React

**Duração Total:** 2h50min (170 minutos)  
**Objetivo:** Ensinar desenvolvimento completo de API REST e Frontend integrado

---

## 📋 ESTRUTURA GERAL DO CURSO

### 🎯 **BLOCO 1: APIs REST** (1h30min - 90min)
- API Simples + Postman
- API com Banco de Dados
- Conceitos REST e JWT

### 🎯 **BLOCO 2: Frontend + Integração** (1h20min - 80min)
- React + Tailwind
- Integração com API
- CORS, Cache e Boas Práticas

---

## 🚀 BLOCO 1: APIs REST (90 minutos)

### 📌 **PARTE 1: Introdução e Setup** (15 min)
**⏰ 00:00 - 00:15**

#### Objetivos da Aula (3 min)
- Apresentar o que será construído
- Mostrar resultado final funcionando
- Explicar estrutura do projeto

#### Setup do Ambiente (7 min)
```bash
# Clonar/preparar projeto
pip install -r requirements.txt

# Mostrar estrutura de pastas
api/
├── app_rest_simples.py      # Começaremos aqui
├── app_rest_db.py          # Evoluiremos para aqui
├── models.py               # Modelos do banco
└── database.py             # Configuração DB
```

#### Introdução ao REST (5 min)
- O que é uma API REST?
- HTTP Methods (GET, POST, PUT, DELETE)
- Status Codes importantes
- JSON como formato de dados

#### **🎯 DINÂMICA 1: Quiz REST + Exercício URLs** (15 min)
**⏰ 00:15 - 00:30**
- Quiz "REST ou não REST?" com placas (5min)
- Exercício em grupos: criar URLs para Blog Posts (10min)
- **Objetivo:** Fixar conceitos antes da prática

---

### 📌 **PARTE 2: API Simples** (25 min)
**⏰ 00:30 - 00:55**

#### Analisando o Código (10 min)
```python
# Mostrar app_rest_simples.py
from flask import Flask, jsonify, request
import jwt

# Explicar estrutura básica:
# - Flask app
# - Dados em memória (listas)
# - Autenticação JWT
# - Endpoints CRUD
```

#### Executando a API (5 min)
```bash
python app_rest_simples.py
# Porta 5002
# Mostrar logs no terminal
```

#### Testando no Postman (10 min)
```bash
# 1. Verificar status da API
GET http://localhost:5002/

# 2. Login para obter token
POST http://localhost:5002/login
{
  "email": "admin@user.com",
  "password": "admin"
}

# 3. Listar livros (vazio inicialmente)
GET http://localhost:5002/livros

# 4. Criar primeiro livro
POST http://localhost:5002/livros
Authorization: Bearer TOKEN_AQUI
{
  "titulo": "1984",
  "autor": "George Orwell",
  "ano": 1949,
  "genero": "Ficção Científica"
}

# 5. Listar novamente (agora com 1 livro)
GET http://localhost:5002/livros
```

#### Demonstrar CRUD Completo (5 min)
- Criar mais livros
- Editar um livro (PUT)
- Deletar um livro (DELETE)
- Buscar livros

#### **🎯 DINÂMICA 2: Desafio "Sua Primeira API"** (25 min)
**⏰ 00:55 - 01:20**
- Cada aluno cria entidade FILMES (15min)
- Apresentações rápidas (10min)
- **Objetivo:** Aplicar conhecimento na prática

---

### 📌 **PARTE 3: Conceitos JWT** (20 min)
**⏰ 01:20 - 01:40**

#### O que é JWT? (5 min)
- Token de autenticação
- Estrutura: Header.Payload.Signature
- Stateless (sem sessão no servidor)

#### Demonstração Prática (5 min)
```javascript
// No console do navegador ou jwt.io
const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...";

// Decodificar header
const header = JSON.parse(atob(token.split('.')[0]));
console.log('Header:', header);

// Decodificar payload  
const payload = JSON.parse(atob(token.split('.')[1]));
console.log('Payload:', payload);
console.log('Expira em:', new Date(payload.exp * 1000));
```

#### Configuração JWT Dinâmica (5 min)
```bash
# Demonstrar novo endpoint
POST http://localhost:5002/jwt/configure
{
  "secret": "minha_chave_super_secreta_256_bits"
}

# Verificar configuração
GET http://localhost:5002/jwt/info
```

#### **🎯 DINÂMICA 3: JWT Detective + Token Master** (15 min)
**⏰ 01:40 - 01:55**
- Quiz interativo decodificando JWT (8min)
- Desafio código em duplas (7min)
- **Objetivo:** Dominar JWT na prática

---

### 📌 **PARTE 4: API com Banco de Dados** (40 min)
**⏰ 01:55 - 02:35**

#### Inicializando o Banco (5 min)
```bash
# Parar API simples
# Executar API com banco
python app_rest_db.py
# Porta 5003

# Mostrar arquivo database.db criado
# Explicar SQLAlchemy + SQLite
```

#### Diferenças da API com Banco (8 min)
```python
# Mostrar models.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # ... mais campos

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    # ... relacionamentos
```

#### Testando Funcionalidades Avançadas (12 min)
```bash
# 1. Login com usuários do banco
POST http://localhost:5003/login
{
  "email": "admin@biblioteca.com",
  "password": "admin123"
}

# 2. Registro de novo usuário
POST http://localhost:5003/register
{
  "nome": "João Silva",
  "email": "joao@teste.com", 
  "password": "senha123"
}

# 3. Criar livro com mais campos
POST http://localhost:5003/livros
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano": 1899,
  "genero": "Romance",
  "isbn": "978-85-359-0277-5",
  "descricao": "Clássico da literatura brasileira",
  "paginas": 256
}

# 4. Testar paginação
GET http://localhost:5003/livros?pagina=1&por_pagina=5

# 5. Testar filtros
GET http://localhost:5003/livros?autor=machado&genero=romance

# 6. Buscar livros
GET http://localhost:5003/livros/buscar?q=casmurro

# 7. Estatísticas (admin)
GET http://localhost:5003/stats
```

#### **🎯 DINÂMICA 4: Biblioteca Personalizada** (20 min)
**⏰ 02:15 - 02:35**
- Duplas implementam melhorias na API (15min)
- Apresentações no Postman (5min)
- **Objetivo:** Expandir conhecimento SQLAlchemy

---

### 📌 **PARTE 5: CORS e OPTIONS** (15 min)
**⏰ 02:35 - 02:50**

#### Problema do CORS (3 min)
- Explicar Same-Origin Policy
- Por que acontece entre localhost:3000 e localhost:5003
- Demonstrar erro no DevTools

#### Configuração CORS (4 min)
```python
# Mostrar configuração na API
CORS(app, 
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True
)
```

#### Testando OPTIONS (4 min)
```bash
# Requisição preflight
curl -X OPTIONS http://localhost:5003/livros \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Mostrar headers de resposta
```

#### **🎯 DINÂMICA 5: CORS na Prática** (5 min)
**⏰ 02:45 - 02:50**
- Experiência guiada de erro CORS
- **Objetivo:** Entender CORS visceralmente

---

## 🎨 BLOCO 2: Frontend + Integração (10 minutos)

### 📌 **PARTE 6: Setup Frontend React** (10 min)
**⏰ 02:50 - 03:00**

#### **🎯 RESUMO FINAL** (5 min)
- Mostrar sistema funcionando completo
- Recapitular conceitos principais
- Próximos passos de estudo

#### **🎯 DINÂMICA 6: Quiz Final "Mestre das APIs"** (5 min)
- 4 rounds rápidos com toda turma
- Entrega de certificados simbólicos
- **Objetivo:** Consolidar aprendizado
- Mostrar token no localStorage
- Demonstrar erro de credenciais inválidas

---

## 📚 **MATERIAIS DE APOIO**

### 🔗 **Links Importantes**
- `POSTMAN_DEBUG_GUIDE.md` - Guia completo de testes
- `JWT_EXPLICACAO.md` - Documentação detalhada sobre JWT
- `CORS_EXPLICACAO.md` - CORS, OPTIONS e Cache
- Repositório GitHub com código completo

### 📁 **Arquivos para Download**
- Collection do Postman
- Código fonte completo
- Slides da apresentação
- Exercícios práticos

### 🎓 **Certificado**
- Quiz final (10 perguntas)
- Projeto prático entregue
- Certificado de conclusão

---

## ⏱️ **CRONOGRAMA RESUMIDO COM DINÂMICAS**

| Tempo | Tópico | Dinâmica | Duração |
|-------|--------|----------|---------|
| 00:00-00:15 | Introdução + Setup | - | 15min |
| 00:15-00:30 | **🎯 Quiz REST + URLs** | Placas + Grupos | 15min |
| 00:30-00:55 | API Simples + Postman | - | 25min |
| 00:55-01:20 | **🎯 Desafio API Filmes** | Individual | 25min |
| 01:20-01:40 | JWT Conceitos | - | 20min |
| 01:40-01:55 | **🎯 JWT Detective** | Interativo | 15min |
| 01:55-02:15 | API com Banco | - | 20min |
| 02:15-02:35 | **🎯 Biblioteca Personalizada** | Duplas | 20min |
| 02:35-02:50 | CORS + **🎯 Demo CORS** | Experiência | 15min |
| 02:50-03:00 | **🎯 Quiz Final + Wrap-up** | Competitivo | 10min |

**TOTAL: 3h00min | DINÂMICAS: 110min (61% do curso)**

---

💡 **Dica para o Instrutor:** Mantenha o Postman aberto durante toda a aula para demonstrações rápidas da API enquanto desenvolve o frontend! 