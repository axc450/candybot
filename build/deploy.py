import os
import sys
import subprocess
import shutil
from zipfile import ZipFile


def main():
    check()
    stop()
    uninstall()
    install()
    migrate()
    start()
    clean()


def check():
    if len(sys.argv) != 3 or not sys.argv[1] or not sys.argv[2]:
        sys.exit("Script requires a CandyBot startup & shutdown command")
    if not os.path.exists("package.zip"):
        sys.exit("No package to deploy found")


def stop():
    print("Shutting down CandyBot")
    subprocess.call(sys.argv[2], shell=True)


def uninstall():
    print("Removing old version")
    delete("candybot")
    delete("dbscripts")
    delete("version")


def install():
    print("Installing new version")
    with ZipFile("package.zip", "r") as f:
        f.extractall()


def migrate():
    print("Migrating database")
    subprocess.call(f"{sys.executable} dbscripts/migrate.py", shell=True)


def start():
    print("Starting up CandyBot")
    subprocess.call(sys.argv[1], shell=True)


def clean():
    print("Cleaning up")
    delete("package.zip")
    delete(__file__)


def delete(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except FileNotFoundError:
        print(f"Couldn't find {path} to delete! Continuing anyway...")


main()
