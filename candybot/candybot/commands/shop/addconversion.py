from candybot import data
from candybot.commands.framework import ShopCommand, ArgumentSpec, PositiveAmountArgument, CandyArgument
from candybot.engine import CandyValue
from candybot.engine.shop import Conversion


class AddConversionCommand(ShopCommand):
    name = "addconversion"
    help = "Adds a conversion to the shop."
    aliases = ["conversionadd"]
    examples = ["🍎 10"]
    argument_spec = ArgumentSpec([CandyArgument, PositiveAmountArgument], False)
    clean = True
    admin = True
    ignore = False

    async def _run(self):
        candy = self.args["candy"]
        amount = self.args["amount"]
        shop = data.get_shop(self.server.id)
        conversion = Conversion(CandyValue(candy, amount))
        shop.conversions.append(conversion)
        data.set_shop(self.server.id, shop)
        await self.send(f"Conversion added to the shop")
