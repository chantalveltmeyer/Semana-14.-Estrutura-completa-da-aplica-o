import os
import requests

from datetime import datetime

from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import SQLAlchemy


# ==========================================================
# CARREGA VARIÁVEIS DO .ENV
# ==========================================================

load_dotenv()


# ==========================================================
# APLICAÇÃO
# ==========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "flasky-aula-070"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# ==========================================================
# CONFIGURAÇÃO DO SISTEMA
# ==========================================================

MAILGUN_API_KEY = os.environ.get(
    "MAILGUN_API_KEY"
)

MAILGUN_DOMAIN = os.environ.get(
    "MAILGUN_DOMAIN"
)

# No .env a variável se chama MAILGUN_FROM
EMAIL_REMETENTE = os.environ.get(
    "MAILGUN_FROM"
)

# E-mail institucional
EMAIL_INSTITUCIONAL = os.environ.get(
    "EMAIL_INSTITUCIONAL"
)

# E-mail do administrador
EMAIL_ADMIN = "flaskaulasweb@zohomail.com"

# Prontuário do aluno
PRONTUARIO = os.environ.get(
    "PRONTUARIO"
)


# ==========================================================
# MODELO USUÁRIO
# ==========================================================

class Usuario(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(200),
        nullable=False
    )


# ==========================================================
# MODELO E-MAIL
# ==========================================================

