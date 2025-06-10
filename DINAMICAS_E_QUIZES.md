# 🎯 DINÂMICAS, QUIZES E DESAFIOS - Mini-Curso API REST

**Objetivo:** Manter engajamento, fixar conceitos e distribuir melhor o tempo de 3 horas

---

## 📊 **ESTRUTURA DAS DINÂMICAS**

### 🕐 **MOMENTO 1: Após Conceitos REST (15min)**
**⏰ Cronômetro: 00:15**

#### 🧠 **QUIZ TEÓRICO - "REST ou não REST?"** (5min)
**Dinâmica:** Alunos levantam placa VERDE (REST) ou VERMELHA (não REST)

**Perguntas:**
1. **"API com /clientes para listar e /clientes/1 para detalhes"** ✅ (Interface uniforme com recurso e identificação)
2. **"API que usa URLs como /getUser, /createUser"** ✅ (Não usa interface uniforme; deveria usar verbos HTTP)
3. **"API que guarda estado da sessão no servidor"** ❌ (Não é stateless)
4. **"API que usa Status Code 200 para tudo"** ❌ (Não segue padrões)
5. **"API que permite cache nos responses"** ✅ (Cacheable)
6. **"API que não retorna body quando o recurso não é encontrado"** ❌ (Sempre deve ter uma Response (body))
7. **"API que retorna 404 quando o recurso não é encontrado"** ✅ (Boa prática de status HTTP)



#### 💡 **EXERCÍCIO PRÁTICO - "Monte a URL"** (10min)
**Dinâmica:** Dividir turma em 4 grupos, cada grupo monta URLs REST

**Desafio:** Criar URLs para um sistema de **Posts do Blog**
```
Grupo 1: Listar todos os posts
Grupo 2: Criar novo post  
Grupo 3: Editar post específico
Grupo 4: Deletar post específico
```

**Resposta Esperada:**
```http
GET    /posts          # Listar
POST   /posts          # Criar
PUT    /posts/123      # Editar
DELETE /posts/123      # Deletar
```

---

### 🕑 **MOMENTO 2: Após API Simples Funcionar (25min)**
**⏰ Cronômetro: 00:40**

#### 🚀 **DESAFIO HANDS-ON - "Sua Primeira API"** (15min)
**Dinâmica:** Cada aluno modifica a API para criar sua própria entidade

**Desafio Individual:**
```python
# Criar uma nova entidade: FILMES
# Campos: id, nome, diretor, ano, nota (1-10)
# Implementar CRUD completo no app_rest_simples.py
```

**Checklist para o Instrutor:**
- [ ] Caminhar entre as máquinas verificando progresso
- [ ] Ajudar com erros de sintaxe
- [ ] Verificar se conseguem testar no Postman

#### 🏆 **MOMENTO DE APRESENTAÇÃO** (10min)
- 3-4 alunos mostram sua API funcionando
- Testar endpoints ao vivo
- Celebrar conquistas! 🎉

---

### 🕒 **MOMENTO 3: Após JWT Completo (55min)**
**⏰ Cronômetro: 00:55**

#### 🔐 **QUIZ INTERATIVO - "JWT Detective"** (8min)
**Dinâmica:** Decodificar JWT na prática

**Material:** Projetar token na tela
```
Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEsInJvbGUiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AdXNlci5jb20iLCJleHAiOjE3MDk5OTk5OTl9.signature_here
```

**Perguntas para os alunos:**
1. **"Quantas partes tem este JWT?"** (3)
2. **"Qual algoritmo usado?"** (HS256)
3. **"Qual o role do usuário?"** (admin)
4. **"Quando expira?"** (Converter timestamp)

#### ⚡ **DESAFIO CÓDIGO - "Token Master"** (7min)
**Dinâmica:** Competição em duplas

**Desafio:**
```javascript
// No console do navegador, decodificar este token:
const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...";

// 1. Extrair o email do usuário
// 2. Verificar se token está expirado
// 3. Mostrar todas as informações
```

