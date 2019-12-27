from candybot.interface import database, converters
from candybot.commands.framework import SettingsCommand, ArgumentSpec, ChannelArgument


class ChannelsCommand(SettingsCommand):
    name = "channels"
    help = "Adds or removes CandyBot channels or shows enabled channels"
    aliases = []
    examples = ["", "#channel"]
    argument_spec = ArgumentSpec([ChannelArgument], True)
    clean = True
    ignore = False

    # TODO: Ask for confirmation
    async def _run(self):
        channel = self.args.get("channel")
        channels = database.get_channels(self.server.id)
        if channel is None:
            self.title = ":hash: CandyBot Channels"
            channels = [(await converters.to_channel(str(x), self.message.guild)).mention for x in channels]
            await self.send("\n".join(channels) if channels else "All")
        else:
            if channel.id in channels:
                database.set_channel(self.server.id, channel.id, remove=True)
                await self.send(f"{channel.mention} was removed as a CandyBot channel")
            else:
                database.set_channel(self.server.id, channel.id, remove=False)
                await self.send(f"{channel.mention} was added as a CandyBot channel")
