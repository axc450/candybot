from candybot.commands.framework import Command, ArgumentSpec, CommandArgument


class HelpCommand(Command):
    name = "help"
    help = "Shows command help/menus."
    aliases = []
    examples = ["", "inv", "shop buy"]
    argument_spec = ArgumentSpec([CommandArgument], True)
    clean = False
    admin = False
    ignore = False

    title = ":question: CandyBot Help"

    async def _run(self):
        command = self.command if self.command else Command
        if self.ignore_command(command):
            return
        if command.subcommands:
            await self.menu_help(command)
        else:
            await self.command_help(command)

    async def menu_help(self, command):
        lines = []
        for subcommand in command.subcommands:
            if self.ignore_command(subcommand):
                continue
            prefix = self.server_settings.prefix
            name = subcommand.full_name
            spec = subcommand.argument_spec
            help_ = subcommand.help.split("\n")[0]
            lines.append(f"`{prefix}{name}{' ' + str(spec) if spec else ''}` {help_}")
        await self.send("\n".join(lines))

    async def command_help(self, command):
        prefix = self.server_settings.prefix
        command_name = command.full_name
        # TODO: Align values
        arg_help = [f"`{x.name} `{x.help}" for x in command.argument_spec.args]
        arg_help = "\n".join(arg_help)
        arg_examples = [f"`{prefix}{command_name} {x}`" for x in command.examples]
        arg_examples = "\n".join(arg_examples)
        aliases = [f"`{x}`" for x in command.aliases]
        aliases = "\n".join(aliases)
        body = (f"`{prefix}{command_name}`\n"
                f"{command.help}\n")
        usage = (f"`{prefix}{command_name} {command.argument_spec}`\n"
                 f"{arg_help}\n")
        aliases = aliases if aliases else "None"
        examples = f"{arg_examples}"

        await self.send(body, fields=[("usage", usage, False), ("examples", examples, True), ("aliases", aliases, True)])

    def ignore_command(self, command):
        return (command.ignore and command != Command) or (command.admin is True and not self.is_admin)
