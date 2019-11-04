from candybot import engine
from candybot.interface import database
from candybot.commands.framework import Command, ArgumentSpec


class PickCommand(Command):
    name = "pick"
    help = "Picks up dropped Candy"
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = True
    admin = False
    ignore = True

    def __init__(self, server_settings, message=None, args=[], invocation=None):
        super().__init__(server_settings, message, args)
        self.invocation = invocation if invocation else "pick"

    def __eq__(self, other):
        return self.invocation == other.invocation

    async def _run(self):
        state = engine.STATE.get(self.message.channel.id)
        if state and state.command == self:
            await state.message.delete()
            database.set_inv(self.message.guild.id, self.message.author.id, state.candy_value, update=True)
            await self.send(state.pick_str)
            del engine.STATE[self.message.channel.id]
