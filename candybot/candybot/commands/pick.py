from candybot import engine, data
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
        user = data.get_user(self.server.id, self.author.id)
        # Need to obtain the lock to avoid multiple users from picking the candy
        async with engine.STATE_LOCK:
            state = engine.STATE.get(self.channel.id)
            current_candy = user.inv[state.candy_value.candy] if state else None
            if state and state.command.invocation == self.invocation and current_candy < self.server_settings.cap:
                # This user will pick up the candy drop
                # Must clear the state inside the lock to avoid other users from picking
                del engine.STATE[self.channel.id]
            else:
                # An earlier command was chosen to be processed or the invocation didn't match
                return
        # Code here will be run after the lock is released and should handle the user successfully picking up candy
        await state.message.delete()
        # Replace the dropped candy value to not exceed the candy cap
        state.candy_value.value = self.add_with_cap(current_candy, state.candy_value.value)
        user.inv += state.candy_value
        data.set_user(user)
        await self.send(state.pick_str)

