from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
from crewai import Agent, Task, Crew
import os

app = FastAPI()

# 🔸 Праверка працы API
@app.get("/")
def root():
    return {"message": "👋 CrewAI API is running!"}

# 🔹 Уваходная мадэль для /ask
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

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.run()
    return {"question": question, "answer": result}


# 🧠 Агенты
agents_storage = []

class AgentInput(BaseModel):
    role: str
    goal: str
    backstory: Optional[str] = None

@app.get("/agents")
def list_agents():
    return {"agents": agents_storage}

@app.post("/agents")
def create_agent(agent: AgentInput):
    agents_storage.append(agent.dict())
    return {"message": "Agent created", "agent": agent}


# 🔧 Інструменты (пакуль пуста)
@app.get("/tools")
def list_tools():
    return {"tools": []}


# 🤝 Стварэнне Crew (з умовай, што ёсць хаця б адзін агент)
class CrewInput(BaseModel):
    task_description: str

@app.post("/crews")
def run_crew(input: CrewInput):
    if not agents_storage:
        return {"error": "No agents created yet"}

    agents = [
        Agent(
            role=a["role"],
            goal=a["goal"],
            backstory=a.get("backstory", ""),
            verbose=True
        )
        for a in agents_storage
    ]

    task = Task(
        description=input.task_description,
        agent=agents[0]  # першы як асноўны
    )

    crew = Crew(agents=agents, tasks=[task], verbose=True)
    result = crew.run()
    return {"task": input.task_description, "result": result}
