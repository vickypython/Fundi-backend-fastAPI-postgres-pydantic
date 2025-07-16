# app/main.py
from fastapi import FastAPI,webSocket,webSocketDisconnect
from app.routers import users


app = FastAPI()

# Register route
app.include_router(users.router)
#simple websocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connection:list[webSocket]=[]
    async def connect(self,websocket:webSocket):
        await WebSocket.accept()
        self.active_connection.append(websocket)
    def disconnet(self,websocket:WebSocket):
        self.active_connection.remove(websocket)
    async def broadcast(self,message:str):
        for connection in self.active_connection:
            await connection.send_text(message)
    async def show_typing(self,sender_id:UUID,chat_id:UUID):
        for uid,ws in self.active_connection.items():
            if uid!=sender_id:
                await ws.send_json(
                    {
                        'typing':"typing",
                        "chat_id":str(chat_id),
                        "sender_id":str(sender_id)
                    }
                )


manager=ConnectionManager()
@app.websocket('/ws/{role}')
async def websocket_endpoint(websocket:WebSocket,
role:str,
db:Session=Depends(get_db)
):
    await manager.connect(websocket)
    try:
        while True:
            data=await websocket.receive_text()
            message_data=schemas.MessageCreate(
                sender_role=role,
                content=data
            )
            db_message=models.Message(**message_data.dict())
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
             broadcast_message = {
                "sender_role": db_message.sender_role,
                "content": db_message.content,
                "timestamp": db_message.timestamp.isoformat()
            }
            await manager.broadcast(json.dumps(broadcast_message))

    except webSocketDisconnect:
        manager.disconnect(websocket)

