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

class PanelView(discord.ui.DesignerView):
    def __init__(self):
        super().__init__(timeout=None)

        container = discord.ui.Container(
            discord.ui.TextDisplay("## <:account:1474536531061379113> Account Panel"),
            discord.ui.Separator(),
            discord.ui.TextDisplay(
                "> Erstelle deinen Account und verifiziere dich.\n"
                "> Wähle unten eine Aktion.\n"
            ),
            discord.ui.Separator(),
        )
        self.add_item(container)

        account_btn = discord.ui.Button(
            label="Account erstellen",
            style=discord.ButtonStyle.success
        )
        account_btn.callback = self.open_account_modal

        verify_btn = discord.ui.Button(
            label="Verifizieren",
            style=discord.ButtonStyle.primary
        )
        verify_btn.callback = self.open_verify_modal

        resend_btn = discord.ui.Button(
            label="Code erneut senden",
            style=discord.ButtonStyle.secondary
        )
        resend_btn.callback = self.resend_code

        row = discord.ui.ActionRow(account_btn, verify_btn, resend_btn)
        self.add_item(row)

    async def open_account_modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(AccountModal())

    async def open_verify_modal(self, interaction: discord.Interaction):
        await interaction.response.send_modal(VerifyModal())

    async def resend_code(self, interaction: discord.Interaction):
        data = interaction.client.verification_data.get(interaction.user.id)

        if not data:
            await interaction.response.send_message(
                "❌ Du hast noch keinen Account erstellt.",
                ephemeral=True
            )
            return

        try:
            await interaction.user.send(
                f"🔐 Dein Verifizierungscode lautet:\n`{data['code']}`"
            )
            await interaction.response.send_message(
                "✅ Code wurde erneut per DM gesendet.",
                ephemeral=True
            )
        except:
            await interaction.response.send_message(
                "❌ Ich kann dir keine DM senden. Aktiviere DMs.",
                ephemeral=True
            )

class AccountModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Account erstellen")

        self.username = discord.ui.InputText(
            label="Username",
            placeholder="Gib deinen Username ein"
        )

        self.add_item(self.username)

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        # Account ID generieren
        account_id = ''.join(random.choices(string.digits, k=8))

        # Code generieren
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # Speichern
        interaction.client.verification_data[user_id] = {
            "username": self.username.value,
            "account_id": account_id,
            "code": code
        }

        try:
            await interaction.user.send(
                f"🎉 Dein Account wurde erstellt!\n\n"
                f"🆔 Account ID: `{account_id}`\n"
                f"👤 Username: `{self.username.value}`\n\n"
                f"🔐 Dein Verifizierungscode:\n`{code}`"
            )
        except:
            await interaction.response.send_message(
                "❌ Ich kann dir keine DM senden. Aktiviere DMs.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            "✅ Account erstellt! Prüfe deine DMs für den Code.",
            ephemeral=True
        )

class VerifyModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Verifizieren")

        self.code_input = discord.ui.InputText(
            label="Verifizierungscode",
            placeholder="Gib deinen Code ein"
        )

        self.add_item(self.code_input)

    async def on_submit(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        entered_code = self.code_input.value

        data = interaction.client.verification_data.get(user_id)

        if not data:
            await interaction.response.send_message(
                "❌ Du hast noch keinen Account erstellt.",
                ephemeral=True
            )
            return

        if entered_code == data["code"]:
            role = interaction.guild.get_role(VERIFIED_ROLE)
            await interaction.user.add_roles(role)

            del interaction.client.verification_data[user_id]

            await interaction.response.send_message(
                "🎉 Erfolgreich verifiziert! Rolle wurde vergeben.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Falscher Code.",
                ephemeral=True
            )