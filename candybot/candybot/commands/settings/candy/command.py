from candybot import data
from candybot.commands.framework import CandySettingsCommand, ArgumentSpec, CandyArgument, CommandNameArgument


class CommandCandyCommand(CandySettingsCommand):
    name = "command"
    help = "Changes the candy pick command."
    aliases = ["candycommand", "candycmd"]
    examples = ["catch"]
    argument_spec = ArgumentSpec([CandyArgument, CommandNameArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        candy = self.args[0]
        command = self.args[1]
        candy_settings = next(x for x in self.server_settings.candy if x.candy == candy)
        candy_settings.command = command
        data.set_settings(self.server.id, self.server_settings)
        await self.send(f"{candy} pick command has been changed")
