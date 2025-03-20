from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.sweetisland.info"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "GPT API is running!"}

@app.post('/chat')
async def chat(question: Question):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': question.prompt}]
    )
    return {'answer': completion.choices[0].message.content.strip()}
