import discord
import __main__
from candybot import engine

BOT = None


class CandyBot(discord.Client):

    @staticmethod
    async def on_ready():
        print("CandyBot Ready")

    @staticmethod
    async def on_message(message):
        await engine.handle_message(message)


def start():
    global BOT
    activity = discord.Game(f"CandyBot {__main__.VERSION}")
    BOT = CandyBot(activity=activity)
    print("Connecting to Discord...")
    BOT.run(__main__.SETTINGS["discord_token"])
