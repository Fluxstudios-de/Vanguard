import os, requests, sqlite3
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv ()
# ------------- Settings -------------

TOKEN = os. getenv("'DISCORD_TOKEN")
GUILD_ID = int (os. getenv("GUILD_IDS"))


intents = discord. Intents.default()
intents. message_content = True
bot = commands. Bot (command_prefix="!", intents=intents)

# ------------- Bot Start -------------

@bot.event
async def on_ready () :
    print (f"🤖 | {bot. user} ist online.")
    await bot. sync_commands ()
    print (" 🧩 | Commands synchronisiert.")

# # ------------- Tests -------------
@bot. slash_command(guild_ids=["GUILD_ID"])
async def hello(ctx):
    await ctx. respond ("Hello!")
    
bot. run(TOKEN)