from flask import Blueprint, jsonify
from ..services.news_service import get_latest_news
news_bp = Blueprint("news", __name__)

@news_bp.route("/", methods=["GET"])
def get_news_data():
    # Call your existing service logic
    data = get_latest_news()
    return jsonify({"articles": data})
