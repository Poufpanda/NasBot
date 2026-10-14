import discord
from discord.ext import commands
import grammarChecker
import asyncio
import os
from dotenv import load_dotenv
import mc_serv

load_dotenv()

token = os.getenv("TOKEN")
command_prefix="!"

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix,intents=intents)
correcteur = grammarChecker.OrthographeChecker()

@bot.command()
async def clear(ctx):
    await ctx.channel.purge()

@bot.command()
async def ping(ctx):
    await ctx.send('yo')

@bot.command(name="start")
async def startmc(ctx):
    mc_serv.startServer()
    await ctx.send("Serveur lancé !")

@bot.command(name="stop")
async def stopmc(ctx):
    mc_serv.stopServer()
    await ctx.send("Serveur stoppé !")

@bot.command(name="restart")
async def restartmc(ctx):
    mc_serv.restartServer()
    await ctx.send("Le serveur se relance !")


@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.invoke(ctx)
        return

    if len(message.attachments) > 0 or message.type != discord.MessageType.default or grammarChecker.analyse(message.content):
        return

    print(f"Analyse du message : {message.content}")
    loop = asyncio.get_event_loop()
    fautes = await loop.run_in_executor(None, correcteur.verifier, message.content)
    print("Traitement fini!")

    if len(fautes) > 0:
        faute = fautes[0]
        reponse = f"{message.author.mention}, j'ai repéré une erreur : '{faute.sentence}'\n"
        
        if faute.replacements:
            reponse += f"Suggestion : **{faute.replacements}**"
        
        await message.channel.send(reponse)
        await bot.process_commands(message)

            
try:
    bot.run(token)
finally:
    print("Fermeture du bot")
    correcteur.fermer()