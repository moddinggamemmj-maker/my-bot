import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# Web server to keep the service active
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run server and bot
if name == "__main__":
    keep_alive()
    bot.run(os.environ['DISCORD_TOKEN'])
