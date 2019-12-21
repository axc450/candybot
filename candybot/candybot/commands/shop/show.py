from candybot.interface import database, discord
from candybot.commands.framework import ShopCommand, ArgumentSpec


class ShowCommand(ShopCommand):
    name = "show"
    help = "Shows the shop."
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = False
    admin = False
    ignore = False

    title = ":dollar: CandyBot Shop"

    async def _run(self):
        shop = database.get_shop(self.server_id)
        shop_str = await self._shop_to_str(shop)
        await self.send(shop_str)

    async def _shop_to_str(self, shop):
        lines = []
        for i, item in enumerate(shop.items):
            role = discord.get_role(self.message.guild, item.item)
            lines.append(f"[**{i+1}**] {role.mention} {item.cost.line_str}")
        return "\n".join(lines)
