from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# 연결된 클라이언트 저장
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 받은 메시지를 모든 클라이언트에게 전송
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
