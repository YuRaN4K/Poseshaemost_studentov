from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, Annotated

app = FastAPI()

class Task(BaseModel):
    name: str
    description: Optional[str] = None

class STaskAdd(BaseModel):
    id: int

tasks = []

@app.post("/tasks")
async def add_task(
    task: Annotated[Task, Depends()],
):
    tasks.append(task)
    return {"ok": True}

# @app.get("/tasks")
# def get_tasks():
#     task = Task(name="Write this one")
#     return {"data": task}
