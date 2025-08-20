from flask import Blueprint
from ..services.news_service import get_latest_news
from ..services.post_service import insert_article_if_not_exists, add_fields_in_db_post_document, update_posted_status
from ..services.gemini import get_gemini_response
from ..utils.formatting import format_article_to_post
import json
import time
from ..services.twitter import post_tweet_with_image_url
from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/post-everything-new", methods=["POST"])
def post_everything_new():
    news = get_latest_news()

    for article in news:
        insert_article_if_not_exists(article)
        gemini_respose =  get_gemini_response(article)

        data = json.loads(gemini_respose)

        formated_post_content = format_article_to_post(data)
        post_tweet_with_image_url(formated_post_content, article["image_url"],f"Check it out 👇\n{article["news_url"]}")       

        update_posted_status(article["news_id"], True)
        add_fields_in_db_post_document(article["news_id"], data)
        time.sleep(5)

    return jsonify({"success": True, "message": "All articles posted successfully!"})

@main_bp.route("hi", methods=["GET"])
def hi():
    return jsonify({"message": "hi"})
