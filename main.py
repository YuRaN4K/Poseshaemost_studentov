from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from aiogram import Bot, Dispatcher
from pydantic import BaseModel
from typing import Optional, Annotated
from contextlib import asynccontextmanager

TELEGRAM_TOKEN = '8351097187:AAHIx9HU7FLOA2Dm3kGb0ZA_5D-Qax6vFg8'

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)




@asynccontextmanager
async lifespan(FastAPI):



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
