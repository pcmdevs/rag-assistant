from src.retriever import retrieve_documents


def main():
    question = "Como funciona a matrícula?"

    print("\nPergunta:")
    print(question)

    print("\nBuscando documentos relevantes...")

    results = retrieve_documents(question)

    if not results:
        print("\nNenhum documento relevante encontrado.")
        return

    print(f"\nResultados encontrados: {len(results)}")

    for index, (document, score) in enumerate(results, start=1):
        print("\n" + "=" * 60)
        print(f"RESULTADO {index}")
        print(f"Relevância: {score:.4f}")

        print("\nConteúdo:")
        print(document.page_content)

        print("\nFonte:")
        print(document.metadata.get("filename", "Desconhecida"))

        page = document.metadata.get("page")

        if page is not None:
            print(f"Página: {page + 1}")


if __name__ == "__main__":
    main()
