# Discord Bot README (Windows)

Welcome to the setup guide for your Discord bot! This README will walk you through the process of setting up the **AmbiBot** on your Windows machine. By the end of this guide, you'll have the bot up and running.

---

## Prerequisites

Before you begin, make sure you have the following:

1. **A Discord account** - You need this to create a bot application.
2. **A text editor** - We recommend using [Notepad++](https://notepad-plus-plus.org/downloads/) for editing files.
3. **Basic familiarity with the Command Prompt** - You'll need to run a few commands to set things up.

---

## Step 1: Install Python 3.12

The bot is written in Python, so you'll need to install Python on your machine. We'll use Python 3.12 for this setup.

1. Go to the [Python official website](https://www.python.org/downloads/).
2. Download **Python 3.12**.
3. Run the installer.
4. During installation, make sure to check the box that says **"Add Python to PATH"**.
5. Click "Install Now" and wait for the installation to complete.

---

## Step 2: Create a Discord Bot Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on **"New Application"** and give your bot a name (e.g., "AmbiBot").
3. Optionally, upload a profile picture for your bot under the **"App Icon"** section.
4. Navigate to the **"Bot"** tab on the left sidebar.
5. Click **"Add Bot"** and confirm.
6. Under the **"OAuth2"** tab, select **"URL Generator"**.
7. In the **"Scopes"** section, check the box for **"bot"**.
8. In the **"Bot Permissions"** section, select the permissions your bot needs (e.g., "Send Messages," "Manage Roles").
9. Copy the generated URL and paste it into your browser to invite the bot to your server.

---

## Step 3: Download the Bot Repository

1. Go to the bot's GitHub repository: [AmbiBot](https://github.com/osyra42/ambibot).
2. Click the green **"Code"** button and select **"Download ZIP"**.
3. Extract the ZIP file to a folder on your computer (e.g., `C:\Users\YourUsername\Documents\ambibot`).

---

## Step 4: Set Up a Virtual Environment

A virtual environment (venv) is an isolated space where you can install Python packages without affecting your system's global Python installation.

1. Open **Command Prompt**.
2. Navigate to the folder where you extracted the bot files. For example:
   ```cmd
   cd C:\Users\YourUsername\Documents\ambibot
   ```
3. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```
4. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
   You'll know it's activated when you see `(venv)` at the beginning of your Command Prompt.

---

## Step 5: Install Requirements

The bot requires certain Python packages to run. These are listed in a file called `requirements.txt`.

1. Make sure your virtual environment is activated.
2. Install the requirements:
   ```cmd
   pip install -r requirements.txt
   ```

---

## Step 6: Configure the Bot

1. Open the `secrets.ini` file in **Notepad++** or your preferred text editor.
2. Replace the placeholders with the following:
   - `bot_token = YOUR_BOT_TOKEN_HERE` - Replace `YOUR_BOT_TOKEN_HERE` with your bot's token from the Discord Developer Portal (found in the **"Bot"** tab).
   - `guild_ids = YOUR_GUILD_IDS_HERE` - Replace `YOUR_GUILD_IDS_HERE` with your Discord server's ID(s). To get your server ID, enable Developer Mode in Discord (Settings > Advanced > Developer Mode), right-click your server name, and select "Copy ID." If you have multiple servers, separate the IDs with commas (e.g., `123456789012345678, 987654321098765432`).
3. Save the file.

---

## Step 7: Run the Bot

1. Double-click on the `zlauncher.bat` file in the bot's folder.
2. A Command Prompt window will open, and the bot should start running.
3. If everything is set up correctly, the bot should come online in your Discord server!

---

## Step 8: Stopping the Bot

To stop the bot, simply close the Command Prompt window that was opened when you ran `zlauncher.bat`. This will terminate the bot's process.

---

## Troubleshooting

- **Bot isn't coming online**: Double-check your `bot_token` and `guild_ids` in the `secrets.ini` file.
- **Missing dependencies**: Make sure you installed all requirements using `pip install -r requirements.txt`.
- **Python not found**: Ensure Python 3.12 is added to your PATH (Step 1).

---

## Support

If you encounter any issues, feel free to open an issue on the [GitHub repository](https://github.com/osyra42/ambibot) or reach out to the community for help.

Enjoy your new Discord bot! 🎉
