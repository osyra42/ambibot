import disnake
from disnake.ext import commands
import yt_dlp
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='music.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.volume = 0.5  # Default volume

    @commands.slash_command(name="play", description="Play a song from a YouTube URL")
    async def play(self, inter: disnake.ApplicationCommandInteraction, url: str):
        """Play a song from a YouTube URL."""
        # Defer the response
        await inter.response.defer()

        if not inter.guild:
            await inter.edit_original_response(content="This command can only be used in a server.")
            return

        member = inter.guild.get_member(inter.user.id)
        if not member or not member.voice:
            await inter.edit_original_response(content="You need to be in a voice channel to use this!")
            return

        voice_channel = member.voice.channel

        if self.voice_client:
            if self.voice_client.channel != voice_channel:
                await self.voice_client.disconnect()
                self.voice_client = await voice_channel.connect()
        else:
            self.voice_client = await voice_channel.connect()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '64',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
        except Exception as e:
            logging.error(f"Error fetching YouTube link: {e}")
            await inter.edit_original_response(content=f"Error fetching YouTube link: {e}")
            return

        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()

        self.voice_client.play(disnake.FFmpegPCMAudio(audio_url, options=f"-filter:a 'volume={self.volume}'"))

        embed = disnake.Embed(title="Now Playing", description=f"[Song]({url})", color=disnake.Color.green())
        await inter.edit_original_response(embed=embed)

    @commands.slash_command(name="pause", description="Pause the currently playing song")
    async def pause(self, inter: disnake.ApplicationCommandInteraction):
        """Pause the currently playing song."""
        # Defer the response
        await inter.response.defer()

        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            embed = disnake.Embed(title="Paused", description="The song has been paused.", color=disnake.Color.yellow())
            await inter.edit_original_response(embed=embed)
        else:
            await inter.edit_original_response(content="No song is currently playing.")

    @commands.slash_command(name="resume", description="Resume the paused song")
    async def resume(self, inter: disnake.ApplicationCommandInteraction):
        """Resume the paused song."""
        # Defer the response
        await inter.response.defer()

        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            embed = disnake.Embed(title="Resumed", description="The song has been resumed.", color=disnake.Color.green())
            await inter.edit_original_response(embed=embed)
        else:
            await inter.edit_original_response(content="No song is currently paused.")

def setup(bot):
    bot.add_cog(Music(bot))