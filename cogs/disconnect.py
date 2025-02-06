import disnake
from disnake.ext import commands

class Disconnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="disconnect", description="Disconnect the bot from the voice channel")
    async def disconnect(self, inter: disnake.ApplicationCommandInteraction):
        """Disconnect the bot from the voice channel."""
        # Get the voice client for the guild
        voice_client = inter.guild.voice_client

        if voice_client:
            await voice_client.disconnect()
            embed = disnake.Embed(
                title="Disconnected",
                description="The bot has been disconnected from the voice channel.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("The bot is not connected to a voice channel.", ephemeral=True)

def setup(bot):
    bot.add_cog(Disconnect(bot))