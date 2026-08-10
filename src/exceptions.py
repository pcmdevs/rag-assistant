class RAGException(Exception):
    """
    Exceção base do projeto, utilizada para indicar que o banco de dados está vazio.
    """

    pass


class DocumentLoadError(RAGException):
    """
    Erro ao carregar documentos
    """
    pass


class EbeddingError(RAGException):
    """
    Erro ao gerar embeddings
    """
    pass


class RetrievalError(RAGException):
    """
    Erro durante a busca
    """
    pass


class LLMError(RAGException):
    """
    Erro ao consultar o LLM
    """
    pass
