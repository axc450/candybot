import discord
import __main__
from candybot import engine
from candybot.interface import files

BOT = None


class CandyBot(discord.Client):

    @staticmethod
    async def on_ready():
        print("CandyBot Ready")

    @staticmethod
    async def on_message(message):
        await engine.handle_message(message)

    @staticmethod
    async def on_guild_join(guild):
        await engine.setup(guild.id)

    @staticmethod
    async def on_guild_leave(guild):
        await engine.teardown(guild.id)


def start():
    global BOT
    token = files.load_token()
    activity = discord.Game(f"CandyBot v{__main__.VERSION}")
    BOT = CandyBot(activity=activity)
    print("Connecting to Discord...")
    BOT.run(token)
