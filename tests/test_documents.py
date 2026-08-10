from src.loader import load_all_pdfs
from src.splitter import split_documents


def main():
    print("\nCarregando documentos...")

    documents = load_all_pdfs()

    print(
        f"Páginas carregadas: {len(documents)}"
    )

    print("\nCriando chunks...")

    chunks = split_documents(documents)

    print(
        f"Chunks criados: {len(chunks)}"
    )

    if chunks:
        print("\nPrimeiro chunk:")
        print("-" * 50)

        print(chunks[0].page_content[:500])

        print("-" * 50)

        print("\nMetadata:")
        print(chunks[0].metadata)


if __name__ == "__main__":
    main()
