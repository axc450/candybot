from candybot import utils, data
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, CandyArgument, AmountArgument


class ChanceCandyCommand(CandySettingsCommand):
    name = "chance"
    help = "Changes the chance value of a candy."
    aliases = ["candychance"]
    examples = ["🍎 5"]
    argument_spec = ArgumentSpec([CandyArgument, AmountArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        candy = self.args[0]
        amount = self.args[1]
        self.server_settings.update_candy_chance_value(candy, amount)
        data.set_settings(self.server.id, self.server_settings)
        new_chance = utils.chance_value_to_percent(self.server_settings.candy, candy)
        await self.send(f"{candy} chance has been changed to {new_chance:.2f}%")
