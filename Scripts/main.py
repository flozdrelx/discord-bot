import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='!', # Set your bot's prefix here
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print(f'Bot ready as: {bot.user}')

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

async def main():
    async with bot:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                try:
                    await bot.load_extension(
                        f'cogs.{filename[:-3]}'
                    )
                    print(f'Loaded {filename}')
                except Exception as e:
                    print(f'Failed loading {filename}: {e}')

        await bot.start(os.getenv('TOKEN'))

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bot stopped')