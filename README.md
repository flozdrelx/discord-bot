# Simple Discord Moderation Bot

#### Portfolio project

A simple Discord moderation bot with basic moderation features and utility commands.

---

# How to use

## Create a Discord bot

1. Go to the Discord Developer Portal
2. Create a new application
3. Go to the **Bot** section
4. Create a bot
5. Copy your bot token

## Configure bot permissions

* Go to **OAuth2 > URL Generator**
* Select the **bot** scope
* Enable the following permissions:

    * Manage Roles
    * Manage Channels
    * Kick Members
    * Ban Members
    * Moderate Members
    * Send Messages
    * Manage Messages
    * Read Message History

* Copy the generated URL and invite the bot to your server
* Make sure the bot role is above the other roles

## Configure the .env file

1. Open `Scripts/.env`
2. Replace:

```env
your_bot_token
```

with your actual bot token.

## Configure roles

1. Open `data/config.json`
2. Set your admin and moderator role IDs

Example:

```json
{
    "roles": {
        "admin_role_id": [123456789012345678],
        "mod_role_id": [123456789012345678]
    }
}
```

---

# Run the bot

## Windows

* Make sure Python is installed
* Double click `run.bat`
* Wait until the virtual environment is created and dependencies are installed

## Linux / macOS

* Make sure Python is installed
* Open a terminal in the project folder
* Make the script executable

```bash
chmod +x run.sh
```

* Run the script

```bash
./run.sh
```

---

# Extra

The bot includes both slash and prefix commands.

If you want to change the bot prefix:

1. Open `Scripts/main.py`
2. Search for this line:

```python
command_prefix='!'
```

3. Replace `'!'` with the prefix you want the bot to use.

The bot also includes a help command that displays all available commands and how to use them.