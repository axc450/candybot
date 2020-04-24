from candybot import data
from candybot.commands.framework import SettingsCommand, ArgumentSpec, AmountArgument


class MinCommand(SettingsCommand):
    name = "min"
    help = "Sets the minimum candy drop."
    aliases = []
    examples = ["5"]
    argument_spec = ArgumentSpec([AmountArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        amount = self.args[0]
        if amount > self.server_settings.max:
            return
        self.server_settings.min = amount
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"Minimum candy drop has been changed to `{amount}`")
