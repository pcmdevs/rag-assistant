# 📚 RAG Assistant

Assistente inteligente capaz de **responder perguntas com base em documentos PDF**.

O projeto utiliza Inteligência Artificial e busca semântica para encontrar informações nos documentos e gerar respostas objetivas, mostrando também as fontes utilizadas.

![Demonstração do RAG Assistant](assets/rag-assistant-demo.png)

---

## 💡 Sobre o projeto

Empresas possuem manuais, políticas, procedimentos e outros documentos que podem conter muitas páginas de informação.

Encontrar uma resposta específica nesses arquivos manualmente pode ser demorado.

O **RAG Assistant** transforma esses documentos em uma base de conhecimento que pode ser consultada através de perguntas em linguagem natural.

Por exemplo:

> **"Como funciona a matrícula?"**

O sistema procura a informação nos documentos, identifica os trechos mais relevantes e utiliza Inteligência Artificial para gerar a resposta.

---

## ✨ O que a aplicação faz

- 📄 Permite adicionar documentos PDF
- 💬 Recebe perguntas em linguagem natural
- 🔎 Pesquisa automaticamente nos documentos
- 🧠 Utiliza busca semântica para encontrar informações relacionadas
- 🤖 Gera respostas utilizando Inteligência Artificial
- 📚 Mostra os documentos utilizados como fonte
- 💾 Mantém uma base vetorial dos documentos
- 🖥️ Possui interface web interativa

---

## ⚙️ Como funciona

De forma simplificada:

```text
📄 Documentos PDF
        ↓
🧠 Processamento
        ↓
🔎 Busca pela informação
        ↓
🤖 Inteligência Artificial
        ↓
💬 Resposta + fontes
```

O projeto utiliza uma arquitetura chamada **RAG (Retrieval-Augmented Generation)**.

Antes de responder, a aplicação procura informações relevantes nos documentos e fornece esse conteúdo para a IA.

Isso permite criar assistentes especializados em uma base de documentos específica.

---

## 🛠️ Tecnologias

O projeto foi desenvolvido com:

**Python • LangChain • Google Gemini • ChromaDB • Streamlit**

Também foram aplicados conceitos de:

**RAG • LLMs • Embeddings • Busca Semântica • Bancos Vetoriais**

---

## 🎯 O que desenvolvi neste projeto

Durante o desenvolvimento foram implementados:

- processamento e divisão de documentos;
- geração de embeddings;
- armazenamento em banco vetorial;
- recuperação semântica de informações;
- integração com modelo de linguagem;
- sistema de fontes e relevância;
- upload de novos documentos;
- interface web;
- tratamento de erros e logs;
- testes dos principais componentes;
- organização modular do código.

---

## 🚀 Executando o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/pcmdevs/rag-assistant.git
cd rag-assistant
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure a API

Crie um arquivo `.env` na raiz do projeto utilizando o `.env.example` como referência.

Adicione sua chave da API Gemini:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> A chave real da API não é armazenada no repositório.

### 4. Processe os documentos

```bash
python ingest.py
```

### 5. Inicie a aplicação

```bash
streamlit run web_app.py
```

A interface estará disponível no navegador.

---

## 🗺️ Próximas melhorias

- Memória de conversa
- Melhorias na precisão das buscas
- Suporte a outros formatos de documentos
- Streaming das respostas
- Testes automatizados
- Docker
- Deploy público

---

## 📌 Observação

Os documentos utilizados na demonstração são **fictícios** e foram criados exclusivamente para testes e apresentação do projeto.