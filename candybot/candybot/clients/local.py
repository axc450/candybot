import asyncio
import traceback
from candybot import engine, converters
from candybot.interface import discord

GUILD_ID = 1
USER_ID = 2
CHANNEL_ID = 3


class Permissions:
    administrator = True


class Member:
    name = "MEMBER"
    mention = "@MEMBER"
    avatar_url = "IMAGE"
    id = USER_ID
    bot = False
    color = "COLOR"
    roles = []
    guild_permissions = Permissions()

    @staticmethod
    async def add_roles(role, reason):
        pass


class Guild:
    id = GUILD_ID
    me = Member()

    @staticmethod
    def get_role(_):
        return Role()


class Role:
    mention = "@ROLE"


class Channel:
    id = CHANNEL_ID
    mention = "#CHANNEL"
    guild = Guild()

    @staticmethod
    async def send(embed):
        print(embed)
        return Message(embed)


class Message:
    author = Member()
    guild = Guild()
    channel = Channel()

    def __init__(self, content):
        self.content = content

    async def delete(self):
        pass


class Embed:
    def __init__(self, description, title, color):
        self.description = description if description is not None else ""
        self.fields = []
        self.title = title
        self.color = color
        self.name = None
        self.icon_url = None

    def __str__(self):
        text = "\n".join([self.description] + self.fields)
        attrs = {x: y for x, y in self.__dict__.items() if x not in ["description", "fields"]}
        return f"{text}\n{attrs}"

    def set_author(self, name, icon_url):
        self.name = name
        self.icon_url = icon_url

    def add_field(self, name, value, **_):
        self.fields.append(f"{name}\n{value}")


class DiscordModule:
    Embed = Embed


class MemberConverter:
    @staticmethod
    async def convert(*_):
        return Member()


class TextChannelConverter:
    @staticmethod
    async def convert(*_):
        return Channel()


class Converter:
    MemberConverter = MemberConverter
    TextChannelConverter = TextChannelConverter


class CommandsModule:
    converter = Converter()


def patch():
    discord.__dict__["discord"] = DiscordModule()
    converters.__dict__["converter"] = Converter()


async def main():
    while True:
        try:
            x = Message(input("> "))
            await engine.handle_message(x)
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()


def start():
    patch()
    print("CandyBot Ready")
    asyncio.run(main())
