from candybot import data, converters
from candybot.commands.framework import AdminCommand, ArgumentSpec, UserArgument


class BlacklistCommand(AdminCommand):
    name = "blacklist"
    help = "Shows current blacklist or blacklists a user from interacting with CandyBot."
    aliases = ["bl"]
    examples = ["", "@User", "User#1234", "123456789"]
    argument_spec = ArgumentSpec([UserArgument], True)
    clean = True
    ignore = False
    
    async def _run(self):
        user = self.args[0]
        blacklist = self.server_settings.blacklist
        if user is None:
            self.title = ":lock: CandyBot Blacklist"
            blacklist = [(await converters.to_user(str(x), self.message.guild)).mention for x in blacklist]
            await self.send("\n".join(blacklist))
        else:
            if user.id in blacklist:
                self.server_settings.blacklist.remove(user.id)
                msg = f"{user.mention} was removed from the CandyBot blacklist"
            else:
                self.server_settings.blacklist.append(user.id)
                msg = f"{user.mention} was added to the CandyBot blacklist"
            data.set_settings(self.server.id, self.server_settings)
            await self.send(msg)
