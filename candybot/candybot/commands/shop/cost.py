from candybot.interface import database
from candybot.commands.framework import ShopCommand, ArgumentSpec, RoleArgument, CandyArgument, AmountArgument


class CostCommand(ShopCommand):
    name = "cost"
    help = "Changes a shop item cost."
    aliases = []
    examples = ["@role 🍎 15", "12345 apple 20"]
    argument_spec = ArgumentSpec([RoleArgument, CandyArgument, AmountArgument], False)
    clean = True
    admin = True
    ignore = False

    async def _run(self):
        database.set_shop_cost(self.message.guild.id, self.role.id, self.candy, self.amount)
        await self.send(f"Updated the cost of {self.role.mention}")
