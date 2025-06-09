# 🌐 CORS, OPTIONS e Cache - Guia Completo

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

## 💾 Cache - Estratégias e Implementação

### 🎯 Tipos de Cache

#### 1. **Cache do Navegador (Browser Cache)**
```javascript
// Headers para controlar cache
fetch('/livros', {
  headers: {
    'Cache-Control': 'no-cache',      // Sempre revalidar
    'Cache-Control': 'max-age=3600',  // Cache por 1 hora
    'Cache-Control': 'no-store'       // Nunca armazenar
  }
});
```

#### 2. **Cache da API (Server-Side)**
```python
from flask import make_response
from datetime import datetime, timedelta

@app.route('/livros')
def listar_livros():
    livros = get_livros()
    response = make_response(jsonify(livros))
    
    # Cache por 5 minutos
    response.headers['Cache-Control'] = 'public, max-age=300'
    response.headers['ETag'] = generate_etag(livros)
    response.headers['Last-Modified'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    return response
```

#### 3. **Cache de Aplicação (Frontend)**
```javascript
class CacheService {
  constructor() {
    this.cache = new Map();
    this.ttl = 5 * 60 * 1000; // 5 minutos
  }
  
  set(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
  
  get(key) {
    const item = this.cache.get(key);
    if (!item) return null;
    
    if (Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }
    
    return item.data;
  }
  
  clear() {
    this.cache.clear();
  }
}

// Uso prático
const cache = new CacheService();

async function getLivros() {
  const cached = cache.get('livros');
  if (cached) {
    console.log('📦 Dados do cache');
    return cached;
  }
  
  console.log('🌐 Buscando na API');
  const response = await fetch('/livros');
  const data = await response.json();
  
  cache.set('livros', data);
  return data;
}
```

### 🔄 Cache com React Query / SWR

```javascript
// React Query
import { useQuery } from 'react-query';

function useBooks() {
  return useQuery(
    'books',
    () => fetch('/livros').then(res => res.json()),
    {
      staleTime: 5 * 60 * 1000,     // 5 minutos fresh
      cacheTime: 10 * 60 * 1000,    // 10 minutos no cache
      refetchOnWindowFocus: false,   // Não recarregar ao focar janela
    }
  );
}

// SWR
import useSWR from 'swr';

function useBooks() {
  return useSWR('/livros', fetcher, {
    refreshInterval: 30000,         // Atualiza a cada 30s
    revalidateOnFocus: false,       // Não revalidar ao focar
    dedupingInterval: 2000,         // Dedupe requests por 2s
  });
}
```

### 📱 Cache no LocalStorage

```javascript
class LocalStorageCache {
  constructor(prefix = 'app_cache_') {
    this.prefix = prefix;
  }
  
  set(key, data, ttlMinutes = 60) {
    const item = {
      data,
      timestamp: Date.now(),
      ttl: ttlMinutes * 60 * 1000
    };
    
    localStorage.setItem(
      this.prefix + key, 
      JSON.stringify(item)
    );
  }
  
  get(key) {
    try {
      const item = JSON.parse(
        localStorage.getItem(this.prefix + key)
      );
      
      if (!item) return null;
      
      if (Date.now() - item.timestamp > item.ttl) {
        this.remove(key);
        return null;
      }
      
      return item.data;
    } catch {
      return null;
    }
  }
  
  remove(key) {
    localStorage.removeItem(this.prefix + key);
  }
  
  clear() {
    Object.keys(localStorage)
      .filter(key => key.startsWith(this.prefix))
      .forEach(key => localStorage.removeItem(key));
  }
}

// Uso
const cache = new LocalStorageCache();

// Salvar
cache.set('user_profile', userData, 30); // 30 minutos

// Recuperar
const profile = cache.get('user_profile');
```

## 🔧 Estratégias Avançadas

### 1. **Cache Invalidation (Invalidação)**

```javascript
class SmartCache {
  constructor() {
    this.cache = new Map();
    this.dependencies = new Map();
  }
  
  set(key, data, dependencies = []) {
    this.cache.set(key, data);
    
    // Mapeia dependências
    dependencies.forEach(dep => {
      if (!this.dependencies.has(dep)) {
        this.dependencies.set(dep, new Set());
      }
      this.dependencies.get(dep).add(key);
    });
  }
  
  invalidate(dependency) {
    const keysToInvalidate = this.dependencies.get(dependency);
    if (keysToInvalidate) {
      keysToInvalidate.forEach(key => {
        this.cache.delete(key);
      });
      this.dependencies.delete(dependency);
    }
  }
}

// Uso
const smartCache = new SmartCache();

// Cache com dependências
smartCache.set('livros_lista', livros, ['livros']);
smartCache.set('livro_123', livro, ['livros', 'livro_123']);

// Quando um livro é editado
smartCache.invalidate('livro_123'); // Remove apenas este livro
smartCache.invalidate('livros');     // Remove listas de livros
```

