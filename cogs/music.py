import disnake
from disnake.ext import commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.volume = 0.5  # Default volume

    @commands.slash_command(name="play", description="Play a song from a YouTube URL")
    async def play(self, inter: disnake.ApplicationCommandInteraction, url: str):
        """Play a song from a YouTube URL."""
        if not inter.guild:
            await inter.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        member = inter.guild.get_member(inter.user.id)
        if not member or not member.voice:
            await inter.response.send_message("You need to be in a voice channel to use this!", ephemeral=True)
            return

        voice_channel = member.voice.channel

        if not self.voice_client:
            self.voice_client = await voice_channel.connect()
        elif self.voice_client.channel != voice_channel:
            await self.voice_client.move_to(voice_channel)

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
            await inter.response.send_message(f"Error fetching YouTube link: {e}")
            return

        if self.voice_client.is_playing():
            self.voice_client.stop()

        self.voice_client.play(disnake.FFmpegPCMAudio(audio_url, options=f"-filter:a 'volume={self.volume}'"))

        embed = disnake.Embed(title="Now Playing", description=f"[Song]({url})", color=disnake.Color.green())
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="pause", description="Pause the currently playing song")
    async def pause(self, inter: disnake.ApplicationCommandInteraction):
        """Pause the currently playing song."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            embed = disnake.Embed(title="Paused", description="The song has been paused.", color=disnake.Color.yellow())
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("No song is currently playing.", ephemeral=True)

    @commands.slash_command(name="resume", description="Resume the paused song")
    async def resume(self, inter: disnake.ApplicationCommandInteraction):
        """Resume the paused song."""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            embed = disnake.Embed(title="Resumed", description="The song has been resumed.", color=disnake.Color.green())
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("No song is currently paused.", ephemeral=True)

    @commands.slash_command(name="disconnect", description="Disconnect the bot from the voice channel")
    async def disconnect(self, inter: disnake.ApplicationCommandInteraction):
        """Disconnect the bot from the voice channel."""
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None
            embed = disnake.Embed(title="Disconnected", description="The bot has been disconnected from the voice channel.", color=disnake.Color.red())
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message("The bot is not connected to a voice channel.", ephemeral=True)

def setup(bot):
    bot.add_cog(Music(bot))