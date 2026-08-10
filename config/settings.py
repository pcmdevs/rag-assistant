import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

DOCUMENTS_DIR = BASE_DIR / "documents"
DATABASE_DIR = BASE_DIR / "database"
LOGS_DIR = BASE_DIR / "logs"

load_dotenv(ENV_PATH)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHAT_MODEL = os.getenv(
    "CHAT_MODEL",
    "gemini-3.6-flash",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "gemini-embedding-001",
)


TOP_K = int(
    os.getenv("TOP_K", "4")
)

RELEVANCE_THRESHOLD = float(
    os.getenv("RELEVANCE_THRESHOLD", "0.55")
)

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", "1000")
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", "200")
)


def validate_settings() -> None:
    """
    Valida as configurações obrigatórias
    antes da aplicação iniciar.
    """

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY não encontrada. "
            "Configure a chave no arquivo .env."
        )


def create_project_directories() -> None:
    """
    Cria os diretórios necessários
    caso ainda não existam.
    """

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
