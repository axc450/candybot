from candybot import data
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
        self.server_settings.cap = amount
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"Candy cap been changed to `{amount}`")
