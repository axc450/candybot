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
        database.set_settings_candy_chance(self.message.guild.id, self.candy.id, self.amount)
        candy = database.get_candy(self.message.guild.id)
        new_chance = utils.chance_value_to_percent(candy)[self.candy]
        await self.send(f"{self.candy} chance has been changed to {new_chance:.2f}%")
