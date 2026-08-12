O projeto **RAG Assistant** foi desenvolvido para permitir que um usuário faça perguntas sobre documentos PDF e receba respostas baseadas no conteúdo desses arquivos.

A arquitetura utilizada foi RAG, que significa **Retrieval-Augmented Generation**. A ideia principal é que a inteligência artificial não responda apenas com base no conhecimento geral do modelo. Antes de gerar uma resposta, o sistema procura informações relevantes dentro dos documentos enviados pelo usuário.

O fluxo começa com o carregamento dos PDFs. Esses documentos são lidos e divididos em partes menores chamadas **chunks**. Essa divisão é importante porque trabalhar com documentos inteiros dificultaria a busca por informações específicas.

Depois, cada chunk é transformado em um **embedding**, que é uma representação numérica do significado do texto. Esses embeddings são armazenados no ChromaDB, que funciona como um banco vetorial.

Quando o usuário faz uma pergunta, essa pergunta também é transformada em embedding. O sistema compara o significado da pergunta com os chunks armazenados no banco e recupera os trechos semanticamente mais relevantes.

Esses trechos são então enviados como contexto para o Google Gemini, junto com a pergunta do usuário. O modelo gera uma resposta utilizando as informações recuperadas dos documentos.

O projeto também preserva metadados, como nome do arquivo e página, permitindo mostrar as fontes utilizadas na resposta.

Além do pipeline RAG, foi criada uma interface web com Streamlit, onde o usuário pode enviar novos PDFs, visualizar os documentos disponíveis, fazer perguntas e consultar as fontes.

Durante o desenvolvimento também foram implementados tratamento de erros, logs, testes dos principais componentes, controle de duplicação no banco vetorial e ajustes de relevância para melhorar a recuperação das informações.

Com esse projeto eu trabalhei conceitos como Python, LangChain, Gemini, embeddings, bancos vetoriais, busca semântica, ChromaDB, Streamlit, RAG, tratamento de erros e organização modular de código.
