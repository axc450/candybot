from candybot.interface import database
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
        database.set_settings_prefix(self.message.guild.id, self.prefix)
        await self.send(f"Prefix has been changed to `{self.prefix}`")
