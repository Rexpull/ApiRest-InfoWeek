# 🔑 JWT (JSON Web Token) - Guia Completo para Alunos

## 📖 O que é JWT?

**JWT (JSON Web Token)** é um padrão aberto (RFC 7519) que define uma forma compacta e segura de transmitir informações entre as partes como um objeto JSON. Este token pode ser verificado e é confiável pois é assinado digitalmente.

## 🏗️ Estrutura do JWT

Um JWT é composto por **3 partes** separadas por pontos (`.`):

```
HEADER.PAYLOAD.SIGNATURE
```

### 1. 🎯 Header (Cabeçalho)
Contém informações sobre como o JWT deve ser verificado:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- **alg**: Algoritmo usado para assinar o token (HS256, RS256, etc.)
- **typ**: Tipo do token (sempre "JWT")

### 2. 📦 Payload (Dados)
Contém as informações (claims) que queremos transmitir:

```json
{
  "sub": "123",           // Subject (ID do usuário)
  "email": "user@test.com", // Email do usuário
  "role": "admin",        // Papel/função do usuário
  "exp": 1640995200,     // Expiration time (timestamp)
  "iat": 1640991600      // Issued at (timestamp)
}
```

#### Types de Claims:
- **Registered Claims**: `sub`, `exp`, `iat`, `iss`, `aud`
- **Public Claims**: Definidos publicamente
- **Private Claims**: Personalizados entre as partes

### 3. 🔐 Signature (Assinatura)
Garante que o token não foi alterado:

```javascript
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

## 🔄 Fluxo de Autenticação JWT

### 1. **Login do Usuário**
```
Cliente → POST /login { email, password } → Servidor
```

### 2. **Validação e Geração do Token**
```python
# No servidor (Python/Flask)
if usuario.check_password(password):
    token = jwt.encode({
        'sub': usuario.id,
        'role': usuario.role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return {'token': token}
```

### 3. **Retorno do Token**
```
Servidor → { token: "eyJhbGciOiJIUzI1NiIs..." } → Cliente
```

### 4. **Armazenamento no Cliente**
```javascript
// No navegador
localStorage.setItem('token', data.token);
```

### 5. **Uso em Requisições Protegidas**
```
Cliente → GET /livros 
        → Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
        → Servidor
```

### 6. **Validação no Servidor**
```python
# Decorator para verificar token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'erro': 'Token necessário'}, 401
            
        try:
            token = token.split(' ')[1]  # Remove "Bearer "
            decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(decoded['sub'])
        except:
            return {'erro': 'Token inválido'}, 401
            
        return f(current_user, *args, **kwargs)
    return decorated
```

## 💡 Vantagens do JWT

### ✅ **Stateless (Sem Estado)**
- Servidor não precisa armazenar sessões
- Escala bem horizontalmente
- Não há necessidade de banco de sessões

### ✅ **Autocontido**
- Toda informação necessária está no token
- Reduz consultas ao banco de dados
- Funciona em arquiteturas distribuídas

### ✅ **Portável**
- Funciona em diferentes domínios
- Ideal para APIs REST
- Suporte nativo em muitas linguagens

### ✅ **Flexível**
- Pode incluir qualquer informação JSON
- Suporta diferentes algoritmos de assinatura
- Extensível com claims personalizados

## ⚠️ Cuidados e Segurança

### 🔒 **Chave Secreta**
```python
# ❌ NUNCA faça isso em produção
SECRET_KEY = "123"

# ✅ Use uma chave forte
SECRET_KEY = "minha_chave_super_secreta_com_256_bits_pelo_menos"

# ✅ Melhor ainda, use variáveis de ambiente
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
```

### ⏰ **Tempo de Expiração**
```python
# ✅ Sempre defina um tempo de expiração
token = jwt.encode({
    'sub': user.id,
    'exp': datetime.utcnow() + timedelta(hours=1)  # 1 hora
}, SECRET_KEY)
```

### 🏪 **Armazenamento no Cliente**
```javascript
// ✅ localStorage (mais comum)
localStorage.setItem('token', token);

// ✅ sessionStorage (mais seguro)
sessionStorage.setItem('token', token);

// ❌ Evite cookies simples sem httpOnly
document.cookie = `token=${token}`;
```

### 🔍 **Validação Completa**
```python
def validate_token(token):
    try:
        # Verifica assinatura e expiração
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        
        # Verifica se usuário ainda existe
        user = User.query.get(decoded['sub'])
        if not user or not user.ativo:
            return None
            
        return user
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido
```

## 🛠️ Implementação Prática

### Frontend (JavaScript)
```javascript
class AuthService {
    constructor() {
        this.token = localStorage.getItem('token');
    }
    
    async login(email, password) {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            this.token = data.token;
            localStorage.setItem('token', this.token);
            return data;
        } else {
            throw new Error(data.erro);
        }
    }
    
    async makeAuthenticatedRequest(url, options = {}) {
        return fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        });
    }
    
    logout() {
        this.token = null;
        localStorage.removeItem('token');
    }
    
    isAuthenticated() {
        if (!this.token) return false;
        
        try {
            const payload = JSON.parse(atob(this.token.split('.')[1]));
            return payload.exp > Date.now() / 1000;
        } catch {
            return false;
        }
    }
}
```

### Backend (Python/Flask)
```python
from functools import wraps
import jwt
from datetime import datetime, timedelta

