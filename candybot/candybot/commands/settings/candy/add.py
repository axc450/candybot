from candybot.interface import database
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
        database.set_settings_candy_add(self.server_id, self.name, self.emoji)
        await self.send(f"{self.emoji} has been added!")
