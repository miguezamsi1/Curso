from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from .config import Config


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(config_class: type[Config] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from . import models  # noqa: F401  # Import models for SQLAlchemy
    from .routes import main_bp

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_year() -> dict[str, int]:
        from datetime import datetime

        return {"current_year": datetime.utcnow().year}

    return app
