from candybot import data
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, CandyArgument


class RemoveCandyCommand(CandySettingsCommand):
    name = "remove"
    help = "Deletes a Candy."
    aliases = ["candydelete", "candyremove", "deletecandy", "removecandy"]
    examples = ["🍎", "apple"]
    argument_spec = ArgumentSpec([CandyArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        candy = self.args[0]
        # Candy Settings
        self.server_settings.remove_candy(candy)
        data.set_settings(self.server.id, self.server_settings)
        # Shop
        shop = data.get_shop(self.server.id)
        shop.remove_candy(candy)
        data.set_shop(self.server.id, shop)
        # Stats
        stats = data.get_stats(self.server.id)
        stats.remove_candy(candy)
        data.set_stats(self.server.id, stats)
        # Users
        users = data.get_users(self.server.id)
        for user in users:
            user.inv[candy] = 0
            data.set_user(user)
        await self.send(f"{candy} has been deleted!")
