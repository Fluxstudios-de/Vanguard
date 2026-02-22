import os, requests, sqlite3
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ─────────────── Setup ───────────────
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_IDS"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
            
# ─────────────── Bot Start ───────────────
@bot.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    channel = bot.get_channel(1474791125280755984)
    if channel:
        view = discord.ui.DesignerView(timeout=None)

        container = discord.ui.Container(
            discord.ui.TextDisplay("### 🚀 Started"),
            discord.ui.TextDisplay("The bot is started and fully functional."),
            discord.ui.Separator(),
            discord.ui.TextDisplay(f"- {bot.user.name}"),
            discord.ui.TextDisplay(f"- {bot.user.id}"),
            discord.ui.TextDisplay(f"- {round(bot.latency * 1000)} ms"),
        )

        view.add_item(container)

        await channel.send(view=view)
    print(f"🤖 {bot.user} ist online.")
    await bot.sync_commands()
    print("✅ Commands synchronisiert.")

    
bot.run(TOKEN) 