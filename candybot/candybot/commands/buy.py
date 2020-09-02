from candybot import data, utils
from candybot.commands import Command
from candybot.engine import Role, Conversion, Upgrade
from candybot.interface import discord
from candybot.commands.framework import ArgumentSpec, ShopItemArgument


class BuyCommand(Command):
    name = "buy"
    help = "Buys an item from the shop."
    aliases = []
    examples = ["1"]
    argument_spec = ArgumentSpec([ShopItemArgument], False)
    clean = True
    admin = False
    ignore = False

    async def _run(self):
        item = self.args[0]
        shop = data.get_shop(self.server.id)
        shop_item = shop[item]
        user = data.get_user(self.server.id, self.author.id)
        if user.inv >= shop_item.cost:
            if isinstance(shop_item, Role):
                await self.buy_role(user, shop_item)
            elif isinstance(shop_item, Conversion):
                await self.buy_conversion(user, shop_item)
            elif isinstance(shop_item, Upgrade):
                await self.buy_upgrade(user, shop_item)
        else:
            await self.send(f"You need {shop_item.cost.line_str} to buy this item!")

    def update_stats(self):
        stats = data.get_stats(self.server.id)
        stats.shop_items_bought += 1
        data.set_stats(self.server.id, stats)

    async def buy_role(self, user, role):
        discord_role = discord.get_role(self.message.guild, role.role)
        if discord_role in self.message.author.roles:
            await self.send("You already have that role!")
        else:
            user.inv += -role.cost
            data.set_user(user)
            await discord.apply_role(self.message.author, discord_role)
            await self.send(f"You have bought the {discord_role.mention} role!")
            self.update_stats()

    async def buy_conversion(self, user, conversion):
        user.inv += -conversion.cost
        user.inv += conversion.candy_value
        data.set_user(user)
        self.update_stats()
        await self.send(f"You converted {conversion.cost.line_str} to {conversion.candy_value.small_str}")

    async def buy_upgrade(self, user, upgrade):
        user.inv += -upgrade.cost
        data.set_user(user)
        self.server_settings.update_candy_chance_value(upgrade.candy)
        data.set_settings(self.server.id, self.server_settings)
        self.update_stats()
        new_chance = utils.chance_value_to_percent(self.server_settings.candy, upgrade.candy)
        await self.send(f"{upgrade.candy} chance has been upgraded to {new_chance:.2f}%")
