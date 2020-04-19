from candybot import data
from candybot.engine import Candy, CandySettings
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, EmojiArgument, NameArgument


class AddCandyCommand(CandySettingsCommand):
    name = "add"
    help = "Adds a candy."
    aliases = ["addcandy", "candyadd"]
    examples = ["🍎 apple"]
    argument_spec = ArgumentSpec([EmojiArgument, NameArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        emoji = self.args["emoji"]
        name = self.args["name"]
        candy = Candy(name, emoji)
        candy_settings = CandySettings(candy)
        if candy in [x.candy for x in self.server_settings.candy]:
            await self.send("This candy already exists!")
        else:
            self.server_settings.candy.append(candy_settings)
            data.set_settings(self.server.id, self.server_settings)
            await self.send(f"{candy} has been added!")
