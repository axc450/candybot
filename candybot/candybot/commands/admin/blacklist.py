from candybot.interface import database
from candybot.commands.framework import AdminCommand, ArgumentSpec, UserArgument


class BlacklistCommand(AdminCommand):
    name = "blacklist"
    help = "Blacklists a user from interacting with CandyBot."
    aliases = ["bl"]
    examples = ["@User", "User#1234", "123456789"]
    argument_spec = ArgumentSpec([UserArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        blacklist = database.get_blacklist(self.message.guild.id)
        if self.user.id in blacklist:
            database.set_blacklist(self.message.guild.id, self.user.id, remove=True)
            await self.send(f"{self.user.mention} was removed from the CandyBot blacklist")
        else:
            database.set_blacklist(self.message.guild.id, self.user.id, remove=False)
            await self.send(f"{self.user.mention} was added to the CandyBot blacklist")
