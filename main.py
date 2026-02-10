from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import platform
import subprocess
import requests
from uuid import uuid4
import os
import shutil
from typing import Optional
import json

app = FastAPI()

# 🔹 Root redirect → /docs
@app.get("/")
def root():
    return RedirectResponse(url="/docs")

class UserData(BaseModel):
    name: str
    age: int

class ListDirInput(BaseModel):
    input: str

class TaskData(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee: Optional[str] = None

# Load tasks
with open('tasks.json', 'r') as f:
    tasks = json.load(f)

@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}

@app.post("/hello")
def create_user(user: UserData):
    return {"message": f"Hello, {user.name}. Your age is {user.age}!"}

@app.post('/generate_uuid_with_data/')
def generate_uuid_with_name(user: UserData):
    generated_uuid = uuid4()
    return {
        "message": f"Hello, {user.name}, Your age is {user.age}",
        "uuid": str(generated_uuid)
    }

@app.get('/ping/{hostname}')
def ping_host(hostname: str) -> bool:
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', hostname]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

@app.get('/generate_uuid/')
def generate_uuid():
    return {"uuid": str(uuid4())}

@app.post("/listdir")
def list_dir(path: ListDirInput):
    try:
        return {"files": os.listdir(path.input)}
    except:
        return {"error": "Directory read failed"}

@app.get("/get_public_ip")
def get_ip():
    try:
        pub_ip = requests.get('https://api.ipify.org').text
        return {"ip": pub_ip}
    except:
        return {"error": "Error fetching IP"}

@app.get("/disk-usage/")
def check_disk_usage(path: str = "/"):
    try:
        total, used, free = shutil.disk_usage(path)
        return {
            "path": path,
            "total_GB": round(total / (2**30), 2),
            "used_GB": round(used / (2**30), 2),
            "free_GB": round(free / (2**30), 2)
        }
    except:
        return {"error": "Invalid path"}

@app.get("/tasks")
def list_tasks_data():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    return tasks.get(task_id, {"error": "Task not found"})

@app.post("/tasks")
def create_task(task: TaskData):
    task.id = str(uuid4())
    tasks[task.id] = task.model_dump()
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
    return {"message": "Task created", "task": tasks[task.id]}

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: TaskData):
    if task_id not in tasks:
        return {"error": "Task not found"}
    for field, value in task.model_dump().items():
        if value is not None and field != "id":
            tasks[task_id][field] = value
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)
    return {"message": "Task updated", "task": tasks[task_id]}

@app.get("/system_info")
def system_information():
    return {
        "system": platform.system(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()
    }

@app.get("/cpuLoadAverage")
def cpu_t():
    try:
        return {"load_avg": os.getloadavg()}
    except:
        return {"error": "Unavailable"}

@app.post("/addnum")
def number(n1: int, n2: int):
    return n1 + n2
