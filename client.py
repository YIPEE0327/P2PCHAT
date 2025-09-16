import tkinter as tk
import asyncio
import websockets
from datetime import datetime

SERVER_URL = "https://railway.com/project/802589bf-4e47-4222-aff3-c48653628e94"  # 배포 URL로 교체

class ChatClient:
    def __init__(self, root, nickname):
        self.root = root
        self.nickname = nickname
        self.root.title(f"Messenger - {nickname}")

        # 채팅창
        self.text_area = tk.Text(root, state="disabled", width=50, height=20)
        self.text_area.pack()

        # 입력창
        self.entry = tk.Entry(root, width=50)
        self.entry.pack()
        self.entry.bind("<Return>", self.send_message)

        # WebSocket 연결
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.connect())

    async def connect(self):
        self.websocket = await websockets.connect(SERVER_URL)
        asyncio.create_task(self.receive_messages())

    async def receive_messages(self):
        try:
            while True:
                msg = await self.websocket.recv()
                display = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n"
                self.text_area.config(state="normal")
                self.text_area.insert("end", display)
                self.text_area.config(state="disabled")
        except:
            self.text_area.config(state="normal")
            self.text_area.insert("end", "서버 연결 끊김...\n")
            self.text_area.config(state="disabled")

    def send_message(self, event):
        msg = self.entry.get()
        self.entry.delete(0, "end")
        asyncio.create_task(self.websocket.send(f"{self.nickname}: {msg}"))

if __name__ == "__main__":
    nickname = input("닉네임 입력: ")
    root = tk.Tk()
    app = ChatClient(root, nickname)
    root.mainloop()
