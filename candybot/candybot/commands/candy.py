from candybot import utils
from candybot.commands.framework import Command, ArgumentSpec


class CandyCommand(Command):
    name = "candy"
    help = "Shows the available candy."
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = False
    admin = False
    ignore = False

    title = ":candy: Candy"

    async def _run(self):
        candy_settings = self.server_settings.candy
        candy_chance = utils.chance_value_to_percent(candy_settings)
        lines = [f"{x.emoji} {x.name} {y:.2f}%" for x, y in candy_chance]
        await self.send("\n".join(lines))
