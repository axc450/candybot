from candybot import data
from candybot.commands.framework import ShopCommand, ArgumentSpec, ShopItemArgument, CandyArgument, AmountArgument


class CostCommand(ShopCommand):
    name = "cost"
    help = "Changes a shop item cost."
    aliases = []
    examples = ["1 🍎 15", "2 apple 20"]
    argument_spec = ArgumentSpec([ShopItemArgument, CandyArgument, AmountArgument], False)
    clean = True
    admin = True
    ignore = False

    async def _run(self):
        item = self.args["item"]
        candy = self.args["candy"]
        amount = self.args["amount"]
        shop = data.get_shop(self.server.id)
        shop[item].cost[candy] = amount
        data.set_shop(self.server.id, shop)
        await self.send(f"Updated the cost of shop item [**{item}**]")
