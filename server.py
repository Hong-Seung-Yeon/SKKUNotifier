# server.py
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import subprocess

app = FastAPI()

@app.get("/run", response_class=PlainTextResponse)
def run_script():
    print("🚀 main.py 실행 시작")
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    print("📤 stdout:\n", result.stdout)
    print("📛 stderr:\n", result.stderr)
    return result.stdout + "\n" + result.stderr
