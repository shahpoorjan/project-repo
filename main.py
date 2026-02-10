from fastapi import FastAPI
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

with open('tasks.json', 'r') as f:
    tasks = json.load(f)
f.close()

@app.get("/hello")
def hello():
    return {"message": "Hello, world!"}

@app.post("/hello")
def create_user(user: UserData):
    print(user.name, user.age)
    return {"message": f"Hello, {user.name}. Your age is {user.age}!"}


# Yunus's task 2
@app.post('/generate_uuid_with_data/')
def generate_uuid_with_name(user: UserData):
    try:
        generated_uuid = uuid4()
        return {
            "message": f"Hello, {user.name}, Your age is {user.age}",
            "uuid": str(generated_uuid)
        }
    except:
        return {"message": "Error generating UUID and obtaining user data"}

 # Somon's task
@app.get('/ping/{hostname}')
def ping_host(hostname: str) -> bool:
    try:
        # -n for Windows, -c for Linux/macOS.
        if platform.system().lower() == 'windows':
            param = '-n'
        else:
            param = '-c'
        command = ['ping', param, '1', hostname]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

# Yunus's task
@app.get('/generate_uuid/')
def generate_uuid():
    try:
        generated_uuid = uuid4()
        return {"message": f"Your UUID is: {generated_uuid}"}
    except:
        return {"message": "Error generating UUID"}

# Elsu's task
@app.post("/listdir")
def list_dir(path: ListDirInput):
    try:
        files = os.listdir(path.input)  
        return {"files": files} 
    except:
        return {
            "Error": "There is some error, try again"
        }

# Jonathan's Task
@app.get("/get_public_ip")
def get_ip():
    try:
        pub_ip = requests.get('https://api.ipify.org')
        pub_ip = pub_ip.text
        return {"message": f"Your public IP address is: {pub_ip}"}
    except:
        return {"message": "Error fetching public IP"}
        
# Naza's Task - read_log_tail(filepath, lines)
@app.get("/read_log_tail(filepath, lines)")
def read_log_tail(filepath: str, lines: int = 5):
    try:
        # this opens the file for reading. "r" means read.
        file = open(filepath, "r") 
        content = file.readlines()
        last_lines = content[-lines:]
        return {"lines": last_lines}
    except FileNotFoundError:
        return {"error": "File not found. Check the path."}
        
# Meerim's task  check_disk_usage(path)

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
    except FileNotFoundError:
        return {"error": "Path does not exist"}
  

## abdul's task
@app.get("/tasks")
def list_tasks_data():
    try:
        return tasks
    except Exception as e:
        return {"error": str(e)}

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    try:
        task = tasks.get(task_id)
        if not task:
            return tasks
        return task
    except Exception as e:
        return {"error": str(e)}

@app.post("/tasks")
def get_task(task: TaskData):
    try:
        if task.id is not None:
            return {"error": f"Task with task ID {task.id} exists"}
        else:
            task.id = str(uuid4())
            tasks[task.id] = task.model_dump()
            with open('tasks.json', 'w') as f:
                f.write(json.dumps(tasks))
                f.close()
            return {"message": f"Task with id {task.id} created successfully", "task": tasks[task.id]}
    except Exception as e:
        return {"error": str(e)}

@app.put("/tasks/{task_id}")
def update_task(task_id: str, task: TaskData):
    try:
        if task_id not in tasks:
            return {"error": f"Task with id {task_id} not found"}
        for field, value in task.model_dump().items():
            if value is not None and field != "id":
                tasks[task_id][field] = value
        with open('tasks.json', 'w') as f:
            f.write(json.dumps(tasks))
        return {"message": f"Task with id {task_id} updated successfully", "task": tasks[task_id]}
    except Exception as e:

        return {"error": str(e)}

        # shah's Task
@app.get("/system_info")
def system_information():
    sys_info = {
        'System information':platform.system(),
        'Python Version':platform.python_version(),
        'Architecture': platform.architecture()
    }
    return(sys_info)

# Tugs's task
@app.get("/cpuLoadAverage")
def cpu_t():
    try:
        load_ave = os.getloadavg()
        print(f"Cpu load average last 1 minutes, 5 minutes, 15 minutes: {load_ave}")
        return f"Cpu load average last 1 minutes, 5 minutes, 15 minutes: {load_ave}"
    except:
        print("Try again")

        return "it should be good"

# Tugs task2

@app.post("/addnum")
def number(n1: int, n2: int) -> int:
    try:
        n1 = 100
        n2 = 101
        return n1 + n2
        print(n1 + n2)

    except ValueError:
        return
    print("Enter integer")