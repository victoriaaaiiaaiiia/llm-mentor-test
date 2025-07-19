from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, I'm your chatbot!"}

#example from FastAPI site
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


class PromptRequest(BaseModel):
    prompt: str

class GeminiResponse(BaseModel):
    response: str

def gemini_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text  # .text returns the generated string content
    except Exception as e:
        # Optional: log or print the error for debugging
        print(f"[Gemini API Error] {e}")
        raise

@app.post("/api/generate-response", response_model=GeminiResponse)
async def generate_response_endpoint(req: PromptRequest):
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        text = gemini_response(prompt)
        return {"response": text}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

