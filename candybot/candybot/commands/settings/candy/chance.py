from candybot import utils, data
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, CandyArgument, AmountArgument


class ChanceCandyCommand(CandySettingsCommand):
    name = "chance"
    help = "Changes the chance value of a candy."
    aliases = ["candychance"]
    examples = ["🍎 10"]
    argument_spec = ArgumentSpec([CandyArgument, AmountArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        candy = self.args["candy"]
        amount = self.args["amount"]
        candy_settings = next(x for x in self.server_settings.candy if x.candy == candy)
        candy_settings.chance = amount
        data.set_settings(self.server.id, self.server_settings)
        new_chance = utils.chance_value_to_percent(self.server_settings.candy, candy)
        await self.send(f"{candy} chance has been changed to {new_chance:.2f}%")
