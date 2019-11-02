from candybot.interface import database
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
        if self.amount < self.server_settings.min:
            return
        database.set_settings_max(self.message.guild.id, self.amount)
        await self.send(f"Maximum candy drop has been changed to `{self.amount}`")
