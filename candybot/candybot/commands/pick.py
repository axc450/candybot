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

    def __init__(self, server_settings, message=None, raw_args=[], invocation=None):
        super().__init__(server_settings, message, raw_args)
        self.invocation = invocation if invocation else "pick"

    async def _run(self):
        # Need to obtain the lock to avoid multiple users from picking the candy
        async with engine.STATE_LOCK:
            state = engine.STATE.get(self.channel_id)
            if state and state.command.invocation == self.invocation:
                # This user will pick up the candy drop
                # Must clear the state inside the lock to avoid other users from picking
                del engine.STATE[self.channel_id]
            else:
                # An earlier command was chosen to be processed or the invocation didn't match
                return
        # Code here will be run after the lock is released and should handle the user successfully picking up candy
        await state.message.delete()
        database.set_inv(self.server_id, self.author_id, state.candy_value, update=True)
        await self.send(state.pick_str)
