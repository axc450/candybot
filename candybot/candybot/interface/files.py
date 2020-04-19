import json


def load_file(file, error, is_json=False):
    try:
        with open(file) as f:
            if is_json:
                return json.load(f)
            else:
                return f.read()
    except OSError:
        print(error)
