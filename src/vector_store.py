import hashlib

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config.settings import DATABASE_DIR
from src.embeddings import get_embeddings


COLLECTION_NAME = "rag_documents"


def get_vector_store() -> Chroma:
    """
    Cria ou conecta ao banco vetorial ChromaDB.
    """

    embeddings = get_embeddings()

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(DATABASE_DIR),
    )


def generate_document_id(document: Document) -> str:
    """
    Gera um ID único e determinístico para cada chunk.

    O ID leva em consideração:
    - nome do arquivo
    - página
    - conteúdo do chunk

    Dessa forma, o mesmo chunk sempre gera o mesmo ID.
    """

    filename = document.metadata.get(
        "filename",
        "unknown",
    )

    page = document.metadata.get(
        "page",
        0,
    )

    content = document.page_content

    raw_id = f"{filename}|{page}|{content}"

    return hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()


def add_documents_to_vector_store(
    documents: list[Document],
) -> int:
    """
    Adiciona documentos ao ChromaDB utilizando
    IDs determinísticos.

    Se um chunk com o mesmo ID já existir,
    ele será atualizado em vez de duplicado.

    Retorna a quantidade de documentos processados.
    """

    if not documents:
        raise ValueError(
            "Nenhum documento foi recebido para indexação."
        )

    vector_store = get_vector_store()

    ids = [
        generate_document_id(document)
        for document in documents
    ]

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    return len(documents)
