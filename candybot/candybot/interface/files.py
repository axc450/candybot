def load_version():
    version = load_file("version", "Could not find a CandyBot version!")
    return f"v{version}"


def load_token():
    return load_file("token", "Could not load the Discord token!")


def load_file(file, error):
    try:
        with open(file) as f:
            return f.read()
    except OSError:
        print(error)
