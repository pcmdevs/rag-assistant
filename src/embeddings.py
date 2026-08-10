from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.settings import (
    EMBEDDING_MODEL,
    GEMINI_API_KEY,
    validate_settings,
)


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """
    Cria e retorna o modelo de embeddings
    utilizado pelo sistema RAG.
    """

    validate_settings()

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY,
    )
