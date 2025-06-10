# ✅ CHECKLIST DO INSTRUTOR - Mini-Curso API REST

## 🎯 **PREPARAÇÃO PRÉ-AULA** (30 min antes)

### Ambiente Técnico
- [ ] Testar todas as 3 APIs (5001, 5002, 5003)
- [ ] Verificar Postman com collections funcionando
- [ ] Verificar frontend React rodando na porta 3000
- [ ] Preparar backup dos códigos
- [ ] Testar projetor/tela compartilhada

### Ferramentas Abertas
- [ ] VSCode com projeto aberto
- [ ] Postman com environments configurados
- [ ] Terminal/PowerShell (2 abas: api e frontend)
- [ ] Navegador com DevTools preparado
- [ ] jwt.io em aba separada

### Material para Dinâmicas
- [ ] Timer/cronômetro visível para todos
- [ ] Tokens JWT prontos para decodificar
- [ ] Lousa/slides para ranking
- [ ] `DINAMICAS_E_QUIZES.md` impresso/aberto

---

## ⏰ **ROTEIRO HORA A HORA**

### **🕐 HORA 1: APIs + JWT (60min)**

#### ✅ **00:00-15: Setup e Introdução**
- [ ] **Apresentação:** "Vamos construir um sistema completo"
- [ ] **Demo rápida:** Mostrar resultado final (2min)
- [ ] **Estrutura:** Explicar pastas api/ e frontend-react/
- [ ] **Conceitos:** REST, JSON, HTTP methods
- [ ] **Terminal:** `pip install -r requirements.txt`

**🎬 Frase de abertura:** *"Em 3 horas vocês vão do zero a um sistema completo funcionando!"*

#### ✅ **15:00-30: 🎯 DINÂMICA - Quiz REST + URLs**
- [ ] **Quiz:** Placas verde/vermelha "REST ou não REST?" (5min)
- [ ] **Exercício:** Grupos criam URLs para Blog Posts (10min)
- [ ] **Circular:** Ajudar grupos com dúvidas
- [ ] **Apresentação:** Cada grupo mostra suas URLs

**🎯 Objetivo:** *"Fixar conceitos antes da prática!"*

#### ✅ **30:00-55: API Simples + Postman**
- [ ] **Código:** Mostrar `app_rest_simples.py` (estrutura)
- [ ] **Executar:** `python app_rest_simples.py` (porta 5002)
- [ ] **Postman 1:** GET / (verificar status)
- [ ] **Postman 2:** POST /login (admin@user.com/admin)
- [ ] **Postman 3:** GET /livros (lista vazia)
- [ ] **Postman 4:** POST /livros (criar 1984 - George Orwell)
- [ ] **Postman 5:** GET /livros (agora com 1 livro)
- [ ] **Demo:** PUT e DELETE rápidos

**🎯 Objetivo:** *"Mostrar que API funciona em 25 minutos!"*

#### ✅ **55:00-20: 🎯 DINÂMICA - Desafio API Filmes**
- [ ] **Explicar:** Cada aluno cria entidade FILMES (15min)
- [ ] **Circular:** Ajudar com erros de sintaxe e lógica
- [ ] **Verificar:** Se conseguem testar no Postman
- [ ] **Apresentações:** 3-4 alunos mostram API funcionando
- [ ] **Celebrar:** Conquistas e primeiros sucessos! 🎉

**🎯 Objetivo:** *"Primeira API criada do zero!"*

#### ✅ **20:00-40: JWT na Prática**
- [ ] **jwt.io:** Decodificar token obtido no Postman
- [ ] **Console:** Mostrar código JavaScript de decodificação
- [ ] **Conceito:** Header.Payload.Signature
- [ ] **Novo endpoint:** POST /jwt/configure (configurar secret)
- [ ] **Verificar:** GET /jwt/info

**💡 Tip:** *"JWT é como um passaporte digital!"*

#### ✅ **40:00-55: 🎯 DINÂMICA - JWT Detective**
- [ ] **Quiz:** Decodificar JWT projetado na tela (8min)
- [ ] **Desafio:** Duplas competem no console do navegador (7min)
- [ ] **Circular:** Verificar se conseguem extrair dados
- [ ] **Apresentar:** Soluções das duplas

**🎯 Objetivo:** *"Dominar JWT visceralmente!"*

#### ✅ **55:00-15: API com Banco**
- [ ] **Parar:** API simples (Ctrl+C)
- [ ] **Executar:** `python app_rest_db.py` (porta 5003)
- [ ] **Mostrar:** arquivo database.db criado
- [ ] **Código:** `models.py` (User, Book, Category)
- [ ] **Postman:** Login com admin@biblioteca.com/admin123
- [ ] **Postman:** POST /register (novo usuário)
- [ ] **Postman:** POST /livros (com mais campos: ISBN, descrição)
- [ ] **Postman:** GET /livros?autor=machado (filtros)
- [ ] **Postman:** GET /stats (estatísticas admin)

**🚀 Destaque:** *"Agora temos dados persistentes!"*

#### ✅ **15:00-35: 🎯 DINÂMICA - Biblioteca Personalizada**
- [ ] **Dividir:** Turma em duplas com desafios específicos
- [ ] **Desafios:** Editora, recentes, favoritos, relatórios, fotos
- [ ] **Circular:** Ajudar com queries SQL/SQLAlchemy
- [ ] **Apresentações:** Cada dupla demonstra no Postman (5min)
- [ ] **Quiz rápido:** Banco de dados (5min)

