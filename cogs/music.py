import disnake
from disnake.ext import commands
import configparser
import random
import yt_dlp  # Changed from youtube_dl to yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = configparser.ConfigParser()
        self.config.read('themes.ini')
        self.current_theme = None
        self.voice_client = None
        self.volume = 0.5  # Default volume
        self.queue = []  # Queue for multiple themes
        self.inactivity_timer = None  # Timer for inactivity

    @commands.slash_command(name="connect", description="Connect the bot to your voice channel")
    async def connect(self, inter: disnake.ApplicationCommandInteraction):
        if inter.author.voice is None:
            await inter.response.send_message("You are not connected to a voice channel.")
            return

        if self.voice_client:
            await self.voice_client.disconnect()
        self.voice_client = await inter.author.voice.channel.connect()
        await inter.response.send_message(f"Connected to {inter.author.voice.channel.name}")

    @commands.slash_command(name="select", description="Select a music theme")
    async def select(self, inter: disnake.ApplicationCommandInteraction, theme: str):
        if theme not in self.config.sections():
            await inter.response.send_message(f"Theme '{theme}' not found.")
            return

        self.current_theme = theme
        await inter.response.send_message(f"Selected theme: {theme}")

    @commands.slash_command(name="start", description="Start playing music from the selected theme or queue")
    async def start(self, inter: disnake.ApplicationCommandInteraction):
        if self.current_theme is None and not self.queue:
            await inter.response.send_message("No theme selected and queue is empty.")
            return

        if self.voice_client is None:
            await inter.response.send_message("Bot is not connected to a voice channel.")
            return

        if self.queue:
            theme = self.queue.pop(0)
        else:
            theme = self.current_theme

        links = [self.config[theme][key] for key in self.config[theme]]
        link = random.choice(links)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Changed from youtube_dl to yt_dlp
                info = ydl.extract_info(link, download=False)
                url = info['url']  # Changed from info['formats'][0]['url'] to info['url']
        except Exception as e:
            await inter.response.send_message(f"Error fetching YouTube link: {e}")
            return

        if not self.voice_client.is_playing():
            self.voice_client.play(disnake.FFmpegPCMAudio(url, options=f"-filter:a 'volume={self.volume}'"))
        await inter.response.send_message(f"Playing {theme} music")

        # Reset inactivity timer
        if self.inactivity_timer:
            self.inactivity_timer.cancel()
        self.inactivity_timer = self.bot.loop.call_later(600, self.disconnect_on_inactivity)

        # Send UI components
        await self.send_ui_components(inter, f"Playing {theme} music")

    @commands.slash_command(name="queue", description="Add a theme to the queue")
    async def queue(self, inter: disnake.ApplicationCommandInteraction, theme: str):
        if theme not in self.config.sections():
            await inter.response.send_message(f"Theme '{theme}' not found.")
            return

        self.queue.append(theme)
        await inter.response.send_message(f"Added {theme} to the queue")

    @commands.slash_command(name="volume", description="Set the volume")
    async def volume(self, inter: disnake.ApplicationCommandInteraction, volume: float):
        if volume < 0 or volume > 1:
            await inter.response.send_message("Volume must be between 0 and 1.")
            return

        self.volume = volume
        await inter.response.send_message(f"Volume set to {volume}")

    async def disconnect_on_inactivity(self):
        if self.voice_client and self.voice_client.is_playing():
            await self.voice_client.disconnect()
            self.voice_client = None
            print("Disconnected due to inactivity.")

    async def send_ui_components(self, inter: disnake.ApplicationCommandInteraction, message: str):
        components = [
            disnake.ui.Button(label="Connect", style=disnake.ButtonStyle.primary, custom_id="connect"),
            disnake.ui.Button(label="Start", style=disnake.ButtonStyle.success, custom_id="start"),
            disnake.ui.Button(label="Stop", style=disnake.ButtonStyle.danger, custom_id="stop"),
            disnake.ui.Button(label="Disconnect", style=disnake.ButtonStyle.secondary, custom_id="disconnect"),
            disnake.ui.Select(
                placeholder="Select a theme",
                options=[disnake.SelectOption(label=theme, value=theme) for theme in self.config.sections()],
                custom_id="select_theme"
            )
        ]
        await inter.response.send_message("Music Control Panel", components=components)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "connect":
            await self.connect(inter)
        elif inter.component.custom_id == "start":
            await self.start(inter)
        elif inter.component.custom_id == "stop":
            await self.stop(inter)
        elif inter.component.custom_id == "disconnect":
            await self.disconnect(inter)

    @commands.Cog.listener()
    async def on_select(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "select_theme":
            await self.select(inter, inter.values[0])

    @commands.slash_command(name="stop", description="Stop playing music")
    async def stop(self, inter: disnake.ApplicationCommandInteraction):
        if self.voice_client is None:
            await inter.response.send_message("Bot is not connected to a voice channel.")
            return

        self.voice_client.stop()
        await inter.response.send_message("Stopped playing music")

    @commands.slash_command(name="disconnect", description="Disconnect the bot from the voice channel")
    async def disconnect(self, inter: disnake.ApplicationCommandInteraction):
        if self.voice_client is None:
            await inter.response.send_message("Bot is not connected to a voice channel.")
            return

        await self.voice_client.disconnect()
        self.voice_client = None
        await inter.response.send_message("Disconnected from voice channel")

def setup(bot):
    bot.add_cog(Music(bot))