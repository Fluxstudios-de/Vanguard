import discord, os, random, string
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
GUILD_ID = int(os.getnev("GUILD_IDS"))
VERIFY_ROLE = os.getenv("VERIFY_ROLES")

class AccountSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(guild_ids=[GUILD_ID])
    async def panel(self, ctx):
        view = PanelView(ctx.author)
        await ctx.send(view=view)

def setup(bot):
    bot.add_cog(AccountSystem(bot))
