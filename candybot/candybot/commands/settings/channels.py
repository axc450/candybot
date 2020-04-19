from candybot import data, converters
from candybot.commands.framework import SettingsCommand, ArgumentSpec, ChannelArgument


class ChannelsCommand(SettingsCommand):
    name = "channels"
    help = "Adds or removes CandyBot channels or shows enabled channels"
    aliases = []
    examples = ["", "#channel"]
    argument_spec = ArgumentSpec([ChannelArgument], True)
    clean = True
    ignore = False

    async def _run(self):
        channel = self.args.get("channel")
        channels = self.server_settings.channels
        if channel is None:
            self.title = ":hash: CandyBot Channels"
            channels = [(await converters.to_channel(str(x), self.message.guild)).mention for x in channels]
            await self.send("\n".join(channels) if channels else "All")
        else:
            if channel.id in channels:
                self.server_settings.channels.remove(channel.id)
                msg = f"{channel.mention} was removed as a CandyBot channel"
            else:
                self.server_settings.channels.add(channel.id)
                msg = f"{channel.mention} was added as a CandyBot channel"
            data.set_settings(self.server.id, self.server_settings)
            await self.send(msg)
