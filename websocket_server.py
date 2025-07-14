import asyncio
import websockets
import json

connected_clients = set()

async def handle_client(websocket, path=None):  # Make path optional
    # Register client
    connected_clients.add(websocket)
    print(f"New client connected (path: {path}). Total clients: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Received message: {data}")
            
            if data.get('type') == 'add':
                # Perform addition
                result = data['a'] + data['b']
                response = {'type': 'add_result', 'result': result}
                await websocket.send(json.dumps(response))
                
            elif data.get('type') == 'auth':
                # Handle authentication
                if data.get('token') == 'your_secret_token':
                    response = {'type': 'auth_success'}
                    await websocket.send(json.dumps(response))
                else:
                    response = {'type': 'auth_failed'}
                    await websocket.send(json.dumps(response))
                    
    finally:
        # Unregister client
        connected_clients.remove(websocket)
        print(f"Client disconnected. Remaining clients: {len(connected_clients)}")

async def main():
    server = await websockets.serve(
        handle_client,
        "0.0.0.0",
        8765
    )
    print("WebSocket server started on ws://0.0.0.0:8765")
    await asyncio.Future()  # run forever

asyncio.run(main())
