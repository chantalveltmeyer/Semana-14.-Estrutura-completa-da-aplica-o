from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from sqlite3 import IntegrityError
from .database import get_db
from .email_service import send_new_user_notification

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "User").strip()

        if not all([name, username, email, password]):
            flash("Preencha todos os campos obrigatórios.", "error")
        elif role not in ("Admin", "User"):
            flash("Função inválida.", "error")
        else:
            try:
                db.execute(
                    """INSERT INTO users (name, username, email, password_hash, role)
                       VALUES (?, ?, ?, ?, ?)""",
                    (name, username, email, generate_password_hash(password), role)
                )
                db.commit()
                user = {"name": name, "username": username, "email": email}
                ok, message = send_new_user_notification(user)
                flash(message, "success" if ok else "warning")
                return redirect(url_for("main.index"))
            except IntegrityError:
                db.rollback()
                flash("Este nome de usuário já está cadastrado.", "error")

    users = db.execute(
        "SELECT id, name, username, email, role FROM users ORDER BY id"
    ).fetchall()
    return render_template("index.html", users=users)

@main.route("/editar/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    db = get_db()
    user = db.execute(
        "SELECT id, name, username, email, role FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    if user is None:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "User").strip()
        password = request.form.get("password", "")

        if not all([name, username, email]) or role not in ("Admin", "User"):
            flash("Confira os campos obrigatórios.", "error")
            return render_template("edit.html", user=user)

        try:
            if password:
                db.execute(
                    """UPDATE users SET name=?, username=?, email=?, role=?,
                       password_hash=? WHERE id=?""",
                    (name, username, email, role, generate_password_hash(password), user_id)
                )
            else:
                db.execute(
                    "UPDATE users SET name=?, username=?, email=?, role=? WHERE id=?",
                    (name, username, email, role, user_id)
                )
            db.commit()
            flash("Usuário atualizado com sucesso.", "success")
            return redirect(url_for("main.index"))
        except IntegrityError:
            db.rollback()
            flash("Esse nome de usuário já pertence a outra conta.", "error")

    return render_template("edit.html", user=user)

@main.route("/excluir/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    flash("Usuário excluído.", "success")
    return redirect(url_for("main.index"))
