from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env variables
load_dotenv()

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found in .env")

# Configure Gemini SDK
genai.configure(api_key=GOOGLE_API_KEY)

# List available models
models = genai.list_models()

# Print them
for model in models:
    print(f"{model.name} -> {model.supported_generation_methods}")
