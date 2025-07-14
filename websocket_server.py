import asyncio
import websockets
import json

connected_clients = set()

async def handle_client(websocket, path=None):
    connected_clients.add(websocket)
    print(f"New client connected. Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Routing message: {data}")
            
            # Route messages between clients
            for client in connected_clients:
                if client != websocket:  # Don't echo back to sender
                    await client.send(json.dumps(data))
                    
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining: {len(connected_clients)}")

async def main():
    server = await websockets.serve(
        handle_client,
        "0.0.0.0",
        8765
    )
    print("WebSocket message router started on ws://0.0.0.0:8765")
    await asyncio.Future()

asyncio.run(main())
