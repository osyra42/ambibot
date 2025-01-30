import disnake
from disnake.ext import commands
import configparser

# Load secrets from INI file
config = configparser.ConfigParser()
config.read('secrets.ini')

# Get the bot token and guild IDs from the config
BOT_TOKEN = config['bot']['BOT_TOKEN']  # Access the 'bot' section
GUILD_IDS = [int(guild_id) for guild_id in config['bot']['GUILD_IDS'].split(',')]  # Access the 'bot' section

# Initialize bot with InteractionBot for slash commands
intents = disnake.Intents.default()
intents.message_content = True  # Enable message content intent
intents.voice_states = True  # Enable voice state intents for voice functionality

bot = commands.InteractionBot(intents=intents, test_guilds=GUILD_IDS)

# Load cogs
try:
    bot.load_extension('cogs.music')  # Load the music cog
    print("Successfully loaded 'cogs.music'")
except Exception as e:
    print(f"Failed to load 'cogs.music': {e}")

try:
    bot.load_extension('cogs.consent')  # Load the consent cog
    print("Successfully loaded 'cogs.consent'")
except Exception as e:
    print(f"Failed to load 'cogs.consent': {e}")

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("Bot is ready and slash commands are registered.")
    print('------')

# Run bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)