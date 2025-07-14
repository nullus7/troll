import discord
from discord.ext import commands
import asyncio
import websockets
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_ws_command(command, data):
    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            message = {'type': command, **data}
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            return json.loads(response)
    except Exception as e:
        print(f"WebSocket error: {e}")
        return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def add(ctx, a: int, b: int):
    """Add two numbers through the connected app"""
    response = await send_ws_command('add', {'a': a, 'b': b})
    if response:
        await ctx.send(f"Result: {response.get('result')}")
    else:
        await ctx.send("Failed to communicate with the app")

bot.run('your_discord_bot_token')
