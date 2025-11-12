from datetime import datetime, timedelta

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_mail import Message

from . import db, mail
from .models import Usuario


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/registro", methods=["GET", "POST"])
def registrar_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")

        if not all([nombre, correo, contrasena]):
            flash("Todos los campos son obligatorios.", "danger")
            return render_template("registro.html")

        if Usuario.query.filter_by(correo=correo).first():
            flash("El correo ya está registrado.", "warning")
            return render_template("registro.html")

        usuario = Usuario(nombre=nombre, correo=correo)
        usuario.establecer_contrasena(contrasena)
        db.session.add(usuario)
        db.session.commit()

        flash("Usuario registrado correctamente.", "success")
        return redirect(url_for("main.index"))

    return render_template("registro.html")


@main_bp.route("/olvide-contrasena", methods=["GET", "POST"])
def solicitar_recuperacion():
    if request.method == "POST":
        correo = request.form.get("correo")
        usuario = Usuario.query.filter_by(correo=correo).first()

        if not usuario:
            flash("No se encontró un usuario con ese correo.", "warning")
            return render_template("olvide_contrasena.html")

        token = usuario.generar_token_recuperacion()
        usuario.reset_token_expira = datetime.utcnow()
        db.session.commit()

        enlace = url_for("main.restablecer_contrasena", token=token, _external=True)
        enviar_correo(
            asunto="Recuperación de contraseña",
            destinatario=usuario.correo,
            plantilla="correo_recuperacion.html",
            usuario=usuario,
            enlace=enlace,
        )

        flash("Se envió un correo con las instrucciones.", "info")
        return redirect(url_for("main.index"))

    return render_template("olvide_contrasena.html")


@main_bp.route("/restablecer/<token>", methods=["GET", "POST"])
def restablecer_contrasena(token: str):
    max_age = current_app.config["PASSWORD_RESET_TOKEN_EXPIRATION"]
    usuario_id = Usuario.validar_token_recuperacion(token, max_age)

    if not usuario_id:
        flash("El enlace de recuperación no es válido o ha expirado.", "danger")
        return redirect(url_for("main.solicitar_recuperacion"))

    usuario = Usuario.query.get(usuario_id)

    if not usuario or usuario.reset_token != token:
        flash("El enlace de recuperación no es válido.", "danger")
        return redirect(url_for("main.solicitar_recuperacion"))

    if request.method == "POST":
        contrasena = request.form.get("contrasena")
        confirmar = request.form.get("confirmar")

        if contrasena != confirmar:
            flash("Las contraseñas no coinciden.", "warning")
            return render_template("restablecer_contrasena.html", token=token)

        usuario.establecer_contrasena(contrasena)
        usuario.reset_token = None
        usuario.reset_token_expira = None
        db.session.commit()

        flash("La contraseña se actualizó correctamente.", "success")
        return redirect(url_for("main.index"))

    token_expira = usuario.reset_token_expira or datetime.utcnow()
    if datetime.utcnow() - token_expira > timedelta(minutes=max_age):
        flash("El enlace ha expirado, solicita uno nuevo.", "danger")
        usuario.reset_token = None
        usuario.reset_token_expira = None
        db.session.commit()
        return redirect(url_for("main.solicitar_recuperacion"))

    return render_template("restablecer_contrasena.html", token=token)


def enviar_correo(asunto: str, destinatario: str, plantilla: str, **contexto) -> None:
    configurado = current_app.config.get("MAIL_SERVER") and current_app.config.get("MAIL_USERNAME")
    if not configurado or current_app.config.get("MAIL_SUPPRESS_SEND"):
        current_app.logger.warning("Servidor de correo no configurado o envío suprimido. Se omite el envío real.")
        return

    mensaje = Message(asunto, recipients=[destinatario])
    mensaje.html = render_template(plantilla, **contexto)
    mail.send(mensaje)
