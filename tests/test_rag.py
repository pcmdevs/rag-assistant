from src.rag import ask_rag


def main():

    question = (
        "Qual é o valor do auxílio home office?"
    )

    print("\nPergunta:")
    print(question)

    print("\nConsultando o RAG...")

    result = ask_rag(question)

    print("\nResposta:")
    print(result["answer"])

    print("\nFontes:")

    if not result["sources"]:
        print("Nenhuma fonte encontrada.")

    for source in result["sources"]:
        print(
            f"- {source['filename']} "
            f"| Página {source['page']} "
            f"| Relevância {source['score']:.4f}"
        )


if __name__ == "__main__":
    main()
