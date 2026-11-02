import requests
from flask import current_app


def send_new_user_notification(user):
    cfg = current_app.config

    api_key = cfg.get("EMAIL_API_KEY")
    domain = cfg.get("MAILGUN_DOMAIN")
    mail_from = cfg.get("EMAIL_FROM")

    api_base = cfg.get(
        "MAILGUN_API_BASE",
        "https://api.mailgun.net"
    )

    if not all([api_key, domain, mail_from]):
        current_app.logger.error(
            "Configuração do Mailgun incompleta."
        )
        return False, "Cadastro realizado, mas o Mailgun não está configurado."

    recipients = []

    for address in (
        cfg.get("ADMIN_EMAIL"),
        cfg.get("INSTITUTIONAL_EMAIL"),
        user.get("email")
    ):
        if address and address not in recipients:
            recipients.append(address)

    body = (
        "Um novo usuário foi cadastrado na aplicação.\n\n"
        f"Prontuário: {cfg.get('STUDENT_RECORD')}\n"
        f"Nome do aluno: {cfg.get('STUDENT_NAME')}\n"
        f"Usuário cadastrado: {user.get('username')}\n"
        f"Nome: {user.get('name')}\n"
        f"E-mail informado: {user.get('email')}\n"
    )

    try:
        response = requests.post(
            f"{api_base.rstrip('/')}/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": mail_from,
                "to": recipients,
                "subject": "Novo usuário cadastrado - Semana 14",
                "text": body
            },
            timeout=20
        )

        response.raise_for_status()

        current_app.logger.info(
            "Solicitação aceita pelo Mailgun: %s",
            response.text
        )

        return True, "Cadastro realizado e notificações enviadas."

    except requests.RequestException:
        current_app.logger.exception(
            "Falha no envio de e-mail pelo Mailgun."
        )
        return False, "Cadastro realizado, mas houve falha no envio dos e-mails."
