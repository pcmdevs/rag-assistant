from src.embeddings import get_embeddings


def main():
    print("\nCriando modelo de embeddings...")

    embeddings = get_embeddings()

    print("Gerando embedding de teste...")

    vector = embeddings.embed_query(
        "Este é um teste do nosso sistema RAG."
    )

    print("\nEmbedding criado com sucesso!")
    print(f"Quantidade de dimensões: {len(vector)}")

    print("\nPrimeiros valores do vetor:")
    print(vector[:5])


if __name__ == "__main__":
    main()
