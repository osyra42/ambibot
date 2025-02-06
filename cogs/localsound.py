import disnake
from disnake.ext import commands
import os

def parse_local_sounds(base_path):
    """Parses the local sound files from the given base path."""
    sounds = {}
    for root, dirs, files in os.walk(base_path):
        section = os.path.basename(root)  # Get the folder name (BGM or SFX)
        if section not in sounds:
            sounds[section] = []
        for file in files:
            if file.endswith(('.mp3', '.wav', '.ogg')):  # Add more extensions if needed
                sounds[section].append({
                    'path': os.path.join(root, file),
                    'description': os.path.splitext(file)[0]  # Use filename as description
                })
    return sounds

class LocalSound(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sounds = parse_local_sounds('sounds')  # Load sounds from the 'sounds' directory
        self.voice_client = None
        self.volume = 0.5  # Default volume

    @commands.slash_command(name="local", description="Display buttons to play sounds from local files")
    async def local(self, inter: disnake.ApplicationCommandInteraction):
        """Displays buttons for each sound file in the BGM and SFX sections."""
        # Create buttons for each sound file in BGM and SFX
        buttons = []
        for section, files in self.sounds.items():
            for file in files:
                # Use the file's description (filename without extension) as the button label
                buttons.append(
                    disnake.ui.Button(
                        label=file['description'],  # Button label is the filename
                        style=disnake.ButtonStyle.primary,
                        custom_id=f"sound_{section}_{file['description']}"  # Unique ID for each button
                    )
                )

        # Send the buttons as a message
        await inter.response.send_message(
            "Choose a sound to play:",
            components=buttons
        )

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.Interaction):
        # Check if the button is a sound button (custom ID starts with "sound_")
        if not inter.component.custom_id or not inter.component.custom_id.startswith("sound_"):
            return  # Ignore buttons that aren't sound-related

        # Get the member object from the guild
        if not inter.guild:
            await inter.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        member = inter.guild.get_member(inter.user.id)
        if not member or not member.voice:
            await inter.response.send_message(
                "You need to be in a voice channel to use this!",
                ephemeral=True
            )
            return

        # Now you can safely access voice state
        voice_channel = member.voice.channel

        # Parse the button's custom ID to get the section and file description
        custom_id_parts = inter.component.custom_id.split("_")
        section = custom_id_parts[1]  # Section (BGM or SFX)
        description = "_".join(custom_id_parts[2:])  # File description (filename without extension)

        # Find the selected sound file
        selected_sound = None
        for sound in self.sounds[section]:
            if sound['description'] == description:
                selected_sound = sound
                break

        if not selected_sound:
            await inter.response.send_message("Sound not found.", ephemeral=True)
            return

        # Check if the bot is connected to a voice channel
        if not member.voice:
            await inter.response.send_message("You are not connected to a voice channel.")
            return

        # Connect to the voice channel if not already connected
        if not self.voice_client:
            self.voice_client = await member.voice.channel.connect()
        elif self.voice_client.channel != member.voice.channel:
            await self.voice_client.move_to(member.voice.channel)

        # Play the selected sound
        if self.voice_client.is_playing():
            self.voice_client.stop()
        self.voice_client.play(disnake.FFmpegPCMAudio(selected_sound['path'], options=f"-filter:a 'volume={self.volume}'"))

        # Send a confirmation message
        await inter.response.send_message(f"Now playing: **{selected_sound['description']}**")

def setup(bot):
    bot.add_cog(LocalSound(bot))