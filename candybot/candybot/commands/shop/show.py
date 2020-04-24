from candybot import data
from candybot.interface import discord
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
        shop = data.get_shop(self.server.id)
        shop_all = shop.all
        roles = await self.get_roles(shop_all["roles"])
        conversions = self.get_conversions(shop_all["conversions"])
        await self.send(fields=[("Roles", roles, True),
                                ("Conversions", conversions, True)])

    async def get_roles(self, roles):
        lines = []
        for position, item in roles:
            role = discord.get_role(self.message.guild, item.item)
            lines.append(f"[**{position}**] {role.mention} {item.cost.line_str}")
        return "\n".join(lines)

    def get_conversions(self, conversions):
        lines = []
        for position, item in conversions:
            lines.append(f"[**{position}**] {item}")
        return "\n".join(lines)
