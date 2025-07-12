from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
from fastapi import WebSocket

app = FastAPI()

# Allow frontend to connect to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for expected JSON input
class CommandRequest(BaseModel):
    command: str

# Endpoint to execute the shell command
@app.post("/execute")
async def execute_command(cmd: CommandRequest):
    try:
        result = subprocess.run(
            cmd.command,
            shell=True,
            capture_output=True,
            text=True
        )
        return {
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None
        }

    except Exception as e:
        return {
            "output": "",
            "error": str(e)
        }


# === HTTP GET ROUTE ===
# route for the root url
@app.get("/")
def read_root():
    return {"message": "hello from server"}

# run "uvicorn filename:app --reload" in the terminal and open the local host via browser

# === WEBSOCKET ROUTE ===
# this route listens for WebSocket connections on the path "/ws"

@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    await websocket.send_text("WebSocket connection establised")

    while True:
        data=await websocket.receive_text()
        await websocket.send_text(f"you said: {data}")

