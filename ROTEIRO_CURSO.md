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

---

### 📌 **PARTE 2: API Simples** (25 min)
**⏰ 00:15 - 00:40**

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

---

### 📌 **PARTE 3: Conceitos JWT** (15 min)
**⏰ 00:40 - 00:55**

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

---

### 📌 **PARTE 4: API com Banco de Dados** (25 min)
**⏰ 00:55 - 01:20**

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

---

### 📌 **PARTE 5: CORS e OPTIONS** (10 min)
**⏰ 01:20 - 01:30**

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

#### Testando OPTIONS (3 min)
```bash
# Requisição preflight
curl -X OPTIONS http://localhost:5003/livros \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v

# Mostrar headers de resposta
```

---

## 🎨 BLOCO 2: Frontend + Integração (80 minutos)

### 📌 **PARTE 6: Setup Frontend React** (15 min)
**⏰ 01:30 - 01:45**

#### Criando o Projeto React (8 min)
```bash
# Se já não existir
npx create-react-app frontend-react
cd frontend-react

# Instalar dependências
npm install axios tailwindcss

# Configurar Tailwind
npx tailwindcss init -p
```

#### Estrutura do Projeto (7 min)
```
frontend-react/
├── src/
│   ├── components/
│   │   ├── Login.jsx          # Componente de login
│   │   ├── Dashboard.jsx      # Dashboard principal
│   │   ├── BookCard.jsx       # Card do livro
│   │   └── BookForm.jsx       # Formulário de livro
│   ├── services/
│   │   └── api.js            # Configuração Axios
│   ├── App.js                # Componente principal
│   └── index.css             # Estilos Tailwind
```

---

### 📌 **PARTE 7: Configuração da API** (10 min)
**⏰ 01:45 - 01:55**

#### Serviço de API (5 min)
```javascript
// Mostrar services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5003';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para token automático
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

#### Serviços Específicos (5 min)
```javascript
// authService
export const authService = {
  async login(email, password) {
    const response = await api.post('/login', { email, password });
    return response.data;
  }
};

