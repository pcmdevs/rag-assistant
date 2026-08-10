from langchain_core.documents import Document

from config.settings import (
    TOP_K,
    RELEVANCE_THRESHOLD,
)

from src.vector_store import get_vector_store
from src.logger import get_logger
from src.exceptions import RetrievalError


logger = get_logger(__name__)


def retrieve_documents(
    question: str,
) -> list[tuple[Document, float]]:
    """
    Busca documentos relevantes
    no banco vetorial.
    """

    if not question or not question.strip():
        return []

    try:
        logger.info(
            "Iniciando busca vetorial."
        )

        vector_store = get_vector_store()

        results = (
            vector_store
            .similarity_search_with_relevance_scores(
                query=question,
                k=TOP_K,
            )
        )

        filtered_results = [
            (document, score)
            for document, score in results
            if score >= RELEVANCE_THRESHOLD
        ]

        logger.info(
            "%s documento(s) relevante(s) encontrado(s).",
            len(filtered_results),
        )

        return filtered_results

    except Exception as error:
        logger.exception(
            "Erro durante a recuperação de documentos."
        )

        raise RetrievalError(
            "Não foi possível consultar "
            "a base de conhecimento."
        ) from error