### 2. **Cache com ETags**

```javascript
class ETagCache {
  constructor() {
    this.cache = new Map();
  }
  
  async fetch(url) {
    const cached = this.cache.get(url);
    
    const headers = {};
    if (cached?.etag) {
      headers['If-None-Match'] = cached.etag;
    }
    
    const response = await fetch(url, { headers });
    
    if (response.status === 304) {
      // Não modificado, usa cache
      return cached.data;
    }
    
    const data = await response.json();
    const etag = response.headers.get('ETag');
    
    if (etag) {
      this.cache.set(url, { data, etag });
    }
    
    return data;
  }
}
```

### 3. **Cache Background Refresh**

```javascript
class BackgroundCache {
  constructor() {
    this.cache = new Map();
    this.refreshPromises = new Map();
  }
  
  async get(key, fetcher, ttl = 300000) { // 5 min default
    const cached = this.cache.get(key);
    const now = Date.now();
    
    // Se tem cache válido, retorna imediatamente
    if (cached && now - cached.timestamp < ttl) {
      return cached.data;
    }
    
    // Se tem cache expirado mas ainda usável
    if (cached && now - cached.timestamp < ttl * 2) {
      // Retorna cache antigo e atualiza em background
      this.refreshInBackground(key, fetcher);
      return cached.data;
    }
    
    // Cache muito antigo ou inexistente, busca agora
    return this.refresh(key, fetcher);
  }
  
  async refreshInBackground(key, fetcher) {
    if (this.refreshPromises.has(key)) {
      return; // Já está atualizando
    }
    
    const promise = this.refresh(key, fetcher);
    this.refreshPromises.set(key, promise);
    
    try {
      await promise;
    } finally {
      this.refreshPromises.delete(key);
    }
  }
  
  async refresh(key, fetcher) {
    try {
      const data = await fetcher();
      this.cache.set(key, {
        data,
        timestamp: Date.now()
      });
      return data;
    } catch (error) {
      console.error('Cache refresh failed:', error);
      throw error;
    }
  }
}
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

### 2. **Cache Stale (Desatualizado)**
```javascript
// ❌ Problema: Dados antigos após update
const updateBook = async (id, data) => {
  await api.put(`/livros/${id}`, data);
  // Cache ainda tem dados antigos!
};

// ✅ Solução: Invalidar cache
const updateBook = async (id, data) => {
  await api.put(`/livros/${id}`, data);
  cache.invalidate('livros');
  cache.invalidate(`livro_${id}`);
};
```

### 3. **Memory Leaks em Cache**
```javascript
// ❌ Problema: Cache crescendo infinitamente
class BadCache {
  constructor() {
    this.cache = new Map(); // Nunca limpa!
  }
}

// ✅ Solução: LRU Cache
class LRUCache {
  constructor(maxSize = 100) {
    this.maxSize = maxSize;
    this.cache = new Map();
  }
  
  set(key, value) {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
  
  get(key) {
    if (this.cache.has(key)) {
      const value = this.cache.get(key);
      this.cache.delete(key);
      this.cache.set(key, value); // Move to end
      return value;
    }
    return null;
  }
}
```

## 🎯 Melhores Práticas

### ✅ CORS
1. **Seja específico com origins** - Não use `*` em produção
2. **Configure apenas headers necessários**
3. **Use HTTPS em produção**
4. **Implemente rate limiting**

### ✅ Cache
1. **Defina TTL apropriado** - Dados dinâmicos = TTL baixo
2. **Invalide ao modificar dados**
3. **Use cache em layers** (Browser → App → Server)
4. **Monitore uso de memória**
5. **Implemente fallbacks para cache miss**

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

# Teste request real
curl -X POST http://localhost:5003/livros \
  -H "Origin: http://localhost:3000" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Teste"}' \
  -v
```

### 2. **Teste Cache**
```javascript
// Console do navegador
const testCache = async () => {
  console.time('First Request');
  await fetch('/livros');
  console.timeEnd('First Request');
  
  console.time('Cached Request');
  await fetch('/livros');
  console.timeEnd('Cached Request');
};

testCache();
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
3. **Cache** = Performance e experiência do usuário
4. **Configurar CORS específico** para seus domínios
5. **Implementar cache inteligente** com invalidação
6. **Testar em cenários reais** com diferentes navegadores

---

💡 **Dica**: Use as ferramentas do DevTools para debugar CORS e monitor cache hits/misses! 