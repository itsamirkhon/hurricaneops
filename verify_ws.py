import asyncio
import websockets
import json
import requests
import time
from threading import Thread

# Configuration
WS_URL = "ws://localhost:8000/ws"
API_URL = "http://localhost:8000/api"

async def listen():
    print(f"Connecting to {WS_URL}...")
    try:
        async with websockets.connect(WS_URL) as websocket:
            print("Connected to WebSocket")
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                print(f"Received WS Message: {data}")
                if data.get("type") == "action_log":
                    print("SUCCESS: Received action log via WebSocket")
                    return
    except Exception as e:
        print(f"WebSocket Error: {e}")

def trigger_action():
    time.sleep(2) # Wait for WS to connect
    print("Triggering action via API...")
    # Create a test incident first to resolve
    # Actually just deploy to a dummy incident if strict validation isn't blocking, or create one
    # Creating incident is safer
    
    # 1. Create Incident
    inc_data = {
        "type": "fire", 
        "priority": "medium", 
        "description": "WS Test Fire", 
        "latitude": 10.0, 
        "longitude": 10.0,
        "affected_count": 0
    }
    
    try:
        res = requests.post(f"{API_URL}/actions/incident/create", json=inc_data)
        print(f"Create Incident Response: {res.status_code}")
        # This execution should trigger broadcast
    except Exception as e:
        print(f"API Trigger Error: {e}")

async def main():
    # Start listener
    listener_task = asyncio.create_task(listen())
    
    # Trigger action in background thread
    t = Thread(target=trigger_action)
    t.start()
    
    # Wait for listener to finish (it returns on success)
    try:
        await asyncio.wait_for(listener_task, timeout=10)
    except asyncio.TimeoutError:
        print("TIMEOUT: Did not receive WebSocket message in time")
    
    t.join()

if __name__ == "__main__":
    asyncio.run(main())
