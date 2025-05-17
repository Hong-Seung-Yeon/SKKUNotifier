from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/run")
def run_script():
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr
    }
