from candybot.interface import database, discord
from candybot.engine import CandyValue
from candybot.commands.framework import AdminCommand, ArgumentSpec, UserArgument, CandyArgument, AmountArgument


class SetCommand(AdminCommand):
    name = "set"
    help = "Sets a user's Candy."
    aliases = []
    examples = ["@User 5 🍎", "User#1234 10 apple"]
    argument_spec = ArgumentSpec([UserArgument, AmountArgument, CandyArgument], optional=False)
    clean = True
    ignore = False

    async def _run(self):
        user = self.args["user"]
        amount = self.args["amount"]
        candy = self.args["candy"]
        candy_value = CandyValue(candy, amount)
        database.set_inv(self.server_id, user.id, candy_value)
        await discord.send_embed(self.message.channel, f"You now have {candy_value.small_str} (set by {self.message.author.mention})", author=user)
