import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-temporaria")

    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.db")
    )

    DATABASE = DATABASE_PATH

    STUDENT_NAME = os.environ.get(
        "STUDENT_NAME",
        "Chantal Nicole Veltmeyer Souza"
    )

    STUDENT_RECORD = os.environ.get(
        "STUDENT_RECORD",
        os.environ.get("PRONTUARIO", "PT3039471")
    )

    INSTITUTIONAL_EMAIL = os.environ.get(
        "INSTITUTIONAL_EMAIL",
        "chantal.veltmeyer@aluno.ifsp.edu.br"
    )

    EMAIL_PROVIDER = os.environ.get("EMAIL_PROVIDER", "mailgun")
    EMAIL_API_KEY = os.environ.get("EMAIL_API_KEY")
    EMAIL_FROM = os.environ.get("EMAIL_FROM")

    ADMIN_EMAIL = os.environ.get(
        "ADMIN_EMAIL",
        "flaskaulasweb@zohomail.com"
    )

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_BASE = os.environ.get(
        "MAILGUN_API_BASE",
        "https://api.mailgun.net"
    )
