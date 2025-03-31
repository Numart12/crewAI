from fastapi import FastAPI, Request
from pydantic import BaseModel
from crewai import Agent, Task, Crew
import uvicorn
import os

# Стварыць FastAPI-дадатак
app = FastAPI()

# Вынік для GET-запыту (праверка)
@app.get("/")
def root():
    return {"message": "👋 CrewAI API is running!"}

# Клас для ўваходных дадзеных
class AskRequest(BaseModel):
    question: str

# POST-эндпойнт для звароту да CrewAI
@app.post("/ask")
async def ask_agent(request: AskRequest):
    question = request.question

    # Агент
    agent = Agent(
        role="AI Assistant",
        goal="Answer business-related questions and assist with client requests",
        backstory="You're Arthur, an AI assistant built by TechTask. You're helpful, polite and smart.",
        verbose=True
    )

    # Задача
    task = Task(
        description=question,
        agent=agent
    )

    # Crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.run()
    return {"question": question, "answer": result}