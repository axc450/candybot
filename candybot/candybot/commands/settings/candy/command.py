from candybot.interface import database
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
        database.set_settings_candy_command(self.server_id, self.candy.id, self.command)
        await self.send(f"{self.candy} pick command has been changed")
