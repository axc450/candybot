import candybot.engine
from candybot.commands.framework.commands import AdminCommand
from candybot.commands.framework.arguments import ArgumentSpec, CandyArgument


class ProcCommand(AdminCommand):
    name = "proc"
    help = "Procs some Candy in this channel."
    aliases = ["spawn", "drop"]
    examples = ["apple", "🍎"]
    argument_spec = ArgumentSpec([CandyArgument], False)
    clean = True
    ignore = False

    async def _run(self):
        candy = self.args["candy"]
        await candybot.engine.proc(self.server_settings, self.message.channel, candy, True)
