from candybot.interface import database, discord
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
        inv = database.get_inv(self.server.id, self.author.id)[self.author.id]
        if inv >= item.cost:
            role = discord.get_role(self.message.guild, item.item)
            user = self.message.author
            if role in user.roles:
                await self.send("You already have that role!")
            else:
                database.set_inv(self.server.id, self.author.id, -item.cost, update=True)
                await discord.apply_role(self.message.author, role)
                database.set_stats_shop(self.server.id)
                await self.send(f"You have bought the {role.mention} role!")
        else:
            await self.send(f"You need {item.cost.line_str} to buy this item!")
