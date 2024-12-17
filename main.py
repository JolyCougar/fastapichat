from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import List
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Хранение подключенных клиентов
clients: List[WebSocket] = []

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Отправка сообщения всем подключенным клиентам
            for client in clients:
                await client.send_text(data)  # Отправляем сообщение всем, включая отправителя
    except WebSocketDisconnect:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
