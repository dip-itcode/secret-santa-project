"""
Application entry point.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from src.config.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
