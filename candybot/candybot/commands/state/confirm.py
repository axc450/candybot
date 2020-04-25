from candybot import engine
from candybot.commands.framework import Command, ArgumentSpec


class ConfirmCommand(Command):
    name = "yes"
    help = "Confirms a prompt"
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = True
    admin = True
    ignore = True

    def __init__(self, server_settings, invocation, message=None, raw_args=[]):
        super().__init__(server_settings, message, raw_args)
        self.invocation = invocation

    async def _run(self):
        async with engine.STATE_LOCK:
            state = engine.STATE.get(self.channel.id)
            if not self.invocation == self.name:
                return
            del engine.STATE[self.channel.id]
        await state.message.delete()
        await state.command.accept()