**🎯 Objetivo:** *"Expandir conhecimento SQLAlchemy!"*

---

### **🕑 HORA 2: CORS + React Setup (60min)**

#### ✅ **80:00-90: CORS e OPTIONS**
- [ ] **Conceito:** Same-Origin Policy problema
- [ ] **Código:** Mostrar configuração CORS na API
- [ ] **Terminal:** Curl OPTIONS para demonstrar preflight
- [ ] **DevTools:** Mostrar headers CORS
- [ ] **Endpoint:** GET /options-info (explicação)

**🌐 Insight:** *"CORS é a ponte entre frontend e backend!"*

#### ✅ **90:00-105: React Setup**
- [ ] **Terminal 2:** `cd frontend-react`
- [ ] **Verificar:** `npm install` já executado
- [ ] **Estrutura:** Mostrar src/components/, src/services/
- [ ] **Arquivo:** `services/api.js` (configuração axios)
- [ ] **Conceito:** Interceptors para token automático

#### ✅ **105:00-125: Login Component**
- [ ] **Código:** `Login.jsx` (useState, handleSubmit)
- [ ] **Executar:** `npm start` (porta 3000)
- [ ] **Testar:** Login com admin@biblioteca.com/admin123
- [ ] **DevTools:** Application > Local Storage (ver token)
- [ ] **Testar:** Credenciais inválidas (mostrar erro)

**⚡ Momento chave:** *"Primeira integração funcionando!"*

---

### **🕒 HORA 3: Dashboard + CRUD (50min)**

#### ✅ **125:00-150: Dashboard Completo**
- [ ] **Código:** `Dashboard.jsx` (useEffect, loadBooks)
- [ ] **Mostrar:** Header com nome do usuário
- [ ] **API call:** useEffect carregando livros automaticamente
- [ ]             **Código:** `BookCard.jsx` (componente reutilizável)
- [ ] **Layout:** Grid responsivo com Tailwind
- [ ] **Testar:** Responsividade (mobile view no DevTools)

**🎨 Visual:** *"Interface moderna em poucos minutos!"*

#### ✅ **150:00-170: CRUD Frontend**
- [ ] **Código:** `BookForm.jsx` (modal, formData)
- [ ] **Testar:** Criar novo livro via formulário
- [ ] **Testar:** Editar livro existente
- [ ] **Testar:** Deletar com confirmação
- [ ] **LocalStorage:** Mostrar token salvo automaticamente no DevTools
- [ ] **Network:** Mostrar requisições no DevTools

**🔥 Final épico:** *"Sistema completo funcionando!"*

---

## 🎯 **WRAP-UP (10min)**

### ✅ **170:00-180: Recapitulação**
- [ ] **Checklist:** ✅ API ✅ JWT ✅ Banco ✅ React ✅ Integração
- [ ] **Próximos passos:** Deploy, testes, authentication avançado
- [ ] **Materiais:** README's, collection Postman, código GitHub
- [ ] **Q&A:** Perguntas dos alunos

---

## 🚨 **TROUBLESHOOTING RÁPIDO**

### Problemas Comuns
- **API não inicia:** Verificar porta livre, dependências instaladas
- **CORS error:** Verificar origins na configuração CORS
- **Login falha:** Verificar credenciais e token no Postman
- **Frontend não conecta:** Verificar URL da API (localhost:5003)
- **Database error:** Deletar database.db e reiniciar API

### Comandos de Emergência
```bash
# Resetar API com banco
python database.py reset

# Limpar cache do React
rm -rf node_modules package-lock.json
npm install

# Verificar processos nas portas
netstat -ano | findstr :5003
netstat -ano | findstr :3000
```

---

## 📊 **MÉTRICAS DE SUCESSO**

### Durante a Aula
- [ ] Alunos conseguem fazer login no Postman
- [ ] Alunos veem livros carregando no frontend
- [ ] Pelo menos 80% consegue criar um livro
- [ ] Ninguém perdido por mais de 5 minutos

### Feedback Final
- [ ] **Clareza:** Explicações compreendidas
- [ ] **Ritmo:** Não muito rápido/lento
- [ ] **Prática:** Código funcionando para todos
- [ ] **Utilidade:** Conseguem aplicar no trabalho

---

## 🎬 **FRASES MOTIVACIONAIS**

### Momentos-Chave
- **Início:** *"Vamos do zero ao deploy em 3 horas!"*
- **Primeira API:** *"Vocês acabaram de criar uma API profissional!"*
- **JWT:** *"Agora entendem autenticação de verdade!"*
- **Banco funcionando:** *"Dados persistentes = aplicação real!"*
- **Frontend conectado:** *"Frontend + Backend = magia!"*
- **Final:** *"Parabéns! Vocês têm um sistema completo!"*

### Quando algo não funciona
- *"Erro é parte do aprendizado - vamos debugar juntos!"*
- *"Na vida real, 50% é debugar - vocês estão no caminho certo!"*

---

## 📱 **BACKUP PLANS**

### Se API não funcionar
- [ ] Usar código comentado como backup
- [ ] Mostrar Postman Collection pré-configurada
- [ ] Fazer demonstração gravada

### Se React falhar
- [ ] Usar versão simplificada HTML/JS
- [ ] Focar mais tempo na API
- [ ] Demo gravada do frontend

### Se internet cair
- [ ] Exemplos locais preparados
- [ ] Códigos salvos offline
- [ ] Slides de backup

---

💡 **LEMBRE-SE:** O importante é o aprendizado, não a perfeição. Se algo falhar, transforme em oportunidade de ensino sobre debugging! 