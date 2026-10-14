import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
command_prefix="!"

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix,intents=intents)

@bot.command()
async def clear(ctx):
    await ctx.channel.purge()

@bot.command()
async def ping(ctx):
    await ctx.send('yo')

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} (ID: {bot.user.id})')
    print('------')
         
try:
    bot.run(token)
finally:
    print("Fermeture du bot")
