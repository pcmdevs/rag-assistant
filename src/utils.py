import os

from dotenv import load_dotenv

load_dotenv()


def check_api_key():

    key = os.getenv("OPENAI_API_KEY")

    if not key:

        raise EnvironmentError(
            "OPENAI_API_KEY não encontrada."
        )

    return key