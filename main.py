import disnake
from disnake.ext import commands
import settings
import yaml

# Load themes from YAML file
with open('themes.yaml', 'r') as file:
    themes = yaml.safe_load(file)

# Initialize bot
intents = disnake.Intents.default()
intents.message_content = True  # Enable message content intent
intents.voice_states = True  # Enable voice state intents for voice functionality
bot = commands.Bot(command_prefix='!', intents=intents, test_guilds=settings.GUILD_IDS)  # Add your test guild ID(s)

# Load cogs
try:
    bot.load_extension('cogs.music')  # Load the music cog
    print("Successfully loaded 'cogs.music'")
except Exception as e:
    print(f"Failed to load 'cogs.music': {e}")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        # Sync commands on startup
        await bot.sync_commands()  # Sync commands globally
        print("Slash commands synced successfully.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# Command: !sync
@bot.command(name="sync")
@commands.is_owner()  # Restrict this command to the bot owner
async def sync(ctx: commands.Context):
    """
    Manually sync slash commands with Discord.
    """
    try:
        await bot.sync_commands()  # Sync commands globally
        await ctx.send("Slash commands have been synced.")
    except Exception as e:
        await ctx.send(f"Failed to sync commands: {e}")

# Run bot
if __name__ == "__main__":
    bot.run(settings.YOUR_BOT_TOKEN)