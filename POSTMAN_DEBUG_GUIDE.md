# 🧪 Guia de Debug das APIs - Postman

Documentação completa para testar e debugar as 3 APIs REST usando Postman.

## 📋 Índice

1. [API Simples (Porta 5002)](#api-simples-porta-5002)
2. [API com Banco (Porta 5003)](#api-com-banco-porta-5003)  
3. [API Completa HATEOAS (Porta 5001)](#api-completa-hateoas-porta-5001)
4. [Configuração do Postman](#configuração-do-postman)
5. [Testes Automatizados](#testes-automatizados)

---

## 🔧 Configuração do Postman

### Variáveis de Ambiente
Crie um Environment no Postman com as seguintes variáveis:

```
API_SIMPLES = http://localhost:5002
API_BANCO = http://localhost:5003  
API_HATEOAS = http://localhost:5001
TOKEN = (será preenchido automaticamente após login)
```

### Headers Globais
Configure nas Collection Settings:

```
Content-Type: application/json
Accept: application/json
```

---

## 🔹 API Simples (Porta 5002)

### Credenciais de Teste
```
Admin: admin@user.com / admin
Cliente: customer@user.com / customer
```

### 1. Verificar Status da API
```http
GET {{API_SIMPLES}}/
```

**Resposta esperada:**
```json
{
  "mensagem": "API REST - Sistema de Livros",
  "versao": "1.0",
  "status": "ativo"
}
```

### 2. Login (Obter Token)
```http
POST {{API_SIMPLES}}/login
Content-Type: application/json

{
  "email": "admin@user.com",
  "password": "admin"
}
```

**Resposta esperada:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id": 1,
    "email": "admin@user.com",
    "role": "admin"
  }
}
```

**Script para extrair token:**
```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("TOKEN", jsonData.token);
}
```

### 3. Listar Livros
```http
GET {{API_SIMPLES}}/livros
```

**Resposta esperada:**
```json
{
  "livros": [],
  "total": 0
}
```

### 4. Criar Livro (Requer Autenticação)
```http
POST {{API_SIMPLES}}/livros
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "ano": 1899,
  "genero": "Romance"
}
```

**Resposta esperada:**
```json
{
  "mensagem": "Livro criado com sucesso",
  "livro": {
    "id": 1,
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "ano": 1899,
    "genero": "Romance",
    "criado_em": "2024-01-15T10:30:00.000000"
  }
}
```

### 5. Obter Livro Específico
```http
GET {{API_SIMPLES}}/livros/1
```

### 6. Atualizar Livro (Requer Autenticação)
```http
PUT {{API_SIMPLES}}/livros/1
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "titulo": "Dom Casmurro - Edição Revisada",
  "autor": "Machado de Assis",
  "ano": 1899,
  "genero": "Romance Brasileiro"
}
```

### 7. Deletar Livro (Requer Autenticação)
```http
DELETE {{API_SIMPLES}}/livros/1
Authorization: Bearer {{TOKEN}}
```

### 8. Buscar Livros
```http
GET {{API_SIMPLES}}/livros/buscar?q=machado
```

---

## 🗄️ API com Banco (Porta 5003)

### Credenciais de Teste
```
Admin: admin@biblioteca.com / admin123
Cliente: cliente@biblioteca.com / cliente123
```

### 1. Verificar Status da API
```http
GET {{API_BANCO}}/
```

**Resposta esperada:**
```json
{
  "mensagem": "API REST - Sistema de Biblioteca",
  "versao": "2.0",
  "database": "SQLAlchemy + SQLite",
  "status": "ativo",
  "endpoints": {
    "autenticacao": "/login",
    "livros": "/livros", 
    "usuarios": "/usuarios",
    "categorias": "/categorias"
  }
}
```

### 2. Login (Obter Token)
```http
POST {{API_BANCO}}/login
Content-Type: application/json

{
  "email": "admin@biblioteca.com",
  "password": "admin123"
}
```

**Resposta esperada:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id": 1,
    "email": "admin@biblioteca.com",
    "role": "admin",
    "nome": "Administrador do Sistema",
    "criado_em": "2024-01-15T10:00:00.000000",
    "ativo": true
  }
}
```

### 3. Registrar Novo Usuário
```http
POST {{API_BANCO}}/register
Content-Type: application/json

{
  "nome": "João Silva",
  "email": "joao@teste.com",
  "password": "senha123"
}
```

### 4. Listar Livros (com Paginação e Filtros)
```http
GET {{API_BANCO}}/livros?pagina=1&por_pagina=10&autor=machado&genero=romance&ano=1899
```

