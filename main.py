import disnake
from disnake.ext import commands
import os
import configparser

# Read bot token from secrets.ini
config = configparser.ConfigParser()
config.read('secrets.ini')
bot_token = config.get('DISCORD', 'TOKEN')

# Intents and Bot Initialization
intents = disnake.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    sync_commands=False
)

# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('AmbiBot is now online!')

bot.run(bot_token)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('AmbiBot is now online!')
    await bot.http.bulk_upsert_global_commands(bot.application_id, [])