class EmailEnviado(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    remetente = db.Column(
        db.String(200),
        nullable=False
    )

    destinatarios = db.Column(
        db.Text,
        nullable=False
    )

    assunto = db.Column(
        db.String(300),
        nullable=False
    )

    texto = db.Column(
        db.Text,
        nullable=False
    )

    data_hora = db.Column(
        db.DateTime,
        default=datetime.now,
        nullable=False
    )


# ==========================================================
# ENVIO DE E-MAIL PELO MAILGUN
# ==========================================================

def enviar_email(nome):

    # ------------------------------------------------------
    # VERIFICA CONFIGURAÇÕES
    # ------------------------------------------------------

    if not MAILGUN_API_KEY:

        raise Exception(
            "MAILGUN_API_KEY não está configurada."
        )

    if not MAILGUN_DOMAIN:

        raise Exception(
            "MAILGUN_DOMAIN não está configurado."
        )

    if not EMAIL_REMETENTE:

        raise Exception(
            "MAILGUN_FROM não está configurado."
        )

    if not EMAIL_INSTITUCIONAL:

        raise Exception(
            "EMAIL_INSTITUCIONAL não está configurado."
        )

    if not PRONTUARIO:

        raise Exception(
            "PRONTUARIO não está configurado."
        )


    # ------------------------------------------------------
    # ASSUNTO
    # ------------------------------------------------------

    assunto = "[Flasky] Novo usuário cadastrado"


    # ------------------------------------------------------
    # CORPO DO E-MAIL
    # ------------------------------------------------------

    texto = f"""
Novo usuário cadastrado no sistema.

Prontuário: {PRONTUARIO}
Nome do aluno: {nome}
Usuário cadastrado: {nome}

Sistema: Avaliação contínua - Aula 070
"""


    # ------------------------------------------------------
    # DESTINATÁRIO PRINCIPAL
    # ------------------------------------------------------

    destinatarios = [
        EMAIL_INSTITUCIONAL
    ]


    # ------------------------------------------------------
    # VERIFICA CHECKBOX
    # ------------------------------------------------------

    enviar_admin = request.form.get(
        "enviar_email"
    )


    if enviar_admin:

        destinatarios.append(
            EMAIL_ADMIN
        )


    # ------------------------------------------------------
    # DIAGNÓSTICO
    # ------------------------------------------------------

    print("======================================")
    print("DIAGNÓSTICO MAILGUN")
    print(
        "API KEY CONFIGURADA:",
        bool(MAILGUN_API_KEY)
    )
    print(
        "DOMAIN:",
        MAILGUN_DOMAIN
    )
    print(
        "FROM:",
        EMAIL_REMETENTE
    )
    print(
        "DESTINATÁRIOS:",
        destinatarios
    )
    print("======================================")


    # ------------------------------------------------------
    # URL DO MAILGUN
    # ------------------------------------------------------

    url = (
        f"https://api.mailgun.net/v3/"
        f"{MAILGUN_DOMAIN}/messages"
    )


    # ------------------------------------------------------
    # ENVIO
    # ------------------------------------------------------

    try:

        resposta = requests.post(

            url,

            auth=(
                "api",
                MAILGUN_API_KEY
            ),

            data={

                "from": EMAIL_REMETENTE,

                "to": destinatarios,

                "subject": assunto,

                "text": texto

            },

            timeout=30

        )

    except requests.exceptions.RequestException as erro:

        raise Exception(
            f"Erro de conexão com o Mailgun: {erro}"
        )


    # ------------------------------------------------------
    # VERIFICA RESPOSTA DO MAILGUN
    # ------------------------------------------------------

    if resposta.status_code != 200:

        raise Exception(

            "Mailgun retornou "
            f"{resposta.status_code}: "
            f"{resposta.text}"

        )


    # ------------------------------------------------------
    # SALVA O E-MAIL NO BANCO
    # ------------------------------------------------------

    registro = EmailEnviado(

        # Aqui estava incorreto:
        # antes estava sendo salvo o nome do aluno.
        remetente=EMAIL_REMETENTE,

        destinatarios=str(
            destinatarios
        ),

        assunto=assunto,

        texto=texto,

        data_hora=datetime.now()

    )


    db.session.add(
        registro
    )

    db.session.commit()


    # ------------------------------------------------------
    # RETORNA RESPOSTA
    # ------------------------------------------------------

    return resposta.json()


# ==========================================================
# HOME
# ==========================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def index():

    # ------------------------------------------------------
    # POST
    # ------------------------------------------------------

    if request.method == "POST":

        nome = request.form.get(
            "nome",
            ""
        ).strip()


        # --------------------------------------------------
        # VALIDA NOME
        # --------------------------------------------------

        if not nome:

            flash(
                "Informe o seu nome.",
                "danger"
            )

            return redirect(
                url_for("index")
            )


        # --------------------------------------------------
        # CADASTRA USUÁRIO
        # --------------------------------------------------

        usuario = Usuario(
            nome=nome
        )

        db.session.add(
            usuario
        )

        db.session.commit()


        # --------------------------------------------------
        # ENVIA E-MAIL
        # --------------------------------------------------

        try:

            resultado = enviar_email(
                nome
            )

            print(
                "MAILGUN:",
                resultado
            )


            flash(
                "Usuário cadastrado e "
                "e-mail enviado com sucesso!",
                "success"
            )


        except Exception as erro:

            # ------------------------------------------------
            # MOSTRA ERRO
            # ------------------------------------------------

            print(
                "ERRO AO ENVIAR E-MAIL:",
                repr(erro)
            )


            flash(

                "Usuário cadastrado, "
                "mas o e-mail não foi enviado. "
                f"Erro: {erro}",

                "danger"

            )


        # --------------------------------------------------
        # VOLTA PARA HOME
        # --------------------------------------------------

        return redirect(
            url_for("index")
        )


    # ------------------------------------------------------
    # LISTA USUÁRIOS
    # ------------------------------------------------------

    usuarios = Usuario.query.order_by(
        Usuario.id
    ).all()


    return render_template(
        "index.html",
        usuarios=usuarios
    )


# ==========================================================
# E-MAILS ENVIADOS
# ==========================================================

@app.route(
    "/emailsEnviados"
)
def emails_enviados():

    emails = EmailEnviado.query.order_by(
        EmailEnviado.data_hora.desc()
    ).all()


    return render_template(
        "emails.html",
        emails=emails
    )


# ==========================================================
# CRIA BANCO DE DADOS
# ==========================================================

with app.app_context():

    db.create_all()


# ==========================================================
# EXECUÇÃO LOCAL
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
