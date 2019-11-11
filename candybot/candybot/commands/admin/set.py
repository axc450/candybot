from candybot.interface import database, discord
from candybot.engine import CandyValue
from candybot.commands.framework import AdminCommand, ArgumentSpec, UserArgument, CandyArgument, AmountArgument


class SetCommand(AdminCommand):
    name = "set"
    help = "Sets a user's Candy."
    aliases = []
    examples = ["@User 5 🍎", "User#1234 10 Apple"]
    argument_spec = ArgumentSpec([UserArgument, AmountArgument, CandyArgument], optional=False)
    clean = True
    ignore = False

    async def _run(self):
        candy_value = CandyValue(self.candy, self.amount)
        database.set_inv(self.message.guild.id, self.user.id, candy_value)
        await discord.send_embed(self.message.channel, f"You now have {candy_value.small_str} (set by {self.message.author.mention})", author=self.user)
