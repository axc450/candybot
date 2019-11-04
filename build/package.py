import os
from zipfile import ZipFile


def main():
    files = get_files()
    create_package(files)


def get_files():
    result = []
    print("Adding CandyBot Source")
    result += find_files("candybot")
    print("Adding database scripts")
    result += find_files("dbscripts")
    print("Adding version")
    result.append("version")
    return result


def create_package(files):
    with ZipFile("build/package.zip", "w") as f:
        for file in files:
            f.write(file)
    print("Package Created!")


def find_files(folder):
    result = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                result.append(os.path.join(root, file))
    return result


main()
