from config.settings import (
    CHAT_MODEL,
    EMBEDDING_MODEL,
    DATABASE_DIR,
    DOCUMENTS_DIR,
    LOGS_DIR,
    TOP_K,
    RELEVANCE_THRESHOLD,
    validate_settings,
    create_project_directories,
)


def main():

    validate_settings()

    create_project_directories()

    print("\nConfigurações carregadas com sucesso!\n")

    print(f"Chat model: {CHAT_MODEL}")
    print(f"Embedding model: {EMBEDDING_MODEL}")

    print(f"\nBanco vetorial:")
    print(DATABASE_DIR)

    print(f"\nDocumentos:")
    print(DOCUMENTS_DIR)

    print(f"\nLogs:")
    print(LOGS_DIR)

    print(f"\nTop K: {TOP_K}")
    print(f"Threshold: {RELEVANCE_THRESHOLD}")


if __name__ == "__main__":
    main()
