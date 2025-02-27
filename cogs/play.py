import disnake
from disnake.ext import commands
import yt_dlp
import asyncio
import configparser

# Read guild ID from secrets.ini
config = configparser.ConfigParser()
config.read('secrets.ini')
guild_id = config.get('bot', 'GUILD_IDS')

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(disnake.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        try:
            return cls(disnake.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except Exception as e:
            print(f"Error creating audio source: {e}")
            return None

class PlayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="play", guild_ids=[int(guild_id)])
    async def play(self, interaction, url: str):
        await interaction.response.defer()
        await self.play_url(interaction, url)

    async def play_url(self, interaction, url):
        try:
            voice_channel = interaction.user.voice.channel
            if not voice_channel:
                await interaction.edit_original_response(content="You need to be in a voice channel to use this command.")
                return
            if interaction.guild.voice_client is None:
                await voice_channel.connect()
            elif interaction.guild.voice_client.channel != voice_channel:
                await interaction.guild.voice_client.move_to(voice_channel)
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            player.volume = 0.2  # Normalize audio to 0.2
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            await interaction.edit_original_response(content=f'Now playing: {player.title}')
        except yt_dlp.utils.DownloadError:
            await interaction.edit_original_response(content="The video is still processing. Please try again later.")
        except Exception as e:
            await interaction.edit_original_response(content=f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(PlayCog(bot))
