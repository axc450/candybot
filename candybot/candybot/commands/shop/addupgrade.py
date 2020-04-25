from candybot import data
from candybot.commands.framework import ShopCommand, ArgumentSpec, CandyArgument
from candybot.engine import Upgrade


class AddUpgradeCommand(ShopCommand):
    name = "addupgrade"
    help = "Adds an upgrade to the shop."
    aliases = ["upgradeadd"]
    examples = ["🍎"]
    argument_spec = ArgumentSpec([CandyArgument], False)
    clean = True
    admin = True
    ignore = False

    async def _run(self):
        candy = self.args[0]
        shop = data.get_shop(self.server.id)
        upgrade = Upgrade(candy)
        shop.upgrades.append(upgrade)
        data.set_shop(self.server.id, shop)
        await self.send(f"Upgrade added to the shop")
