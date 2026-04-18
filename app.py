from flask import Flask
from config import Config
from extensions import db, jwt, bcrypt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── Initialise extensions ────────────────────────
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # ── Register blueprints ──────────────────────────
    from auth.routes     import auth_bp
    from frontend.routes import frontend_bp
    from admin.routes    import admin_bp
    from crypto.routes   import crypto_bp
    from fraud.routes    import fraud_bp
    from receipts.routes import receipts_bp

    app.register_blueprint(auth_bp,     url_prefix="/api/auth")
    app.register_blueprint(crypto_bp,   url_prefix="/api/crypto")
    app.register_blueprint(fraud_bp,    url_prefix="/api/fraud")
    app.register_blueprint(receipts_bp, url_prefix="/api/receipts")
    app.register_blueprint(frontend_bp)
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # ── Create tables ────────────────────────────────
    with app.app_context():
        import models   # noqa: F401 — ensure models are registered
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
