import __main__
from candybot.interface import discord, database
from candybot.commands.framework import Command, ArgumentSpec


class StatsCommand(Command):
    name = "stats"
    help = "Shows CandyBot stats."
    aliases = ["info"]
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = False
    admin = False
    ignore = False

    title = ":chart_with_upwards_trend: CandyBot Stats"

    async def _run(self):
        info = self._get_info()
        candy = self._get_candy()
        fields = [("info", info, True), ("candy", candy, True)]
        await self.send(fields=fields)

    def _get_info(self):
        server_settings = database.get_settings(self.server_id)
        channels = database.get_channels(self.server_id)
        channels = [discord.get_channel(self.message.guild, x).mention for x in channels]
        return "\n".join([
            self._make_field("Version", __main__.VERSION),
            self._make_field("Command Prefix", f"`{server_settings.prefix}`"),
            self._make_field("Drop Chance", f"{server_settings.chance * 100:.2f}%"),
            self._make_field("Drop Amount", f"{server_settings.min}-{server_settings.max}"),
            self._make_field("Candy Cap", server_settings.cap),
            self._make_field("Channels", ("\n" + "\n".join(channels)) if channels else "All")
        ])

    def _get_candy(self):
        candy = database.get_stats_candy(self.server_id)
        shop = database.get_stats_shop(self.server_id)
        return "\n".join([
            self._make_field("Candy Dropped", "\n" + candy.list_str),
            self._make_field("Shop Items Bought", shop),
        ])

    @staticmethod
    def _make_field(name, value):
        return f"**{name}:** {value}"
