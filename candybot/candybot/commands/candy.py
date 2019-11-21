from candybot import utils
from candybot.interface import database
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
        candy = database.get_candy(self.message.guild.id)
        candy_chance = utils.chance_value_to_percent(candy)
        lines = [f"{x.emoji} {x.name} {candy_chance[x]:.2f}%" for x in candy]
        await self.send("\n".join(lines))
