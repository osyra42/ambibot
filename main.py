import disnake
from disnake.ext import commands
import configparser
import random
import youtube_dl
import settings

# Load themes from INI file
config = configparser.ConfigParser()
config.read('themes.ini')

# Initialize bot
bot = commands.Bot(command_prefix='!')

# Load cogs
bot.load_extension('cogs.music')

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Run bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.sync_commands()

bot.run(settings.YOUR_BOT_TOKEN)