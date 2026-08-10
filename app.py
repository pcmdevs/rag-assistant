from src.rag import ask_rag
from src.logger import get_logger
from src.exceptions import RAGException


logger = get_logger(__name__)


def show_header():
    print("\n" + "=" * 60)
    print("              TechNova RAG Assistant")
    print("=" * 60)

    print(
        "\nFaça perguntas sobre os documentos "
        "da base de conhecimento."
    )

    print(
        "Digite 'sair' para encerrar o programa."
    )


def show_sources(sources):
    if not sources:
        print("\nFontes:")
        print("Nenhuma fonte encontrada.")
        return

    print("\nFontes:")

    for source in sources:
        print(
            f"- {source['filename']} "
            f"| Página {source['page']} "
            f"| Relevância {source['score']:.4f}"
        )


def main():
    logger.info(
        "Aplicação iniciada."
    )

    show_header()

    while True:

        print("\n" + "-" * 60)

        question = input(
            "\nVocê > "
        ).strip()

        if question.lower() in {
            "sair",
            "exit",
            "quit",
        }:
            logger.info(
                "Aplicação encerrada pelo usuário."
            )

            print(
                "\nEncerrando o TechNova "
                "RAG Assistant."
            )

            break

        if not question:
            print(
                "\nDigite uma pergunta válida."
            )
            continue

        print(
            "\nBuscando informações..."
        )

        try:
            result = ask_rag(question)

            print("\nAssistente:\n")
            print(result["answer"])

            show_sources(
                result["sources"]
            )

        except RAGException as error:
            logger.error(
                "Erro controlado: %s",
                error,
            )

            print(
                "\nNão foi possível processar "
                "sua pergunta."
            )

            print(
                f"Motivo: {error}"
            )

        except Exception:
            logger.exception(
                "Erro não tratado na aplicação."
            )

            print(
                "\nOcorreu um erro inesperado."
            )


if __name__ == "__main__":
    main()
