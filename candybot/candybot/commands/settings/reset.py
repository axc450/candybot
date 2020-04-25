from candybot import data
from candybot.engine import Settings, Shop, Stats, engine
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

    confirm_msg = "Are you sure you want to reset CandyBot?"

    async def _run(self):
        await engine.confirm(self)

    async def accept(self):
        data.set_settings(self.server.id, Settings.from_default())
        data.set_shop(self.server.id, Shop.from_default())
        data.set_stats(self.server.id, Stats.from_default())
        users = data.get_users(self.server.id)
        for user in users:
            user.remove_inv()
            data.set_user(user)
        await self.send("CandyBot has been reset!")