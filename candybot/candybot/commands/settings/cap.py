from candybot.interface import database
from candybot.commands.framework import SettingsCommand, ArgumentSpec, AmountArgument


class CapCommand(SettingsCommand):
    name = "cap"
    help = "Sets the candy cap."
    aliases = []
    examples = ["50"]
    argument_spec = ArgumentSpec([AmountArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        amount = self.args["amount"]
        database.set_settings_cap(self.server.id, amount)
        await self.send(f"Candy cap been changed to `{amount}`")
