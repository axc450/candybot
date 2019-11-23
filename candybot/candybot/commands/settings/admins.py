from candybot.interface import database, converters
from candybot.commands.framework import SettingsCommand, ArgumentSpec, UserArgument


class AdminsCommand(SettingsCommand):
    name = "admins"
    help = "Adds or removes CandyBot admins or shows admins"
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([UserArgument], True)
    clean = True
    ignore = False

    # TODO: Ask for confirmation
    async def _run(self):
        admins = database.get_admins(self.message.guild.id)
        if self.user is None:
            self.title = ":lifter: CandyBot Admins"
            admins = [(await converters.to_user(str(x), self.message.guild)).mention for x in admins]
            await self.send("\n".join(admins) if admins else "All")
        else:
            if self.user.id in admins:
                database.set_admin(self.message.guild.id, self.user.id, remove=True)
                await self.send(f"{self.user.mention} was removed as a CandyBot admin")
            else:
                database.set_admin(self.message.guild.id, self.user.id, remove=False)
                await self.send(f"{self.user.mention} was added as a CandyBot admin")
