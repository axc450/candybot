from candybot import data
from candybot.commands.framework import ShopCommand, ArgumentSpec, PositiveAmountArgument, CandyArgument
from candybot.engine import CandyValue, Conversion


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
        candy = self.args[0]
        amount = self.args[1]
        shop = data.get_shop(self.server.id)
        conversion = Conversion(CandyValue(candy, amount))
        shop.conversions.append(conversion)
        data.set_shop(self.server.id, shop)
        await self.send(f"Conversion added to the shop")
