import disnake
from disnake.ext import commands
import os
import configparser

# Read guild ID from secrets.ini
config = configparser.ConfigParser()
config.read('secrets.ini')
guild_id = config.get('bot', 'GUILD_IDS')

class LocalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="play_local", guild_ids=[int(guild_id)])
    async def play_local(self, interaction):
        await interaction.response.defer()

        view = disnake.ui.View()
        bgm_files = os.listdir('sounds/BGM')
        sfx_files = os.listdir('sounds/SFX')

        for file in bgm_files:
            if file.endswith('.mp3'):
                button = disnake.ui.Button(label=file[:-4], style=disnake.ButtonStyle.primary)
                button.callback = self.play_sound_callback('BGM', file[:-4])
                view.add_item(button)

        for file in sfx_files:
            if file.endswith('.mp3'):
                button = disnake.ui.Button(label=file[:-4], style=disnake.ButtonStyle.primary)
                button.callback = self.play_sound_callback('SFX', file[:-4])
                view.add_item(button)

        await interaction.edit_original_response(content="Select a sound to play:", view=view)

    def play_sound_callback(self, sound_type, sound_name):
        async def callback(interaction):
            await interaction.response.defer()

            sound_path = f'sounds/{sound_type}/{sound_name}.mp3'
            if not os.path.exists(sound_path):
                await interaction.edit_original_response(content="Sound not found.")
                return

            voice_channel = interaction.user.voice.channel
            if not voice_channel:
                await interaction.edit_original_response(content="You need to be in a voice channel to use this command.")
                return

            if interaction.guild.voice_client is None:
                await voice_channel.connect()
            elif interaction.guild.voice_client.channel != voice_channel:
                await interaction.guild.voice_client.move_to(voice_channel)

            source = disnake.FFmpegPCMAudio(sound_path)
            source = disnake.PCMVolumeTransformer(source, volume=0.2)  # Normalize audio to 0.2
            if interaction.guild.voice_client.is_playing():
                interaction.guild.voice_client.stop()
            interaction.guild.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            await interaction.edit_original_response(content=f'Now playing: {sound_name}')

        return callback

def setup(bot):
    bot.add_cog(LocalCog(bot))
