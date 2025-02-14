import disnake
from disnake.ext import commands
import random
import yt_dlp

def parse_playlist(file_path):
    """
    Parses a custom playlist file with sections, URLs, and descriptions.
    """
    playlist = {}
    current_section = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Ignore comments and empty lines
            if line.startswith('#') or not line:
                continue
            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                playlist[current_section] = []
            else:
                # Split URL and description (if description exists)
                if ';' in line:
                    url, description = line.split(';', 1)
                else:
                    url, description = line, ''  # No description provided
                # Add to the current section
                playlist[current_section].append({
                    'url': url.strip(),
                    'description': description.strip()
                })

    return playlist

class Ambiance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playlist = parse_playlist('playlist.txt')  # Load playlist from file
        self.voice_client = None
        self.volume = 0.5  # Default volume

    @commands.slash_command(name="playlist", description="Display buttons to play ambiance from different sections")
    async def playlist(self, inter: disnake.ApplicationCommandInteraction):
        """
        Displays buttons for each section in the playlist.
        """
        # Defer the response
        await inter.response.defer()

        # Create buttons for each section with custom IDs prefixed with "ambiance_"
        buttons = [
            disnake.ui.Button(
                label=section,
                style=disnake.ButtonStyle.primary,
                custom_id=f"ambiance_{section}"  # Add a prefix to distinguish ambiance buttons
            )
            for section in self.playlist.keys()
        ]

        # Send the buttons as a message
        await inter.edit_original_response(
            content="Choose a section to play a random song:",
            components=buttons
        )

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.Interaction):
        # Check if the button is a ambiance button (custom ID starts with "ambiance_")
        if not inter.component.custom_id or not inter.component.custom_id.startswith("ambiance_"):
            return  # Ignore buttons that aren't ambiance-related

        # Defer the response
        await inter.response.defer()

        # Get the member object from the guild
        if not inter.guild:
            await inter.edit_original_response(content="This command can only be used in a server.")
            return

        member = inter.guild.get_member(inter.user.id)
        if not member or not member.voice:
            await inter.edit_original_response(content="You need to be in a voice channel to use this!")
            return

        # Now you can safely access voice state
        voice_channel = member.voice.channel

        # Get the section from the button's custom_id (remove the "ambiance_" prefix)
        section = inter.component.custom_id[len("ambiance_"):]

        # Check if the bot is connected to a voice channel
        if not member.voice:
            await inter.edit_original_response(content="You are not connected to a voice channel.")
            return

        # Connect to the voice channel if not already connected
        if not self.voice_client:
            self.voice_client = await member.voice.channel.connect()
        elif self.voice_client.channel != member.voice.channel:
            await self.voice_client.move_to(member.voice.channel)

        # Get a random song from the selected section
        songs = self.playlist[section]
        song = random.choice(songs)
        url = song['url']

        # Use yt-dlp to extract the audio URL
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
            await inter.edit_original_response(content=f"Error fetching YouTube link: {e}")
            return

        # Play the audio
        if self.voice_client.is_playing():
            self.voice_client.stop()
        self.voice_client.play(disnake.FFmpegPCMAudio(audio_url, options=f"-filter:a 'volume={self.volume}'"))

        # Send a confirmation message
        await inter.edit_original_response(content=f"Now playing a random song from **{section}**: {song['description']}")

def setup(bot):
    bot.add_cog(Ambiance(bot))