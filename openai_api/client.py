import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_service_ai_value(service, category):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "IA não configurada"

    client = OpenAI(api_key=api_key)

    prompt = f"""
Me mostre uma descrição de venda para o serviço "{service}" na categoria "{category}",
destacando benefícios e diferenciais. Máx. 250 caracteres.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text