**Resposta esperada:**
```json
{
  "livros": [
    {
      "id": 1,
      "titulo": "Dom Casmurro",
      "autor": "Machado de Assis",
      "ano": 1899,
      "genero": "Romance",
      "isbn": "978-85-359-0277-5",
      "descricao": "Clássico da literatura brasileira",
      "paginas": 256,
      "disponivel": true,
      "criado_em": "2024-01-15T10:00:00.000000",
      "atualizado_em": "2024-01-15T10:00:00.000000",
      "criado_por": 1
    }
  ],
  "paginacao": {
    "pagina_atual": 1,
    "total_paginas": 1,
    "total_itens": 1,
    "por_pagina": 10,
    "tem_proxima": false,
    "tem_anterior": false
  }
}
```

### 5. Criar Livro (Requer Autenticação)
```http
POST {{API_BANCO}}/livros
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "titulo": "O Cortiço",
  "autor": "Aluísio Azevedo", 
  "ano": 1890,
  "genero": "Naturalismo",
  "isbn": "978-85-359-0123-4",
  "descricao": "Romance naturalista brasileiro",
  "paginas": 304
}
```

### 6. Obter Livro Específico
```http
GET {{API_BANCO}}/livros/1
```

### 7. Atualizar Livro (Requer Autenticação)
```http
PUT {{API_BANCO}}/livros/1
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "titulo": "Dom Casmurro - Nova Edição",
  "descricao": "Clássico da literatura brasileira - Edição comentada",
  "disponivel": true
}
```

### 8. Deletar Livro (Requer Autenticação)
```http
DELETE {{API_BANCO}}/livros/1
Authorization: Bearer {{TOKEN}}
```

### 9. Buscar Livros
```http
GET {{API_BANCO}}/livros/buscar?q=machado
```

### 10. Listar Usuários (Admin apenas)
```http
GET {{API_BANCO}}/usuarios
Authorization: Bearer {{TOKEN}}
```

### 11. Atualizar Usuário (Admin apenas)
```http
PUT {{API_BANCO}}/usuarios/2
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "nome": "Cliente Atualizado",
  "ativo": true,
  "role": "customer"
}
```

### 12. Listar Categorias
```http
GET {{API_BANCO}}/categorias
```

### 13. Criar Categoria (Admin apenas)
```http
POST {{API_BANCO}}/categorias
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "nome": "Ficção Científica",
  "descricao": "Livros de ficção científica"
}
```

### 14. Estatísticas do Sistema (Admin apenas)
```http
GET {{API_BANCO}}/stats
Authorization: Bearer {{TOKEN}}
```

**Resposta esperada:**
```json
{
  "total_livros": 3,
  "livros_disponiveis": 3,
  "total_usuarios": 2,
  "usuarios_ativos": 2,
  "total_categorias": 6,
  "livros_por_genero": {
    "Romance": 1,
    "Naturalismo": 1,
    "Tecnologia": 1
  }
}
```

---

## 🔗 API Completa HATEOAS (Porta 5001)

### Credenciais de Teste
```
Admin: admin@user.com / admin
Cliente: customer@user.com / customer
```

### 1. Verificar Status da API (com HATEOAS)
```http
GET {{API_HATEOAS}}/
Accept: application/json
```

**Resposta esperada:**
```json
{
  "mensagem": "API REST com HATEOAS",
  "_links": {
    "livros": {"href": "/livros"},
    "documentacao": {"href": "/docs"}
  }
}
```

### 2. Verificar Status da API (XML)
```http
GET {{API_HATEOAS}}/
Accept: application/xml
```

**Resposta esperada:**
```xml
<root>
  <mensagem>API REST com HATEOAS</mensagem>
</root>
```

### 3. Login (Obter Token)
```http
POST {{API_HATEOAS}}/login
Content-Type: application/json

{
  "email": "admin@user.com",
  "password": "admin"
}
```

