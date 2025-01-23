import disnake
from disnake.ext import commands
import random
import youtube_dl
import settings
import yaml

# Load themes from YAML file
with open('themes.yaml', 'r') as file:
    themes = yaml.safe_load(file)

# Initialize bot
intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
bot.load_extension('cogs.music')

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.sync_commands()

# Run bot
bot.run(settings.YOUR_BOT_TOKEN)