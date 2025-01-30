import disnake
from disnake.ext import commands

class ConsentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='consent')
    async def consent(self, inter):
        # Read the consent form from the file
        with open('consent_form.txt', 'r') as file:
            consent_form = file.read()

        # Try to send the consent form via DM
        try:
            await inter.author.send(consent_form)
        except disnake.Forbidden:
            # If DM is not allowed, post the consent form in the server as an ephemeral message
            await inter.send(consent_form, ephemeral=True)  # Ephemeral message
            await inter.send(f"{inter.author.mention} Please consent to the terms by replying with 'I consent'.")

        # Wait for the user's response
        def check(message):
            return message.author == inter.author and message.channel == inter.channel and message.content.lower() == 'i consent'

        try:
            response = await self.bot.wait_for('message', check=check, timeout=60.0)
            await inter.send(f"{inter.author.mention} Thank you for consenting!")
            # Save the consent to the database (not implemented here)
        except TimeoutError:
            await inter.send(f"{inter.author.mention} You did not consent in time. Please try again later.")

# Add the cog to the bot
def setup(bot):
    bot.add_cog(ConsentCog(bot))