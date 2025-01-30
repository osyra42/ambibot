# use /consent to get a document and the user needs to sign it with "i agree" button and then save it to the database, if a user doesn't agree then the users voice is not recorded

import discord
from discord.ext import commands

class ConsentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='consent')
    async def consent(self, ctx):
        # Read the consent form from the file
        with open('consent_form.txt', 'r') as file:
            consent_form = file.read()

        # Try to send the consent form via DM
        try:
            await ctx.author.send(consent_form)
        except discord.Forbidden:
            # If DM is not allowed, post the consent form in the server as an ephemeral message
            await ctx.send(consent_form, delete_after=60)  # Ephemeral message
            await ctx.send(f"{ctx.author.mention} Please consent to the terms by replying with 'I consent'.")

        # Wait for the user's response
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == 'i consent'

        try:
            response = await self.bot.wait_for('message', check=check, timeout=60.0)
            await ctx.send(f"{ctx.author.mention} Thank you for consenting!")
            # Save the consent to the database (not implemented here)
        except TimeoutError:
            await ctx.send(f"{ctx.author.mention} You did not consent in time. Please try again later.")

# Add the cog to the bot
def setup(bot):
    bot.add_cog(ConsentCog(bot))