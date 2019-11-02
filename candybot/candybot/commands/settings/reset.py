from candybot import engine
from candybot.commands.framework import SettingsCommand, ArgumentSpec


# TODO: Reset should reset state too
class ResetCommand(SettingsCommand):
    name = "reset"
    help = "Resets all CandyBot settings and stats."
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = True
    ignore = False

    # TODO: Ask for confirmation
    async def _run(self):
        await engine.teardown(self.message.guild.id)
        await engine.setup(self.message.guild.id)
        await self.send("CandyBot has been reset!")
