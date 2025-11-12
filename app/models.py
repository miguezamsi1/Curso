from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .config import Config


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expira = db.Column(db.DateTime, nullable=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def establecer_contrasena(self, contrasena: str) -> None:
        self.contrasena_hash = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena: str) -> bool:
        return check_password_hash(self.contrasena_hash, contrasena)

    def generar_token_recuperacion(self) -> str:
        serializer = URLSafeTimedSerializer(Config.SECURITY_PASSWORD_SALT)
        token = serializer.dumps({"user_id": self.id})
        self.reset_token = token
        self.reset_token_expira = datetime.utcnow()
        return token

    @staticmethod
    def validar_token_recuperacion(token: str, max_age_minutes: int) -> int | None:
        serializer = URLSafeTimedSerializer(Config.SECURITY_PASSWORD_SALT)
        try:
            data = serializer.loads(token, max_age=max_age_minutes * 60)
            return data.get("user_id")
        except Exception:  # noqa: BLE001
            return None
