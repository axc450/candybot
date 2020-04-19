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
        roles = await self.get_roles(shop)
        await self.send(fields=[("Roles", roles, True)])

    async def get_roles(self, shop):
        lines = []
        for i, item in enumerate(shop.roles):
            role = discord.get_role(self.message.guild, item.item)
            lines.append(f"[**{i+1}**] {role.mention} {item.cost.line_str}")
        return "\n".join(lines)
