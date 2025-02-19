import disnake
from disnake.ext import commands
import configparser
from cogs.play import YTDLSource
import yt_dlp
import os

# Read guild ID from secrets.ini
config = configparser.ConfigParser()
config.read('secrets.ini')
guild_id = config.get('bot', 'GUILD_IDS')

# Ensure the theme_songs directory exists
theme_songs_dir = os.path.join('sounds', 'theme_songs')
os.makedirs(theme_songs_dir, exist_ok=True)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(theme_songs_dir, '%(extractor)s-%(id)s-%(title)s.%(ext)s'),
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # Bind to ipv4
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class ThemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist = self.load_playlist('playlist.txt')

    def load_playlist(self, file_path):
        playlist = {}
        with open(file_path, 'r') as file:
            current_category = None
            for line in file:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    current_category = line[1:-1]
                    playlist[current_category] = []
                elif current_category and line:
                    url, *description = line.split(';')
                    playlist[current_category].append((url.strip(), description[0].strip() if description else ""))
        return playlist

    @commands.slash_command(name="theme", guild_ids=[int(guild_id)])
    async def theme(self, interaction):
        await interaction.response.defer()
        view = disnake.ui.View()
        for category in self.playlist:
            button = disnake.ui.Button(label=category, style=disnake.ButtonStyle.blurple)
            button.callback = lambda interaction, c=category: self.play_category(interaction, c)
            view.add_item(button)
        await interaction.edit_original_response(content="Choose a theme:", view=view)

    async def play_category(self, interaction, category):
        if category in self.playlist:
            url, description = self.playlist[category][0]
            await self.play_url(interaction, url)

    async def play_url(self, interaction, url):
        try:
            voice_channel = interaction.user.voice.channel
            if not voice_channel:
                await interaction.response.defer()
                await interaction.edit_original_response(content="You need to be in a voice channel to use this command.")
                return
            if interaction.guild.voice_client is None:
                await voice_channel.connect()
            elif interaction.guild.voice_client.channel != voice_channel:
                await interaction.guild.voice_client.move_to(voice_channel)
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            interaction.guild.voice_client.stop()
            interaction.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            await interaction.edit_original_response(content=f'Now playing: {player.title}')
        except yt_dlp.utils.DownloadError:
            await interaction.edit_original_response(content="The video is still processing. Please try again later.")
        except Exception as e:
            await interaction.edit_original_response(content=f"An error occurred: {e}")

def setup(bot):
    bot.add_cog(ThemeCog(bot))
