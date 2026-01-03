import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY not found in .env")
else:
    genai.configure(api_key=API_KEY)
    test_models = [
        'gemini-flash-latest', 
        'gemini-flash-lite-latest', 
        'gemini-2.5-flash',
        'gemini-pro-latest'
    ]
    
    print("Testing models for quota...")
    for model_name in test_models:
        try:
            print(f"Checking {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi", generation_config={"max_output_tokens": 5})
            print(f"SUCCESS: {model_name} works!")
            with open("working_model.txt", "w") as f:
                f.write(model_name)
            break
        except Exception as e:
            print(f"FAILED: {model_name} - {str(e)[:100]}")
