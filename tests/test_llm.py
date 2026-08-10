from src.llm import get_llm


def main():
    print("\nCriando modelo de linguagem...")

    llm = get_llm()

    print("Enviando pergunta de teste...")

    response = llm.invoke(
        "Responda apenas com a palavra OK."
    )

    print("\nResposta recebida:")
    print(response.text)


if __name__ == "__main__":
    main()
