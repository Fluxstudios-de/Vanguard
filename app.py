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

class PanelView(discord.ui.DesignerView):
    def __init__(self, author):
        super().__init__(timeout=None)
        self.author = author

        container = discord.ui.Container(
            discord.ui.TextDisplay("## <:account:1474536531061379113> Account Panel"),
            discord.ui.Separator(),
            discord.ui.TextDisplay(
                "> Hier Kannst du dir dein Account Erstellen und dich Verifizieren!.\n"
                "> Wähle unten eine Aktion.\n"
            ),
            discord.ui.Separator(),
        )

        self.add_item(container)

        button_row = discord.ui.ActionRow(
            discord.ui.Button(
                label="Account",
                style=discord.ButtonStyle.success,
                custom_id="confirm_btn"
            ),
            discord.ui.Button(
                label="Verifizieren",
                style=discord.ButtonStyle.danger,
                custom_id="close_btn"
            )
        )

        self.add_item(button_row)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message(
                "❌ Du darfst dieses Panel nicht benutzen.",
                ephemeral=True
            )
            return False
        return True

    async def on_interaction(self, interaction: discord.Interaction):
        custom_id = interaction.data.get("custom_id")

        if custom_id == "confirm_btn":
            await interaction.response.send_message(
                "✅ Bestätigt!",
                ephemeral=True
            )

        elif custom_id == "close_btn":
            await interaction.message.delete()
            
# ─────────────── Bot Start ───────────────
@bot.event
async def on_ready():
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

@bot.slash_command(guild_ids=[GUILD_ID])
async def panel(ctx):
    view = PanelView(ctx.author)
    await ctx.send(view=view)

    
bot.run(TOKEN) 