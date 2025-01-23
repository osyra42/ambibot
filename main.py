import disnake
from disnake.ext import commands
import settings
import yaml

# Load themes from YAML file
with open('themes.yaml', 'r') as file:
    themes = yaml.safe_load(file)

# Initialize bot with InteractionBot for slash commands
intents = disnake.Intents.default()
intents.message_content = True  # Enable message content intent
intents.voice_states = True  # Enable voice state intents for voice functionality

bot = commands.InteractionBot(intents=intents, test_guilds=settings.GUILD_IDS)

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
    print("Bot is ready and slash commands are registered.")
    print('------')

# Run bot
if __name__ == "__main__":
    bot.run(settings.YOUR_BOT_TOKEN)