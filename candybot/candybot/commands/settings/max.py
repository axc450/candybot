from candybot import data
from candybot.commands.framework import SettingsCommand, ArgumentSpec, AmountArgument


class MaxCommand(SettingsCommand):
    name = "max"
    help = "Sets the maximum candy drop."
    aliases = []
    examples = ["50"]
    argument_spec = ArgumentSpec([AmountArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        amount = self.args["amount"]
        if amount < self.server_settings.min:
            return
        self.server_settings.max = amount
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"Maximum candy drop has been changed to `{amount}`")
