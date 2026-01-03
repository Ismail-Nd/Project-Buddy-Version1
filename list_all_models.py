import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY not found in .env")
else:
    genai.configure(api_key=API_KEY)
    print("Listing all models...")
    try:
        for m in genai.list_models():
            print(f"Name: {m.name}")
            print(f"Supported Methods: {m.supported_generation_methods}")
            print("-" * 20)
    except Exception as e:
        print(f"Error listing models: {e}")
