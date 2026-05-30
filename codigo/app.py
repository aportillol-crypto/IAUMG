from flask import Flask
from config.database import init_db
from config.cache import init_cache
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp


def create_app() -> Flask:
    """Factory de la aplicacion Flask."""
    app = Flask(__name__)

    init_db(app)
    init_cache(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
