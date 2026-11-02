import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("MAILGUN_API_KEY")
dominio = os.environ.get("MAILGUN_DOMAIN")

url = f"https://api.mailgun.net/v3/{dominio}/messages"

dados = {
    "from": f"FlaskyApp <postmaster@{dominio}>",
    "to": "chantal.veltmeyer@aluno.ifsp.edu.br",
    "subject": "Teste FlaskyApp - Mailgun",
    "text": "Este é um teste de envio pelo Mailgun."
}

resposta = requests.post(
    url,
    auth=("api", api_key),
    data=dados,
    timeout=30
)

print("STATUS:", resposta.status_code)
print("RESPOSTA:", resposta.text)
