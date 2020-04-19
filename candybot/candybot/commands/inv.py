from candybot import data
from candybot.interface import discord
from candybot.commands.framework import Command, ArgumentSpec, UserArgument


class InvCommand(Command):
    name = "inv"
    help = "Shows a user's current Inventory."
    aliases = ["inventory"]
    examples = ["", "@User", "User#1234", "123456789.inv 123"]
    argument_spec = ArgumentSpec([UserArgument], True)
    admin = False
    clean = False
    ignore = False

    async def _run(self):
        user = self.args.get("user", self.message.author)
        inv = data.get_user(self.server.id, user.id).inv
        await discord.send_embed(self.message.channel, inv.list_str, author=user)
