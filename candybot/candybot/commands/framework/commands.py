from .arguments import ArgumentSpec, CommandArgument
from candybot.interface import discord
from candybot.exceptions import CommandError, ArgumentError
from . import parsers
from ...engine import Settings


class Command:
    ignore = True
    title = None

    def __init__(self, server_settings, message=None, raw_args=[]):
        self.server_settings: Settings = server_settings
        self.message = message
        self.raw_args = raw_args
        self.args = {}

    @property
    def name(self):
        raise NotImplementedError

    @property
    def help(self):
        raise NotImplementedError

    @property
    def aliases(self):
        raise NotImplementedError

    @property
    def examples(self):
        raise NotImplementedError

    @property
    def argument_spec(self):
        raise NotImplementedError

    @property
    def clean(self):
        raise NotImplementedError

    @property
    def admin(self):
        raise NotImplementedError

    def _run(self):
        raise NotImplementedError

    @property
    def server(self):
        return self.message.guild

    @property
    def author(self):
        return self.message.author

    @property
    def channel(self):
        return self.message.channel

    @property
    def is_admin(self):
        return (self.message.author.guild_permissions.administrator or
                self.author.id in self.server_settings.admins)

    @property
    def is_blacklisted(self):
        return self.author.id in self.server_settings.blacklist and not self.is_admin

    async def run(self):
        try:
            self._check_run()
            self.args = await parsers.parse_args(self)
        # TODO: Check these are correct
        except (CommandError, ArgumentError, IndexError):
            return
        else:
            await self._run()
        finally:
            if self.clean:
                await self.message.delete()

    def _check_run(self):
        if self.admin and not self.is_admin:
            raise CommandError
        if self.is_blacklisted:
            raise CommandError

    async def send(self, text=None, fields=[]):
        if self.title:
            return await discord.send_embed(self.message.channel, text, title=self.title, color=self.message.guild.me.color, fields=fields)
        else:
            return await discord.send_embed(self.message.channel, text, author=self.message.author)

    def add_with_cap(self, a, b):
        # What the value would be if there was no cap
        total = a + b
        # What the value should actually be
        return b - max(total - self.server_settings.cap, 0)


class AdminCommand(Command):
    name = "admin"
    help = "CandyBot admin commands."
    aliases = []
    argument_spec = ArgumentSpec([CommandArgument], False)
    admin = True
    ignore = False

    @property
    def examples(self):
        raise NotImplementedError

    @property
    def clean(self):
        raise NotImplementedError

    def _run(self):
        raise NotImplementedError


class SettingsCommand(Command):
    name = "settings"
    help = "CandyBot setup commands."
    aliases = []
    argument_spec = ArgumentSpec([CommandArgument], False)
    admin = True
    ignore = False

    @property
    def examples(self):
        raise NotImplementedError

    @property
    def clean(self):
        raise NotImplementedError

    def _run(self):
        raise NotImplementedError


class ShopSettingsCommand(SettingsCommand):
    name = "shop"
    help = "CandyBot shop commands."
    aliases = []
    argument_spec = ArgumentSpec([CommandArgument], False)
    admin = True
    ignore = False

    @property
    def examples(self):
        raise NotImplementedError

    @property
    def clean(self):
        raise NotImplementedError

    def _run(self):
        raise NotImplementedError


class CandySettingsCommand(SettingsCommand):
    name = "candy"
    help = "CandyBot candy commands."
    aliases = []
    argument_spec = ArgumentSpec([CommandArgument], False)
    admin = True
    ignore = False

    @property
    def examples(self):
        raise NotImplementedError

    @property
    def clean(self):
        raise NotImplementedError

    def _run(self):
        raise NotImplementedError
