from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from config.settings import (
    CHAT_MODEL,
    GEMINI_API_KEY,
    validate_settings,
)

from src.logger import get_logger
from src.exceptions import LLMError


logger = get_logger(__name__)


def get_llm() -> ChatGoogleGenerativeAI:
    """
    Cria e retorna o modelo Gemini.
    """

    try:
        validate_settings()

        logger.info(
            "Inicializando modelo de linguagem: %s",
            CHAT_MODEL,
        )

        return ChatGoogleGenerativeAI(
            model=CHAT_MODEL,
            google_api_key=GEMINI_API_KEY,
        )

    except Exception as error:
        logger.exception(
            "Erro ao inicializar o modelo de linguagem."
        )

        raise LLMError(
            "Não foi possível inicializar "
            "o modelo de linguagem."
        ) from error
