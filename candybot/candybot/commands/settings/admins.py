from candybot.interface import database
from candybot.commands.framework import SettingsCommand, ArgumentSpec, UserArgument


class AdminsCommand(SettingsCommand):
    name = "admins"
    help = "Adds or removes CandyBot admins"
    aliases = []
    examples = []
    argument_spec = ArgumentSpec([UserArgument], False)
    clean = True
    ignore = False

    # TODO: Ask for confirmation
    async def _run(self):
        admins = database.get_admins(self.message.guild.id)
        if self.user.id in admins:
            database.set_admin(self.message.guild.id, self.user.id, remove=True)
            await self.send(f"{self.user.mention} was removed as a CandyBot admin")
        else:
            database.set_admin(self.message.guild.id, self.user.id, remove=False)
            await self.send(f"{self.user.mention} was added as a CandyBot admin")
