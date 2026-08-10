from langchain_core.prompts import (
    ChatPromptTemplate,
)

from config.prompts import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_PROMPT,
)

from src.llm import get_llm
from src.retriever import retrieve_documents
from src.logger import get_logger
from src.exceptions import RAGException


logger = get_logger(__name__)


def build_context(results) -> str:
    """
    Converte os documentos recuperados
    em contexto para o modelo.
    """

    context_parts = []

    for index, (document, score) in enumerate(
        results,
        start=1,
    ):

        filename = document.metadata.get(
            "filename",
            "Fonte desconhecida",
        )

        page = document.metadata.get("page")

        if page is not None:
            page += 1

        context_part = f"""
DOCUMENTO {index}

Fonte: {filename}
Página: {page if page is not None else "Desconhecida"}
Relevância: {score:.4f}

Conteúdo:
{document.page_content}
"""

        context_parts.append(context_part)

    return "\n".join(context_parts)


def ask_rag(question: str) -> dict:
    """
    Executa o fluxo completo do RAG.
    """

    if not question or not question.strip():
        raise ValueError(
            "A pergunta não pode estar vazia."
        )

    logger.info(
        "Pergunta recebida para processamento."
    )

    try:
        results = retrieve_documents(question)

        if not results:
            logger.info(
                "Nenhum contexto relevante encontrado."
            )

            return {
                "answer": (
                    "Não encontrei informações suficientes "
                    "na base de conhecimento para responder "
                    "a essa pergunta."
                ),
                "sources": [],
            }

        context = build_context(results)

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    RAG_SYSTEM_PROMPT,
                ),
                (
                    "human",
                    RAG_USER_PROMPT,
                ),
            ]
        )

        messages = prompt.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        llm = get_llm()

        logger.info(
            "Enviando contexto para o modelo."
        )

        response = llm.invoke(messages)

        answer = response.text.strip()

        no_information_message = (
            "Não encontrei informações suficientes "
            "na base de conhecimento para responder "
            "a essa pergunta."
        )

        if (
            no_information_message.lower()
            in answer.lower()
        ):
            logger.info(
                "Modelo informou ausência "
                "de informação suficiente."
            )

            return {
                "answer": answer,
                "sources": [],
            }

        sources = []

        for document, score in results:

            source = {
                "filename": document.metadata.get(
                    "filename",
                    "Fonte desconhecida",
                ),
                "page": (
                    document.metadata.get(
                        "page",
                        0,
                    )
                    + 1
                ),
                "score": score,
            }

            sources.append(source)

        logger.info(
            "Resposta gerada com sucesso."
        )

        return {
            "answer": answer,
            "sources": sources,
        }

    except RAGException:
        raise

    except Exception as error:
        logger.exception(
            "Erro inesperado durante "
            "o processamento do RAG."
        )

        raise RAGException(
            "Ocorreu um erro inesperado "
            "durante o processamento da pergunta."
        ) from error
