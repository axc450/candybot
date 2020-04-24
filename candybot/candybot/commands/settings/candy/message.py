from candybot import data
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, CandyArgument, TextArgument


class MessageCandyCommand(CandySettingsCommand):
    name = "message"
    help = "Changes the candy drop message."
    aliases = ["candymessage", "candymsg"]
    examples = ["🍎 Apples appeared!", "apple Apples appeared!"]
    argument_spec = ArgumentSpec([CandyArgument, TextArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        candy = self.args[0]
        text = self.args[1]
        candy_settings = next(x for x in self.server_settings.candy if x.candy == candy)
        candy_settings.text = text
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"{candy} drop message has been changed")
