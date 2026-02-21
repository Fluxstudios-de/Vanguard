import discord













class PanelView(discord.ui.DesignerView):
    def __init__(self, author):
        super().__init__(timeout=120)
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