**Resposta esperada:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "_links": {
    "self": {"href": "/login", "method": "POST"}
  }
}
```

### 4. Listar Livros (com Links HATEOAS)
```http
GET {{API_HATEOAS}}/livros
Accept: application/json
```

**Resposta esperada:**
```json
{
  "_embedded": {
    "livros": []
  },
  "_links": {
    "self": {"href": "/livros"},
    "create": {"href": "/livros", "method": "POST"}
  }
}
```

### 5. Criar Livro (com HATEOAS)
```http
POST {{API_HATEOAS}}/livros
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "titulo": "1984",
  "autor": "George Orwell"
}
```

**Resposta esperada:**
```json
{
  "id": 1,
  "titulo": "1984",
  "autor": "George Orwell",
  "_links": {
    "self": {"href": "/livros/1"},
    "update": {"href": "/livros/1", "method": "PUT"},
    "delete": {"href": "/livros/1", "method": "DELETE"}
  }
}
```

### 6. Obter Livro Específico (com HATEOAS)
```http
GET {{API_HATEOAS}}/livros/1
Authorization: Bearer {{TOKEN}}
```

### 7. Atualizar Livro (com HATEOAS)
```http
PUT {{API_HATEOAS}}/livros/1
Authorization: Bearer {{TOKEN}}
Content-Type: application/json

{
  "titulo": "1984 - Edição Especial",
  "autor": "George Orwell"
}
```

### 8. Deletar Livro (com HATEOAS)
```http
DELETE {{API_HATEOAS}}/livros/1
Authorization: Bearer {{TOKEN}}
```

**Resposta esperada:**
```json
{
  "title": "OK",
  "status": 200,
  "detail": "Livro removido com sucesso",
  "_links": {
    "listar": {"href": "/livros", "method": "GET"}
  }
}
```

### 9. Teste de Content Negotiation - Erro 415
```http
POST {{API_HATEOAS}}/livros
Authorization: Bearer {{TOKEN}}
Content-Type: text/plain

titulo=Teste&autor=Autor
```

**Resposta esperada:**
```json
{
  "title": "Unsupported Media Type",
  "status": 415,
  "detail": "Unsupported Media Type. Please use application/json or application/x-www-form-urlencoded"
}
```

### 10. Teste de Accept Header - Erro 406
```http
GET {{API_HATEOAS}}/livros
Accept: text/csv
```

**Resposta esperada:**
```json
{
  "title": "Not Acceptable",
  "status": 406,
  "detail": "Not Acceptable format requested: text/csv, only application/json and text/csv are supported"
}
```

---

## 🧪 Testes Automatizados

### Scripts de Teste para Collection

#### Teste de Login Bem-sucedido
```javascript
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('token');
    pm.environment.set("TOKEN", jsonData.token);
});
```

#### Teste de Criação de Livro
```javascript
pm.test("Book created successfully", function () {
    pm.response.to.have.status(201);
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('livro');
    pm.environment.set("BOOK_ID", jsonData.livro.id);
});
```

#### Teste de Autorização
```javascript
pm.test("Unauthorized access blocked", function () {
    pm.response.to.have.status(401);
    var jsonData = pm.response.json();
    pm.expect(jsonData.erro || jsonData.message).to.include("autorização");
});
```

#### Teste de Validação de Dados
```javascript
pm.test("Validation error for missing required fields", function () {
    pm.response.to.have.status(400);
    var jsonData = pm.response.json();
    pm.expect(jsonData.detalhes || jsonData.detail).to.include("obrigatório");
});
```

### Collection Runner - Sequência de Testes

1. **API Simples:**
   - Verificar Status → Login → Criar Livro → Listar → Editar → Deletar

2. **API com Banco:**
   - Verificar Status → Registrar → Login → Criar Livro → Buscar → Estatísticas

3. **API HATEOAS:**
   - Verificar Status → Login → Criar Livro → Verificar Links → Content Negotiation

---

## 🔍 Troubleshooting

### Erros Comuns

#### 401 Unauthorized
```json
{
  "erro": "Token de autorização necessário"
}
```
**Solução:** Verificar se o token está sendo enviado no header Authorization

#### 415 Unsupported Media Type
```json
{
  "erro": "Tipo de conteúdo inválido"
}
```
**Solução:** Definir `Content-Type: application/json`

#### 404 Not Found
```json
{
  "erro": "Livro não encontrado"
}
```
**Solução:** Verificar se o ID do livro existe

#### Connection Error
**Solução:** Verificar se a API está rodando na porta correta

### Logs de Debug

Para ver logs detalhados das APIs, verifique o console do Python onde elas estão executando.

---

## 📊 Collection do Postman

Para facilitar os testes, importe a collection completa:

1. Crie uma nova Collection no Postman
2. Adicione todas as requests acima
3. Configure as variáveis de ambiente
4. Execute os testes automatizados

---

**🎯 Resumo das Portas:**
- **Porta 5001:** API HATEOAS Completa
- **Porta 5002:** API REST Simples  
- **Porta 5003:** API REST com Banco de Dados 