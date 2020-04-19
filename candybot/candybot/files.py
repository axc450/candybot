from candybot.interface import files
from candybot.interface.files import load_file


def load_version():
    version = files.load_file("version", "Could not find a CandyBot version!")
    return f"v{version}"


def load_settings():
    return load_file("settings.json", "Could not load the settings file!", is_json=True)

