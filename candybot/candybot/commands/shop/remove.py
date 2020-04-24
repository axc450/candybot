from candybot import data
from candybot.commands.framework import ShopCommand, ArgumentSpec, ShopItemArgument
from candybot.engine import Role


class RemoveCommand(ShopCommand):
    name = "remove"
    help = "Removes a shop item."
    aliases = []
    examples = ["1"]
    argument_spec = ArgumentSpec([ShopItemArgument], False)
    clean = True
    admin = True
    ignore = False

    async def _run(self):
        item = self.args[0]
        shop = data.get_shop(self.server.id)
        shop.remove_item(item)
        data.set_shop(self.server.id, shop)
        await self.send(f"Removed the shop item [**{item}**]")