def create_token(user):
    payload = {
        'sub': user.id,
        'email': user.email,
        'role': user.role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'erro': 'Token de autorização necessário'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer TOKEN
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(decoded['sub'])
            
            if not current_user:
                return jsonify({'erro': 'Usuário não encontrado'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/protected')
@token_required
def protected_route(current_user):
    return jsonify({
        'mensagem': 'Acesso autorizado',
        'usuario': current_user.email
    })
```

## 🧪 Testando JWT

### 1. **Decodificar Manualmente**
```javascript
// No console do navegador
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";
const parts = token.split('.');

// Decodifica o header
const header = JSON.parse(atob(parts[0]));
console.log('Header:', header);

// Decodifica o payload
const payload = JSON.parse(atob(parts[1]));
console.log('Payload:', payload);
console.log('Expira em:', new Date(payload.exp * 1000));
```

### 2. **Verificar Expiração**
```javascript
function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.exp < Date.now() / 1000;
    } catch {
        return true;
    }
}
```

### 3. **Debug no Servidor**
```python
@app.route('/debug-token')
@token_required
def debug_token(current_user):
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    
    # Decodifica sem verificar (apenas para debug)
    decoded = jwt.decode(token, verify=False)
    
    return jsonify({
        'token_info': decoded,
        'current_user': current_user.to_dict(),
        'is_expired': decoded['exp'] < time.time()
    })
```

## 🔗 Ferramentas Úteis

1. **[jwt.io](https://jwt.io/)** - Decodificar e validar tokens online
2. **[JWT Debugger](https://jwt.ms/)** - Outra ferramenta de debug
3. **Postman** - Testar APIs com tokens JWT
4. **Console do Navegador** - Inspecionar tokens em runtime

## 📝 Resumo para Memorizar

1. **JWT = Header + Payload + Signature**
2. **Sempre definir expiração (`exp`)**
3. **Usar chave secreta forte**
4. **Validar token em toda requisição protegida**
5. **Armazenar no localStorage/sessionStorage**
6. **Enviar no header Authorization: Bearer TOKEN**
7. **JWT é stateless - não precisa de sessão no servidor**
8. **Verificar se usuário ainda existe/está ativo**

## 🎯 Exercícios Práticos

1. **Criar um sistema de login simples**
2. **Implementar refresh token**
3. **Adicionar diferentes roles (admin, user)**
4. **Criar middleware de autorização**
5. **Testar cenários de token expirado**
6. **Implementar logout automático**

---

💡 **Dica**: Use sempre o frontend criado neste projeto para visualizar na prática como o JWT funciona na seção "JWT Info"! 