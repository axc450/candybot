import os
import inspect
import importlib
from candybot.commands.framework import Command, parse_command

COMMAND_NAMES = []


def import_commands(folder, package_tree=[]):
    """
    Custom recursive importer that searches for Python files and imports the command class within them.
    :param folder: The path to the current folder to search.
    :param package_tree: Package reference as a str list (used to import the module).
    """
    # Loop through all files and folders
    for file in os.listdir(folder):
        file_parts = file.split(".")
        # Python file, so import it
        if file_parts[-1] == "py" and file_parts[0] != "__init__":
            # Get the name of the module to import
            module_str = ".".join(["candybot", "commands"] + package_tree + [str(file_parts[0])])
            # Import it
            module = importlib.import_module(module_str)
            # Extract the class defined in the module
            command = inspect.getmembers(module, lambda x: inspect.isclass(x) and x.__module__ == module.__name__)[0]
            # Add it to the global namespace (the import above only imports to the current scope)
            globals()[command[0]] = command[1]
        # Folder, so look in it
        elif len(file_parts) == 1 and file_parts[0] not in ["__pycache__", "framework"]:
            import_commands(os.path.join(folder, file_parts[0]), package_tree + [file_parts[0]])
        # Ignore
        else:
            continue


def get_subcommands(command):
    subclasses = command.__subclasses__()
    return sorted(subclasses, key=lambda x: bool(x.__subclasses__()))


def get_full_name(command):
    if isinstance(command.name, str):
        return get_full_name(command.__bases__[0]) + [command.name]
    else:
        return []


def setup_command(command):
    command.subcommands = get_subcommands(command)
    command.full_name = " ".join(get_full_name(command))
    if not command.ignore:
        COMMAND_NAMES.append(command.name)
        COMMAND_NAMES.extend(command.aliases)
    for subcommand in command.subcommands:
        setup_command(subcommand)


import_commands(os.path.dirname(__file__))
setup_command(Command)