**Solução:**
```javascript
const parts = token.split('.');
const payload = JSON.parse(atob(parts[1]));
console.log('Email:', payload.email);
console.log('Expirado:', payload.exp < Date.now() / 1000);
console.log('Dados completos:', payload);
```

---

### 🕓 **MOMENTO 4: Após API com Banco (1h20min)**
**⏰ Cronômetro: 01:20**

#### 🏗️ **PROJETO PRÁTICO - "Biblioteca Personalizada"** (20min)
**Dinâmica:** Trabalho em duplas para expandir a API

**Desafio das Duplas:**
```
Dupla 1: Adicionar campo "editora" nos livros + filtro
Dupla 2: Criar endpoint para livros mais recentes (últimos 30 dias)
Dupla 3: Implementar sistema de "favoritos" (nova tabela)
Dupla 4: Criar relatório de livros por autor (agrupamento)
Dupla 5: Adicionar foto/capa do livro (campo URL)
```

**Checklist para Instrutor:**
- [ ] Dividir turma em duplas
- [ ] Dar 15min para implementar
- [ ] 5min para cada dupla apresentar no Postman
- [ ] Ajudar com queries SQL/SQLAlchemy

#### 🎯 **QUIZ EXPRESS - "Banco de Dados"** (5min)
**Perguntas Rápidas:**
1. **"Qual ORM estamos usando?"** (SQLAlchemy)
2. **"Qual banco de dados?"** (SQLite)
3. **"Como definir relacionamento?"** (ForeignKey)
4. **"Para que serve db.session.commit()?"** (Salvar mudanças)

---

### 🕔 **MOMENTO 5: Após CORS (1h30min)**
**⏰ Cronômetro: 01:30**

#### 🌐 **DEMONSTRAÇÃO INTERATIVA - "CORS na Prática"** (10min)
**Dinâmica:** Experiência guiada de erro CORS

**Roteiro:**
1. **Desabilitar CORS** temporariamente na API
2. **Tentar requisição** do navegador
3. **Mostrar erro** no DevTools
4. **Reabilitar CORS** 
5. **Funcionar novamente**

**Comandos para os alunos executarem:**
```javascript
// No console do navegador (localhost:3000)
fetch('http://localhost:5003/livros')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('CORS Error:', error));
```

---

### 🕕 **MOMENTO 6: Durante React (1h45min-2h35min)**
**⏰ Cronômetro: 01:45 - 02:35**

#### 🎨 **SÉRIE DE MINI-DESAFIOS** (50min total)

##### **Mini-Desafio 1: Login Funcional** (15min)
```jsx
// Desafio: Adicionar validação visual
// - Email inválido = borda vermelha
// - Senha < 6 caracteres = aviso
// - Loading spinner no botão
```

##### **Mini-Desafio 2: Card Personalizado** (15min)
```jsx
// Desafio: Melhorar BookCard
// - Adicionar badge do gênero
// - Ícone de disponibilidade
// - Hover effects
// - Truncar descrição longa
```

##### **Mini-Desafio 3: Filtros Avançados** (20min)
```jsx
// Desafio: Implementar filtros
// - Select de gêneros
// - Range de anos  
// - Busca em tempo real
// - Limpar filtros
```

#### 🏃‍♂️ **CHECKPOINT RÁPIDO** (a cada 15min)
**Pergunta do Instrutor:** *"Quem conseguiu fazer funcionar?"*
- ✋ Levanta mão quem terminou
- 🤝 Quem terminou ajuda quem não terminou
- 📝 Anote quantos % conseguiram

---

### 🕖 **MOMENTO 7: Quiz Final (2h50min)**
**⏰ Cronômetro: 02:50**

#### 🏆 **QUIZ COMPLETO - "Mestre das APIs"** (10min)

**ROUND 1: Conceitos (2min)**
1. O que significa REST? 
2. JWT significa?
3. CORS resolve qual problema?

**ROUND 2: Prático - HTTP Status (2min)**
1. Status para criação bem-sucedida? (201)
2. Status para não autorizado? (401)  
3. Status para não encontrado? (404)

