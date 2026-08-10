from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from config.settings import DOCUMENTS_DIR


def load_pdf(file_path: Path) -> list[Document]:
    """
    Carrega um arquivo PDF e retorna
    uma lista de documentos do LangChain.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {file_path}"
        )

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(
            f"O arquivo precisa ser PDF: {file_path.name}"
        )

    loader = PyPDFLoader(str(file_path))

    documents = loader.load()

    return documents


def load_all_pdfs() -> list[Document]:
    """
    Carrega todos os arquivos PDF existentes
    na pasta documents.
    """

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "Nenhum arquivo PDF encontrado "
            "na pasta documents."
        )

    all_documents = []

    for pdf_file in pdf_files:
        documents = load_pdf(pdf_file)

        for document in documents:
            document.metadata["filename"] = pdf_file.name

        all_documents.extend(documents)

    return all_documents
