from config.settings import (
    create_project_directories,
    validate_settings,
)

from src.loader import load_all_pdfs
from src.splitter import split_documents
from src.vector_store import (
    add_documents_to_vector_store,
)


def main():
    print("\nIniciando ingestão de documentos...\n")

    validate_settings()
    create_project_directories()

    print("1. Carregando PDFs...")

    documents = load_all_pdfs()

    print(
        f"   {len(documents)} página(s) carregada(s)."
    )

    print("\n2. Dividindo documentos em chunks...")

    chunks = split_documents(documents)

    print(
        f"   {len(chunks)} chunk(s) criado(s)."
    )

    print(
        "\n3. Gerando embeddings "
        "e atualizando o ChromaDB..."
    )

    processed = add_documents_to_vector_store(
        chunks
    )

    print(
        f"\n   {processed} chunk(s) processado(s)."
    )

    print(
        "\nIngestão concluída com sucesso!"
    )


if __name__ == "__main__":
    main()
