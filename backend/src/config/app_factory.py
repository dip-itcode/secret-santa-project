"""
Flask application factory.
"""
import os
from flask import Flask
from flask_cors import CORS

from src.routes import api_bp


def create_app(config: dict = None) -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ── Defaults ──────────────────────────────────
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "")

    if config:
        app.config.update(config)

    # ── Optional MongoDB ───────────────────────────
    mongo_uri = app.config.get("MONGO_URI")
    if mongo_uri:
        try:
            from src.services import MongoService
            mongo = MongoService(uri=mongo_uri)
            if mongo.ping():
                app.config["MONGO_SERVICE"] = mongo
                app.logger.info("MongoDB connected ✅")
            else:
                app.logger.warning("MongoDB ping failed — running without DB")
        except Exception as exc:
            app.logger.warning(f"MongoDB init failed: {exc}")

    app.register_blueprint(api_bp)
    return app
