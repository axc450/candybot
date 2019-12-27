from candybot.interface import database, discord
from candybot.commands.framework import Command, ArgumentSpec, UserArgument


class InvCommand(Command):
    name = "inv"
    help = "Shows a user's current Inventory."
    aliases = ["inventory"]
    examples = ["", "@User", "User#1234", "123456789"]
    argument_spec = ArgumentSpec([UserArgument], True)
    admin = False
    clean = False
    ignore = False

    async def _run(self):
        user = self.args.get("user", self.message.author)
        inv = database.get_inv(self.server.id, user.id)[user.id]
        await discord.send_embed(self.message.channel, inv.list_str, author=user)
