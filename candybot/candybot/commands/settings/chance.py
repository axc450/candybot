from candybot.interface import database
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
        database.set_settings_chance(self.server.id, percent / 100)
        await self.send(f"Candy proc chance has been changed to {percent}%")
