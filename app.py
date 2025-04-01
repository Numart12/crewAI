# app.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew
import uvicorn
import os

app = FastAPI()

# ✅ Дадаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Альбо ўкажы дакладны frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck
@app.get("/")
def root():
    return {"message": "👋 CrewAI API is running!"}

# --- ASK ENDPOINT ---
class AskRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(request: AskRequest):
    question = request.question
    agent = Agent(
        role="AI Assistant",
        goal="Answer business-related questions and assist with client requests",
        backstory="You're Arthur, an AI assistant built by TechTask. You're helpful, polite and smart.",
        verbose=True
    )
    task = Task(description=question, agent=agent)
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.run()
    return {"question": question, "answer": result}

# --- /agents ENDPOINT ---
@app.get("/agents")
def get_agents():
    return [{
        "role": "AI Assistant",
        "goal": "Answer business-related questions",
        "backstory": "You're Arthur, an AI assistant built by TechTask."
    }]

# --- /tools ENDPOINT ---
@app.get("/tools")
def get_tools():
    return [{
        "name": "DefaultTool",
        "description": "No custom tools yet."
    }]

# --- /crews ENDPOINT ---
@app.get("/crews")
def get_crews():
    return [{
        "name": "DefaultCrew",
        "agents": ["AI Assistant"],
        "tasks": ["Answer questions"]
    }]
