# server.py
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

clients = []

@app.get("/")
async def root():
    return {"message": "Server is running!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=10000)
