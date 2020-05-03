import __main__
from candybot import data
from candybot.interface import discord
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
        return "\n".join([
            self._make_field("Version", __main__.VERSION),
            self._make_field("Command Prefix", f"`{self.server_settings.prefix}`"),
            self._make_field("Drop Chance", f"{self.server_settings.chance * 100:.2f}%"),
            self._make_field("Drop Amount", f"{self.server_settings.min}-{self.server_settings.max}"),
            self._make_field("Candy Cap", self.server_settings.cap)
        ])

    def _get_candy(self):
        stats = data.get_stats(self.server.id)
        return "\n".join([
            self._make_field("Candy Dropped", "\n" + stats.candy_dropped.list_str),
            self._make_field("Shop Items Bought", stats.shop_items_bought)
        ])

    @staticmethod
    def _make_field(name, value):
        return f"**{name}:** {value}"
