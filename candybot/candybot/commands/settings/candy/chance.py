from candybot import utils
from candybot.interface import database
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
        database.set_settings_candy_chance(self.server.id, candy.id, amount)
        candy = database.get_candy(self.server.id)
        new_chance = utils.chance_value_to_percent(candy)[candy]
        await self.send(f"{candy} chance has been changed to {new_chance:.2f}%")
