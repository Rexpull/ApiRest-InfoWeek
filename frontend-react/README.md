# 📚 Sistema de Biblioteca - Frontend React

Frontend moderno em React + Tailwind CSS para gerenciamento de livros, consumindo a API REST com banco de dados.

## 🚀 Tecnologias

- **React 18** - Framework JavaScript
- **Tailwind CSS** - Framework CSS utility-first
- **Axios** - Cliente HTTP para requisições à API
- **React Hooks** - Gerenciamento de estado

## 🎯 Funcionalidades

- ✅ **Autenticação** - Login/logout com JWT
- ✅ **Cadastro** - Registro de novos usuários
- ✅ **CRUD de Livros** - Criar, listar, editar e excluir livros
- ✅ **Busca** - Pesquisar livros por título, autor ou descrição
- ✅ **Paginação** - Navegação entre páginas de livros
- ✅ **Responsivo** - Interface adaptável a mobile/tablet/desktop

## 📦 Instalação e Execução

### Pré-requisitos
- Node.js 16+
- npm ou yarn
- API com banco rodando na porta 5003

### Passos

1. **Instale as dependências:**
```bash
npm install
```

2. **Configure o Tailwind CSS:**
```bash
npx tailwindcss init -p
```

3. **Execute a aplicação:**
```bash
npm start
```

4. **Acesse o frontend:**
- URL: http://localhost:3000
- A aplicação conecta automaticamente com http://localhost:5003

## 🔗 Dependências da API

Este frontend foi desenvolvido especificamente para a **API com Banco de Dados** (porta 5003). Certifique-se de que ela esteja rodando:

```bash
cd api
python app_rest_db.py
```

## 🎨 Interface

### Tela de Login
- Alternância entre Login/Cadastro
- Credenciais de teste exibidas
- Validação de campos

### Dashboard Principal  
- Header com informações do usuário
- Barra de busca e filtros
- Grade responsiva de livros
- Paginação automática
- Botões de ação (adicionar, editar, excluir)

### Formulários
- Modal para adicionar/editar livros
- Validação de campos obrigatórios
- Interface limpa e intuitiva

## 🔐 Autenticação

### Credenciais de Teste
- **Admin:** admin@biblioteca.com / admin123
- **Cliente:** cliente@biblioteca.com / cliente123

### Fluxo de Autenticação
1. Login retorna JWT token
2. Token armazenado no localStorage
3. Token enviado automaticamente nas requisições
4. Logout limpa dados locais

## 📱 Responsividade

- **Desktop:** Grid de 3 colunas
- **Tablet:** Grid de 2 colunas  
- **Mobile:** Grid de 1 coluna
- **Formulários:** Adaptáveis ao tamanho da tela

## 🛠️ Estrutura do Projeto

```
frontend-react/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── BookCard.jsx
│   │   └── BookForm.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── index.js
│   └── index.css
├── package.json
├── tailwind.config.js
└── README.md
```

## 🎯 Comparação com Frontend Anterior

### ✅ Melhorias
- **Código 70% menor** - Componentização React
- **Performance** - Renderização otimizada
- **Manutenibilidade** - Separação de responsabilidades
- **Styling** - Tailwind CSS mais produtivo
- **API única** - Foco na API com banco

### 🗑️ Removido
- Seletor de múltiplas APIs
- Seção de informações JWT
- Interface HTML/CSS/JS vanilla
- Documentação extensa inline

## 🚀 Deploy

Para fazer build para produção:

```bash
npm run build
```

Os arquivos serão gerados na pasta `build/` prontos para deploy.

---

**Conecta-se exclusivamente com:** API REST com Banco (porta 5003) 