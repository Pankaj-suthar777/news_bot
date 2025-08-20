from typing import TypedDict

class News(TypedDict):
    news_id: int
    title: str
    description: str
    news_url: str
    image_url: str
    content: str
    is_posted: bool