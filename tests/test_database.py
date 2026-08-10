from src.vector_store import get_vector_store


def main():
    print("\nVerificando banco vetorial...")

    vector_store = get_vector_store()

    data = vector_store.get()

    total = len(data["ids"])

    print(f"\nTotal de registros no ChromaDB: {total}")

    print("\nPrimeiros IDs:")

    for document_id in data["ids"][:5]:
        print(f"- {document_id}")


if __name__ == "__main__":
    main()
