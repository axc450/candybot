from . import commands


def parse_command(raw, leaf):
    split_command = raw.split()
    return resolve_command(commands.Command, split_command, leaf)


def resolve_command(root_command, args, leaf):
    if args:
        match = not root_command.ignore and (root_command.name == args[0] or args[0] in root_command.aliases)
        for subcommand in root_command.subcommands:
            inner, iargs = resolve_command(subcommand, args[1:] if match else args, leaf)
            if inner:
                return inner, iargs
        if match and (not leaf or not root_command.subcommands):
            return root_command, args[1:]
    return None, args


async def parse_args(args, spec, server):
    match = find_match(args, spec)
    return await parse_match(match, server)


def find_match(args, spec):
    match = {}
    i = 0
    arg_type = None
    for i, arg_type in enumerate(spec):
        try:
            match[arg_type] = args[i]
        except IndexError:
            if len(spec) - 1 == i and spec.optional:
                return match
            raise
    if len(args) > i + 1:
        if arg_type and arg_type.ignore_spaces:
            match[arg_type] = " ".join(args[i:])
        else:
            raise IndexError
    return match


async def parse_match(match, server):
    return {x.name: await x.parse(y, server) for x, y in match.items()}