// booksService  
export const booksService = {
  async getBooks(page = 1, filters = {}) {
    const params = { pagina: page, por_pagina: 12, ...filters };
    const response = await api.get('/livros', { params });
    return response.data;
  }
};
```

---

### 📌 **PARTE 8: Componente de Login** (15 min)
**⏰ 01:55 - 02:10**

#### Criando o Login (8 min)
```jsx
// Mostrar Login.jsx
import React, { useState } from 'react';
import { authService } from '../services/api';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const data = await authService.login(email, password);
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.usuario));
      onLogin(data.usuario);
    } catch (error) {
      alert('Erro ao fazer login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-6">Login</h2>
        {/* ... inputs ... */}
      </form>
    </div>
  );
};
```

#### Testando o Login (7 min)
- Executar `npm start`
- Demonstrar login funcionando
- Mostrar token no localStorage
- Demonstrar erro de credenciais inválidas

---

### 📌 **PARTE 9: Dashboard de Livros** (25 min)
**⏰ 02:10 - 02:35**

#### Componente Dashboard (10 min)
```jsx
// Mostrar Dashboard.jsx
const Dashboard = ({ user, onLogout }) => {
  const [livros, setLivros] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    try {
      const data = await booksService.getBooks();
      setLivros(data.livros);
    } catch (error) {
      console.error('Erro ao carregar livros:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">📚 Biblioteca</h1>
          <div className="flex items-center space-x-4">
            <span>Olá, {user.nome}</span>
            <button onClick={onLogout}>Sair</button>
          </div>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-8">
        {/* Search bar */}
        {/* Books grid */}
      </main>
    </div>
  );
};
```

#### Componente BookCard (8 min)
```jsx
// Mostrar BookCard.jsx
const BookCard = ({ livro, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold mb-2">{livro.titulo}</h3>
      <p className="text-gray-600 mb-1">📖 {livro.autor}</p>
      <p className="text-gray-500 mb-1">📅 {livro.ano}</p>
      <p className="text-gray-500 mb-1">🏷️ {livro.genero}</p>
      
      <div className="flex space-x-2 mt-4">
        <button 
          onClick={() => onEdit(livro)}
          className="bg-blue-500 text-white px-3 py-1 rounded"
        >
          Editar
        </button>
        <button 
          onClick={() => onDelete(livro.id)}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Excluir
        </button>
      </div>
    </div>
  );
};
```

#### Testando Interface (7 min)
- Mostrar livros carregando da API
- Demonstrar responsividade (mobile/desktop)
- Testar busca
- Mostrar loading states

---

### 📌 **PARTE 10: CRUD Frontend** (15 min)
**⏰ 02:35 - 02:50**

#### Formulário de Livro (8 min)
```jsx
// Mostrar BookForm.jsx
const BookForm = ({ livro, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    titulo: livro?.titulo || '',
    autor: livro?.autor || '',
    ano: livro?.ano || '',
    genero: livro?.genero || '',
    descricao: livro?.descricao || ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (livro) {
        await booksService.updateBook(livro.id, formData);
      } else {
        await booksService.createBook(formData);
      }
      onSave();
    } catch (error) {
      alert('Erro ao salvar livro');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded-lg w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">
          {livro ? 'Editar Livro' : 'Novo Livro'}
        </h2>
        <form onSubmit={handleSubmit}>
          {/* ... inputs ... */}
        </form>
      </div>
    </div>
  );
};
```

#### Integrando CRUD (4 min)
- Criar livro via formulário
- Editar livro existente
- Deletar com confirmação
- Recarregar lista automaticamente

#### Cache e Performance (3 min)
```javascript
// Demonstrar cache simples
const cache = new Map();

const getCachedBooks = async () => {
  const cached = cache.get('books');
  if (cached && Date.now() - cached.timestamp < 5 * 60 * 1000) {
    return cached.data;
  }
  
  const data = await booksService.getBooks();
  cache.set('books', { data, timestamp: Date.now() });
  return data;
};
```

---

## 🎯 **WRAP-UP FINAL** (10 min)
**⏰ 02:50 - 03:00**

### Recapitulação (5 min)
1. ✅ **API REST** - 3 versões diferentes
2. ✅ **Autenticação JWT** - Token seguro
3. ✅ **Banco de Dados** - SQLAlchemy + SQLite
4. ✅ **Frontend React** - Interface moderna
5. ✅ **Integração** - API + Frontend funcionando

### Próximos Passos (3 min)
- Deploy em produção
- Testes automatizados
- Documentação com Swagger
- Cache avançado
- WebSockets para real-time

### Q&A (2 min)
- Dúvidas dos alunos
- Sugestões de melhorias

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

## ⏱️ **CRONOGRAMA RESUMIDO**

| Tempo | Tópico | Duração |
|-------|--------|---------|
| 00:00-00:15 | Introdução + Setup | 15min |
| 00:15-00:40 | API Simples + Postman | 25min |
| 00:40-00:55 | JWT Conceitos | 15min |
| 00:55-01:20 | API com Banco | 25min |
| 01:20-01:30 | CORS + OPTIONS | 10min |
| 01:30-01:45 | Setup React | 15min |
| 01:45-01:55 | Config API | 10min |
| 01:55-02:10 | Login Component | 15min |
| 02:10-02:35 | Dashboard + Cards | 25min |
| 02:35-02:50 | CRUD Frontend | 15min |
| 02:50-03:00 | Wrap-up + Q&A | 10min |

**TOTAL: 3h00min (com 10min de buffer)**

---

💡 **Dica para o Instrutor:** Mantenha o Postman aberto durante toda a aula para demonstrações rápidas da API enquanto desenvolve o frontend! 