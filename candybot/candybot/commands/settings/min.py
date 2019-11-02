from candybot.interface import database
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
        if self.amount > self.server_settings.max:
            return
        database.set_settings_min(self.message.guild.id, self.amount)
        await self.send(f"Minimum candy drop has been changed to `{self.amount}`")
