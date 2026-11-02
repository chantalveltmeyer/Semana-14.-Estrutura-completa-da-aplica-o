# Semana 14 — Aplicação Flask modular

Aplicação de cadastro, listagem, edição e exclusão de usuários, com banco SQLite e notificações por e-mail via Resend.

## Estrutura

- `flasky.py`: ponto de entrada local.
- `config.py`: configurações e variáveis de ambiente.
- `app/__init__.py`: criação e configuração da aplicação.
- `app/routes.py`: rotas e operações CRUD.
- `app/database.py`: conexão e inicialização do SQLite.
- `app/email_service.py`: integração com Resend.
- `app/templates/`: páginas HTML.
- `app/static/style.css`: estilos.

## Executar localmente

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python flasky.py
```

Acesse `http://127.0.0.1:5000`.

## Configurar o Resend

1. Crie/acesse sua conta em https://resend.com/.
2. Gere uma API Key.
3. Verifique um domínio ou remetente autorizado no Resend.
4. Configure no ambiente do PythonAnywhere:
   - `RESEND_API_KEY`: sua chave privada.
   - `MAIL_FROM`: remetente autorizado no formato `Nome <email@seudominio.com>`.
   - `ADMIN_EMAIL`: `flaskaulasweb@zohomail.com`.
   - `INSTITUTIONAL_EMAIL`: seu e-mail institucional.
   - `STUDENT_NAME`: nome completo.
   - `PRONTUARIO`: prontuário.
   - `SECRET_KEY`: uma chave aleatória forte.
   - `DATABASE_PATH`: caminho absoluto do banco SQLite.

**Importante:** não publique a API Key no GitHub nem a coloque diretamente no código. O remetente de teste `onboarding@resend.dev` possui restrições; para enviar para destinatários externos, configure e valide um domínio/remetente conforme as regras atuais do Resend.

O cadastro é gravado mesmo se o serviço de e-mail ainda não estiver configurado. Nesse caso, a página informa que as notificações não foram enviadas.

## Publicar no PythonAnywhere

1. Envie os arquivos e pastas deste ZIP para `/home/ChantalVeltmeyer/mysite/`.
2. Abra um Bash console e execute:

```bash
cd /home/ChantalVeltmeyer/mysite
pip install --user -r requirements.txt
```

3. No painel **Web**, configure o virtualenv se estiver usando um.
4. No arquivo WSGI, mantenha o caminho e use:

```python
import sys
path = '/home/ChantalVeltmeyer/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

from flasky import app as application
```

5. Em **Web > Environment variables**, cadastre as variáveis indicadas acima.
6. Confirme que `DATABASE_PATH` aponta para um arquivo dentro de `mysite`.
7. Clique em **Reload**.

## Funcionalidades

- Cadastro com nome, usuário, e-mail, senha e função.
- Senhas armazenadas com hash, nunca em texto puro.
- Aviso de novo cadastro para o administrador, endereço institucional e e-mail informado.
- E-mail contém Prontuário, nome do aluno e usuário cadastrado.
- Edição de dados e troca opcional de senha.
- Exclusão com confirmação no navegador.

## Observação de segurança

Esta versão didática implementa o CRUD solicitado, mas não inclui autenticação/autorização administrativa. Antes de usar publicamente, proteja as rotas de edição e exclusão com login e controle de acesso.
