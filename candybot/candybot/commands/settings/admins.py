from candybot import data, converters
from candybot.commands.framework import SettingsCommand, ArgumentSpec, UserArgument


class AdminsCommand(SettingsCommand):
    name = "admins"
    help = "Adds or removes CandyBot admins or shows admins"
    aliases = []
    examples = ["", "@User", "User#1234", "123456789"]
    argument_spec = ArgumentSpec([UserArgument], True)
    clean = True
    ignore = False

    async def _run(self):
        user = self.args.get("user")
        admins = self.server_settings.admins
        if user is None:
            self.title = ":lifter: CandyBot Admins"
            admins = [(await converters.to_user(str(x), self.message.guild)).mention for x in admins]
            await self.send("\n".join(admins))
        else:
            if user.id in admins:
                self.server_settings.admins.remove(user.id)
                msg = f"{user.mention} was removed as a CandyBot admin"
            else:
                self.server_settings.admins.add(user.id)
                msg = f"{user.mention} was added as a CandyBot admin"
            data.set_settings(self.server.id, self.server_settings)
            await self.send(msg)
