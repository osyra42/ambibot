import disnake
from disnake.ext import commands
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Logs to the console
    ]
)

class ConsentView(disnake.ui.View):
    def __init__(self, inter):
        super().__init__(timeout=60)
        self.inter = inter
        self.sent_via_dm = False

    @disnake.ui.button(label="I agree", style=disnake.ButtonStyle.green)
    async def agree_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.user != self.inter.author:
            await interaction.response.send_message("You're not the user who requested consent.", ephemeral=True)
            return

        # Log consent
        logging.info(f"{interaction.user} (ID: {interaction.user.id}) has agreed to the consent form.")

        await interaction.response.send_message(f"Thank you for consenting, {interaction.user.mention}!")
        self.stop()

    @disnake.ui.button(label="I don't agree", style=disnake.ButtonStyle.red)
    async def disagree_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if interaction.user != self.inter.author:
            await interaction.response.send_message("You're not the user who requested consent.", ephemeral=True)
            return

        # Log disagreement
        logging.info(f"{interaction.user} (ID: {interaction.user.id}) has disagreed to the consent form.")

        await interaction.response.send_message("You have not consented. Please try again later if you change your mind.")
        self.stop()

    async def on_timeout(self):
        try:
            if self.sent_via_dm:
                await self.inter.author.send(f"{self.inter.author.mention} You didn't consent in time. Please try again later.")
            else:
                await self.inter.followup.send(f"{self.inter.author.mention} You didn't consent in time. Please try again later.", ephemeral=True)
        except disnake.Forbidden:
            await self.inter.followup.send(f"{self.inter.author.mention} You didn't consent in time. Please try again later.", ephemeral=True)

class ConsentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='consent')
    async def consent(self, inter: disnake.ApplicationCommandInteraction):
        with open('consent_form.txt', 'r') as file:
            consent_form = file.read()

        view = ConsentView(inter)

        try:
            await inter.author.send(consent_form, view=view)
            view.sent_via_dm = True
        except disnake.Forbidden:
            await inter.send(consent_form, view=view, ephemeral=True)
            view.sent_via_dm = False

def setup(bot):
    bot.add_cog(ConsentCog(bot))