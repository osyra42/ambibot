import disnake
from disnake.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, inter, amount: int):
        await inter.response.defer()
        if amount <= 0 or amount > 1000:
            await inter.edit_original_response(content='Please enter a number between 1 and 1000.')
            return

        if not inter.me.guild_permissions.manage_messages:
            await inter.edit_original_response(content='I do not have permission to manage messages in this channel.')
            return

        try:
            await inter.channel.purge(limit=amount)
            await inter.edit_original_response(content=f'Successfully purged {amount} messages.')
        except Exception as e:
            await inter.edit_original_response(content=f'Failed to purge messages: {e}')

def setup(bot):
    bot.add_cog(Purge(bot))
