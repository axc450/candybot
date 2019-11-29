from candybot.interface import database, discord
from candybot.engine import CandyValue
from candybot.commands.framework import Command, ArgumentSpec, UserArgument, CandyArgument, ZeroAmountArgument


class GiftCommand(Command):
    name = "gift"
    help = "Gifts candy to someone else."
    aliases = ["give"]
    examples = ["@User 5 🍎", "User#1234 10 apple"]
    argument_spec = ArgumentSpec([UserArgument, ZeroAmountArgument, CandyArgument], optional=False)
    clean = True
    admin = False
    ignore = False

    # TODO: Reduce database calls in here if possible (use a cache?)
    async def _run(self):
        # Users shouldn't be able to gift themselves...
        if self.message.author == self.user:
            return
        invs = database.get_inv(self.message.guild.id, self.message.author.id, self.user.id)
        if invs[self.message.author.id][self.candy] < self.amount:
            await discord.send_embed(self.message.channel, f"You don't have enough {self.candy}!", author=self.message.author)
        else:
            candy_value = CandyValue(self.candy, self.amount)
            database.set_inv(self.message.guild.id, self.message.author.id, -candy_value, update=True)
            database.set_inv(self.message.guild.id, self.user.id, candy_value, update=True)
            await discord.send_embed(self.message.channel,
                                     f"You have been gifted {candy_value.small_str} by {self.message.author.mention}\n"
                                     f"You now have {(invs[self.user.id][self.candy] + candy_value).small_str}",
                                     author=self.user)
