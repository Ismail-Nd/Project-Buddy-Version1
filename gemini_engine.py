import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the API Key
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def get_intent_ai(text):
    """
    Uses Gemini to interpret user intent from potentially noisy speech-to-text.
    Returns: { "type": "OPEN_APP" | "SEARCH" | "UNKNOWN", "target": "query/app" }
    """
    if not API_KEY:
        return {"type": "ERROR", "target": "API Key not set"}

    model = genai.GenerativeModel('gemini-flash-latest') # Verified working free tier alias
    
    prompt = f"""
    You are a voice assistant intent parser. 
    The following text comes from a speech recognizer and might have phonetic errors.
    
    User Spoke: "{text}"
    
    Tasks:
    1. Correct phonetic errors (e.g., "hoping you tube" -> "open youtube").
    2. Identify the intent:
       - OPEN_APP: If user wants to open a platform (youtube, gmail, chrome, etc) or app (notepad, calc).
       - SEARCH: If user is asking a question or wants to search something (e.g., "whats trending in tech").
       - UNKNOWN: If you can't satisfy the request.
    
    Return ONLY a valid JSON object. No extra text.
    Example 1: {{"type": "OPEN_APP", "target": "youtube"}}
    Example 2: {{"type": "SEARCH", "target": "latest tech trends 2024"}}
    Example 3: {{"type": "OPEN_APP", "target": "notepad"}}
    """

    try:
        response = model.generate_content(prompt)
        # Extract JSON from response text (Gemini sometimes wraps in code blocks)
        content = response.text.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        
        return json.loads(content)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {"type": "ERROR", "target": str(e)}
