from flask import Flask
from . import config

# try:
#     get_latest_news()
# except RuntimeError as e:
#     print(f"Error: {e}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    from .routes.news import news_bp
    from .routes.main import main_bp

    app.register_blueprint(news_bp, url_prefix="/news")
    app.register_blueprint(main_bp, url_prefix="/main")

    return app
