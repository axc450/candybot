from candybot import data
from candybot.commands.framework import ShopSettingsCommand, ArgumentSpec, RoleArgument
from candybot.engine import Role


class AddRoleCommand(ShopSettingsCommand):
    name = "addrole"
    help = "Adds a role to the shop."
    aliases = ["roleadd"]
    examples = ["@role", "12345"]
    argument_spec = ArgumentSpec([RoleArgument], False)
    clean = True
    admin = True
    ignore = False

    async def _run(self):
        role = self.args[0]
        shop = data.get_shop(self.server.id)
        shop.roles.append(Role(role.id))
        data.set_shop(self.server.id, shop)
        await self.send(f"{role.mention} added to the shop")
