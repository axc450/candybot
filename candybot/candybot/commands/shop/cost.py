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
        role = self.args["role"]
        candy = self.args["candy"]
        amount = self.args["amount"]
        database.set_shop_cost(self.server.id, role.id, candy, amount)
        await self.send(f"Updated the cost of {role.mention}")
