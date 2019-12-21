from candybot.interface import database
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, CandyArgument


class RemoveCandyCommand(CandySettingsCommand):
    name = "remove"
    help = "Deletes a Candy."
    aliases = ["candydelete", "candyremove", "deletecandy", "removecandy"]
    examples = ["🍎", "apple"]
    argument_spec = ArgumentSpec([CandyArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        database.set_settings_candy_remove(self.server_id, self.candy.id)
        await self.send(f"{self.candy} has been deleted!")
