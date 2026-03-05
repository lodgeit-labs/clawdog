import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

print("Available Models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)