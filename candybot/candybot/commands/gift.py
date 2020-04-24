from candybot import data
from candybot.interface import discord
from candybot.engine import CandyValue
from candybot.commands.framework import Command, ArgumentSpec, UserArgument, CandyArgument, PositiveAmountArgument


class GiftCommand(Command):
    name = "gift"
    help = "Gifts candy to someone else."
    aliases = ["give"]
    examples = ["@User 5 🍎", "User#1234 10 apple"]
    argument_spec = ArgumentSpec([UserArgument, PositiveAmountArgument, CandyArgument], optional=False)
    clean = True
    admin = False
    ignore = False

    # TODO: Reduce database calls in here if possible (use a cache?)
    async def _run(self):
        user = self.args[0]
        candy = self.args[1]
        amount = self.args[2]

        # Users shouldn't be able to gift themselves...
        if self.message.author == user:
            return
        # Get info
        sender = data.get_user(self.server.id, self.author.id)
        receiver = data.get_user(self.server.id, user.id)
        sender_candy = sender.inv[candy]
        receiver_candy = receiver.inv[candy]
        # Do some checking
        if sender_candy < amount:
            await self.send(f"You don't have enough {candy}!")
        elif receiver_candy >= self.server_settings.cap:
            await self.send(f"{user.mention} cannot obtain any more {candy}!")
        else:
            # Get the value that should actually be gifted (ensure cap is not exceeded)
            value_update = self.add_with_cap(receiver_candy, amount)
            # Update user candy values
            sender.inv[candy] = sender_candy - value_update
            receiver.inv[candy] = receiver_candy + value_update
            # Set the new inventories
            data.set_user(sender)
            data.set_user(receiver)
            # Handle output
            gift_as_candy_value = CandyValue(candy, value_update)
            receiver_as_candy_value = CandyValue(candy, receiver.inv[candy])
            await discord.send_embed(self.message.channel,
                                     f"You have been gifted {gift_as_candy_value.small_str} by {self.message.author.mention}\n"
                                     f"You now have {receiver_as_candy_value.small_str}",
                                     author=user)
