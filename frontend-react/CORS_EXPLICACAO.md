# 🌐 CORS, OPTIONS e LocalStorage - Guia Completo

## 📖 O que é CORS?

**CORS (Cross-Origin Resource Sharing)** é um mecanismo de segurança implementado pelos navegadores que controla como recursos de um domínio podem ser acessados por scripts executando em outro domínio.

### 🎯 Problema que o CORS Resolve

```javascript
// ❌ Sem CORS, isso seria bloqueado:
// Frontend em localhost:3000 tentando acessar API em localhost:5003
fetch('http://localhost:5003/livros')
  .then(response => response.json())
  .catch(error => console.log('CORS Error:', error));
```

### 🔧 Como Funciona

```
┌─────────────────┐    Request     ┌─────────────────┐
│   Frontend      │──────────────→ │   Backend       │
│ localhost:3000  │                │ localhost:5003  │
│                 │ ←──────────────│                 │
└─────────────────┘   Response     └─────────────────┘
                     + CORS Headers
```

## 🚀 Implementação no Projeto

### Backend (Flask/Python)
```python
from flask_cors import CORS

# ✅ Configuração básica
CORS(app)

# ✅ Configuração avançada (nossa implementação)
CORS(app, 
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True
)
```

### Headers CORS Essenciais
```http
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

## ⚡ Método OPTIONS (Preflight)

### 🎯 O que é Preflight?

O navegador envia automaticamente uma requisição **OPTIONS** antes de certas requisições para verificar permissões.

### 🔍 Quando Acontece?

```javascript
// ✅ Requisições simples (sem preflight)
fetch('http://localhost:5003/livros')

// ❌ Requisições complexas (com preflight)
fetch('http://localhost:5003/livros', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',  // Trigger preflight
    'Authorization': 'Bearer token123'    // Trigger preflight
  },
  body: JSON.stringify({titulo: 'Livro'})
});
```

### 📊 Fluxo Completo

```
1. 🔍 Preflight Request (OPTIONS)
   OPTIONS /livros HTTP/1.1
   Origin: http://localhost:3000
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: content-type,authorization

2. ✅ Preflight Response
   HTTP/1.1 200 OK
   Access-Control-Allow-Origin: http://localhost:3000
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
   Access-Control-Allow-Headers: Content-Type, Authorization

3. 🚀 Actual Request (POST)
   POST /livros HTTP/1.1
   Origin: http://localhost:3000
   Content-Type: application/json
   Authorization: Bearer token123
```

### 🛠️ Testando OPTIONS

```bash
# Terminal
curl -X OPTIONS http://localhost:5003/livros \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type,authorization" \
  -v
```

```javascript
// JavaScript
fetch('http://localhost:5003/livros', { method: 'OPTIONS' })
  .then(response => {
    console.log('Status:', response.status);
    console.log('Headers:', [...response.headers.entries()]);
  });
```

## 💾 LocalStorage - Armazenamento Local

### 🎯 O que é LocalStorage?

O localStorage permite armazenar dados no navegador que persistem entre sessões. É perfeito para salvar tokens de autenticação e configurações do usuário.

### 📱 Uso no Projeto

```javascript
// Salvar token após login
localStorage.setItem('token', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...');
localStorage.setItem('user', JSON.stringify({id: 1, nome: 'João'}));

// Recuperar dados
const token = localStorage.getItem('token');
const user = JSON.parse(localStorage.getItem('user'));

// Remover dados (logout)
localStorage.removeItem('token');
localStorage.removeItem('user');

// Limpar tudo
localStorage.clear();
```

### 🔧 Implementação no Frontend

```javascript
// services/api.js - Interceptor automático
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// App.js - Verificar login salvo
useEffect(() => {
  const savedToken = localStorage.getItem('token');
  const savedUser = localStorage.getItem('user');
  
  if (savedToken && savedUser) {
    setUser(JSON.parse(savedUser));
  }
}, []);

// Login.jsx - Salvar após autenticação
const handleLogin = async (credentials) => {
  const response = await authService.login(credentials);
  
  localStorage.setItem('token', response.token);
  localStorage.setItem('user', JSON.stringify(response.usuario));
  
  onLogin(response.usuario);
};
```

### 🔍 Debug no DevTools

1. **Abra o DevTools** (F12)
2. **Vá para Application tab**
3. **Clique em Local Storage**
4. **Veja os dados salvos** (token, user, etc.)

```javascript
// Console do navegador
console.log('Token:', localStorage.getItem('token'));
console.log('User:', JSON.parse(localStorage.getItem('user')));

// Verificar tamanho
console.log('Storage usado:', JSON.stringify(localStorage).length + ' bytes');
```

## 🚨 Problemas Comuns e Soluções

### 1. **CORS Preflight Failed**
```javascript
// ❌ Problema
fetch('http://localhost:5003/livros', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Custom-Header': 'value'  // Header não permitido
  }
});

// ✅ Solução: Configurar no backend
CORS(app, allow_headers=["Content-Type", "Authorization", "X-Custom-Header"])
```

### 2. **Token Perdido após Refresh**
```javascript
// ❌ Problema: só salvar em variável
let token = 'abc123';

// ✅ Solução: usar localStorage
localStorage.setItem('token', 'abc123');
```

### 3. **Dados Corrompidos no LocalStorage**
```javascript
// ❌ Problema: salvar objeto diretamente
localStorage.setItem('user', userObject); // [object Object]

// ✅ Solução: usar JSON
localStorage.setItem('user', JSON.stringify(userObject));
const user = JSON.parse(localStorage.getItem('user'));
```

## 🎯 Melhores Práticas

### ✅ CORS
1. **Seja específico com origins** - Não use `*` em produção
2. **Configure apenas headers necessários**
3. **Use HTTPS em produção**
4. **Implemente rate limiting**

### ✅ LocalStorage
1. **Sempre use JSON.stringify/parse** para objetos
2. **Verifique se existe antes de usar**
3. **Limpe dados sensíveis no logout**
4. **Cuidado com limite de 5-10MB**
5. **Use try/catch para JSON.parse**

### ✅ OPTIONS
1. **Não bloquear OPTIONS** - Sempre permitir
2. **Retornar headers corretos**
3. **Cache preflight responses** (Access-Control-Max-Age)

## 🧪 Testando na Prática

### 1. **Teste CORS**
```bash
# Teste preflight
curl -X OPTIONS http://localhost:5003/livros \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -v
```

### 2. **Teste LocalStorage**
```javascript
// Console do navegador
localStorage.setItem('test', 'funcionou!');
console.log(localStorage.getItem('test'));
localStorage.removeItem('test');
```

### 3. **Debug CORS no DevTools**
```javascript
// Network tab: procure por:
// - Request headers: Origin, Access-Control-Request-*
// - Response headers: Access-Control-Allow-*
// - Status: 200 (OK) ou 204 (No Content) para OPTIONS
```

## 📚 Resumo Executivo

1. **CORS** = Segurança entre domínios
2. **OPTIONS** = Verificação de permissões (preflight)
3. **LocalStorage** = Dados persistentes no navegador
4. **Configurar CORS específico** para seus domínios
5. **Usar localStorage para token** e dados do usuário
6. **Testar em cenários reais** com diferentes navegadores

---

💡 **Dica**: Use as ferramentas do DevTools para debugar CORS e verificar dados no localStorage! 