from google import genai
from google.genai import types
from ..config import GEMINI_API_KEY
from typing import TypedDict
from ..services.system_instruction import SYSTEM_INSTRUCTION
from ..types.news import News

class GeminiResponse(TypedDict):
    body: str
    hashtags: str

client = genai.Client(api_key=GEMINI_API_KEY)

def get_gemini_response(artical: News) -> GeminiResponse:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Title: {artical['title']}\nContent: {artical['content']}",
        config=types.GenerateContentConfig(
             system_instruction=SYSTEM_INSTRUCTION,
            # thinking_config=types.ThinkingConfig(thinking_budget=0)  
        ),
        
    )
    return response.text