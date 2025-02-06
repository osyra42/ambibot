import disnake
from disnake.ext import commands
import configparser
import os

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

def check_permissions():
    def decorator(func):
        async def wrapper(inter: disnake.ApplicationCommandInteraction, *args, **kwargs):
            # Check if the user is the owner
            if inter.user.id != inter.guild.owner_id:
                await inter.response.send_message("You do not have permission to use this command.", ephemeral=True)
                return
            return await func(inter, *args, **kwargs)
        return wrapper
    return decorator

# Directory containing cogs
cogs_dir = "cogs"

# Load all .py files in the cogs directory as cogs
for filename in os.listdir(cogs_dir):
    if filename.endswith(".py") and not filename.startswith("_"):  # Ignore __init__.py and private files
        cog_name = f"{cogs_dir}.{filename[:-3]}"  # Remove '.py' and format as 'cogs.filename'
        try:
            bot.load_extension(cog_name)  # Load the cog
            print(f"Successfully loaded '{cog_name}'")
        except Exception as e:
            print(f"Failed to load '{cog_name}': {e}")

print("==================================================")

# Event: Bot is ready
@bot.event
async def on_ready():
    print("==================================================")
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print("Bot is ready and slash commands are registered.")

    # Fetch the bot owner's information
    app_info = await bot.application_info()
    owner = app_info.owner
    print(f'Bot owner: {owner.name} (ID: {owner.id})')

    print('==================================================')

# Example command with permission check
@bot.slash_command()
@check_permissions()
async def example_command(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message("You have permission to use this command!")

# Run bot
if __name__ == "__main__":
    bot.run(BOT_TOKEN)