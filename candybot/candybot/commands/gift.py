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
        user = self.args["user"]
        amount = self.args["amount"]
        candy = self.args["candy"]

        # Users shouldn't be able to gift themselves...
        if self.message.author == user:
            return
        invs = database.get_inv(self.server.id, self.author.id, user.id)
        author_candy = invs[self.author.id][candy]
        user_candy = invs[user.id][candy]
        if author_candy < amount:
            await self.send(f"You don't have enough {candy}!")
        elif user_candy >= self.server_settings.cap:
            await self.send(f"{user.mention} cannot obtain any more {candy}!")
        else:
            candy_value = self.calculate_pick(user_candy, CandyValue(candy, amount))
            database.set_inv(self.server.id, self.author.id, -candy_value, update=True)
            database.set_inv(self.server.id, user.id, candy_value, update=True)
            await discord.send_embed(self.message.channel,
                                     f"You have been gifted {candy_value.small_str} by {self.message.author.mention}\n"
                                     f"You now have {(user_candy + candy_value).small_str}",
                                     author=user)

    # TODO: Combine this with the one in PickCommand and move
    def calculate_pick(self, current_candy, gifted_candy):
        # What the candy value would be if there was no cap
        new_candy = current_candy + gifted_candy.value
        # What the candy value should actually be
        calculated_candy = gifted_candy.value - max(new_candy - self.server_settings.cap, 0)
        return CandyValue(gifted_candy.candy, calculated_candy)
