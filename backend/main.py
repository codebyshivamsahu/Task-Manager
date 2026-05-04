from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []
counter = 1

class Task(BaseModel):
    title: str

@app.get("/")
def root():
    return {"message": "Task Manager API is running 🚀"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def add_task(task: Task):
    global counter
    new_task = {"id": counter, "title": task.title, "completed": False}
    tasks.append(new_task)
    counter += 1
    return new_task

@app.put("/tasks/{task_id}")
def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return {"message": "Deleted"}