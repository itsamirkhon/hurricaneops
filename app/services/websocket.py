from typing import List
from fastapi import WebSocket

class WebSocketManager:
    """
    Manages WebSocket sections for real-time updates.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # If sending fails, assume disconnection
                # We iterate over a copy or handle safely usually, but list remove might be tricky during iteration
                # For simplicity in this demo, we pass. Disconnect handles removal.
                pass

# Global instance
manager = WebSocketManager()