**ROUND 3: Prático - Endpoints (3min)**
```
"Como buscar livro com ID 5?"
"Como criar novo usuário?"
"Como atualizar livro existente?"
```

**ROUND 4: Código Express (3min)**
```javascript
// Qual o problema neste código?
const token = localStorage.getItem('token');
fetch('/api/protected', {
  headers: { 'Authorization': token }  // ❌ Falta "Bearer "
});
```

---

## 🎯 **SISTEMA DE PONTUAÇÃO**

### 🏆 **Ranking Individual**
- Quiz teórico: **1 ponto** por acerto
- Desafio prático completo: **3 pontos**
- Ajudar colega: **2 pontos**
- Apresentar código: **2 pontos**

### 🥇 **Prêmios Simbólicos**
- **🏆 1º Lugar:** "API Master"
- **🥈 2º Lugar:** "Full Stack Developer" 
- **🥉 3º Lugar:** "Code Helper"
- **🎖️ Participação:** "Future Developer"

---

## ⏰ **CRONÔMETRO DE ATIVIDADES**

| Horário | Atividade | Dinâmica | Duração |
|---------|-----------|----------|---------|
| 00:15 | Quiz REST | Placas Verde/Vermelha | 5min |
| 00:20 | Exercício URLs | Grupos | 10min |
| 00:40 | Desafio API Própria | Individual | 15min |
| 00:55 | JWT Detective | Interativo | 8min |
| 01:03 | Token Master | Duplas | 7min |
| 01:20 | Biblioteca Personalizada | Duplas | 20min |
| 01:30 | CORS Demo | Experiência guiada | 10min |
| 01:45-02:35 | React Mini-Desafios | Progressivos | 50min |
| 02:50 | Quiz Final | Competitivo | 10min |

**Total Dinâmicas: 135min (2h15min) do curso total**

---

## 📋 **CHECKLIST DO INSTRUTOR**

### ✅ **Preparação**
- [ ] Imprimir placas verde/vermelha (ou usar mãos)
- [ ] Preparar timer visível para todos
- [ ] Ter tokens JWT prontos para decodificar
- [ ] Preparar ranking na lousa/slide

### ✅ **Durante as Dinâmicas**
- [ ] Circular entre as máquinas constantemente
- [ ] Anotar quem está com dificuldades
- [ ] Celebrar pequenas vitórias
- [ ] Manter energia alta
- [ ] Adaptar tempo conforme necessário

### ✅ **Frases Motivacionais**
- *"Quem conseguiu? Levanta a mão!"*
- *"Errar é parte do processo - vamos debugar juntos!"*
- *"Este erro é clássico, todo dev já passou por isso!"*
- *"Vocês estão mandando muito bem!"*
- *"Na vida real, 80% é problema de CORS!"*

---

## 🎨 **VARIAÇÕES PARA TURMAS DIFERENTES**

### 👨‍💻 **Turma Avançada**
- Adicionar desafios de performance
- Implementar testes automatizados
- Deploy em cloud providers
- Padrões de arquitetura

### 👩‍🎓 **Turma Iniciante**
- Mais tempo nos conceitos básicos
- Exercícios mais guiados
- Menos JavaScript, mais Python
- Foco na compreensão vs velocidade

### 🏢 **Turma Corporativa**
- Foco em boas práticas
- Segurança e compliance
- Documentação
- Padrões da empresa

---

## 📊 **MÉTRICAS DE SUCESSO**

### 🎯 **Objetivos por Dinâmica**
- **70%** acertam quiz teórico
- **80%** conseguem completar desafios práticos
- **90%** participam ativamente
- **100%** se divertem aprendendo!

### 📈 **Indicadores de Engajamento**
- Perguntas dos alunos aumentam
- Menos pessoas olhando celular
- Risadas e comemoração nos acertos
- Colaboração espontânea entre alunos

---

💡 **DICA DOURADA:** Se alguma dinâmica estiver tomando muito tempo, corte para manter o cronograma. É melhor terminar todas as partes do que se aprofundar demais em uma só! 