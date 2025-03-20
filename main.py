from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = "asst_9HbbmEDLTbMB47DotTIY0zcm" 

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
    return {"message": "Custom GPT Assistant is running!"}

@app.post('/chat')
async def chat(question: Question):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question.prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value.strip()

    return {"answer": response}
