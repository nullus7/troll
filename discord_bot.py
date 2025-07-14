import discord
from discord.ext import commands
import asyncio
import websockets
import json
import uuid

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class DiscordWSClient:
    def __init__(self):
        self.uri = "ws://localhost:8765"
        self.websocket = None
        self.pending_requests = {}

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        asyncio.create_task(self.listen_for_responses())

    async def listen_for_responses(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                if data.get('type') == 'calc_result':
                    request_id = data.get('request_id')
                    if request_id in self.pending_requests:
                        self.pending_requests[request_id](data)
        except Exception as e:
            print(f"Listener error: {e}")

    async def send_add_request(self, a, b):
        request_id = str(uuid.uuid4())
        message = {
            'type': 'add',
            'request_id': request_id,
            'a': a,
            'b': b
        }
        
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[request_id] = future.set_result
        
        await self.websocket.send(json.dumps(message))
        
        try:
            response = await asyncio.wait_for(future, timeout=10)
            return response
        except asyncio.TimeoutError:
            return {'success': False, 'error': 'Timeout'}
        finally:
            self.pending_requests.pop(request_id, None)

ws_client = DiscordWSClient()

@bot.event
async def on_ready():
    await ws_client.connect()
    print(f'Bot ready: {bot.user}')

@bot.command()
async def add(ctx, a: int, b: int):
    """Add two numbers"""
    response = await ws_client.send_add_request(a, b)
    
    if response.get('success'):
        await ctx.send(f"✅ Result: {response['result']}")
    else:
        await ctx.send(f"❌ Error: {response.get('error', 'Unknown error')}")

bot.run('your_discord_bot_token')
