from candybot import data
from candybot.interface import discord
from candybot.commands.framework import ShopCommand, ArgumentSpec, ShopItemArgument


class BuyCommand(ShopCommand):
    name = "buy"
    help = "Buys an item from the shop."
    aliases = []
    examples = ["1"]
    argument_spec = ArgumentSpec([ShopItemArgument], False)
    clean = True
    admin = False
    ignore = False

    async def _run(self):
        item = self.args["item"]
        shop = data.get_shop(self.server.id)
        shop_item = shop[item]
        user = data.get_user(self.server.id, self.author.id)
        if user.inv >= shop_item.cost:
            role = discord.get_role(self.message.guild, shop_item.item)
            if role in self.message.author.roles:
                await self.send("You already have that role!")
            else:
                user.inv += -shop_item.cost
                data.set_user(user)
                await discord.apply_role(self.message.author, role)
                stats = data.get_stats(self.server.id)
                stats.shop_items_bought += 1
                data.set_stats(self.server.id, stats)
                await self.send(f"You have bought the {role.mention} role!")
        else:
            await self.send(f"You need {shop_item.cost.line_str} to buy this item!")
