from candybot import data
from candybot.commands.framework import SettingsCommand, ArgumentSpec, PercentArgument


class ChanceCommand(SettingsCommand):
    name = "chance"
    help = "Sets the chance for Candy to proc."
    aliases = []
    examples = ["20"]
    argument_spec = ArgumentSpec([PercentArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        percent = self.args["percent"]
        self.server_settings.chance = percent / 100
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"Candy proc chance has been changed to {percent}%")
