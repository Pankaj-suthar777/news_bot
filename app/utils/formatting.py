from ..services.gemini import GeminiResponse

def format_article_to_post(gemini_response: GeminiResponse) -> str:
    news_string = (
        f'{gemini_response["body"]}\n\n'
        f'{gemini_response["hashtags"]}\n'
    )
    return news_string