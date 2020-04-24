from candybot import data
from candybot.commands.framework import SettingsCommand, ArgumentSpec, PrefixArgument


class PrefixCommand(SettingsCommand):
    name = "prefix"
    help = "Sets the prefix for CandyBot to use on this server."
    aliases = []
    examples = ["/"]
    argument_spec = ArgumentSpec([PrefixArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        prefix = self.args[0]
        self.server_settings.prefix = prefix
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"Prefix has been changed to `{prefix}`")
