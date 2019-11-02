from .arguments import ArgumentSpec, CommandArgument
from candybot.interface import discord, database
from candybot.exceptions import CommandError, ArgumentError
from . import parsers


class Command:
    ignore = True

    def __init__(self, server_settings, message=None, args=[]):
        self.server_settings = server_settings
        self.message = message
        self.args = args
        self._is_admin = None
        self._is_blacklisted = None

    def __getattr__(self, item):
        return None

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
    def is_admin(self):
        if self._is_admin is None:
            if self.message.author.guild_permissions.administrator:
                self._is_admin = True
            else:
                admins = database.get_admins(self.message.guild.id)
                self._is_admin = self.message.author.id in admins
        return self._is_admin

    @property
    def is_backlisted(self):
        if self._is_blacklisted is None:
            if self.message.author.guild_permissions.administrator:
                self._is_blacklisted = False
            else:
                blacklist = database.get_blacklist(self.message.guild.id)
                self._is_blacklisted = self.message.author.id in blacklist
        return self._is_blacklisted

    async def run(self):
        try:
            self._check_run()
            parsed_args = await parsers.parse_args(self.args, self.argument_spec, self.message.guild)
            self._set_args(parsed_args)
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

    def _set_args(self, args):
        for name in args:
            arg = args[name]
            setattr(self, name, arg)

    async def send(self, text=None, fields=[]):
        if self.title:
            await discord.send_embed(self.message.channel, text, title=self.title, color=self.message.guild.me.color, fields=fields)
        else:
            await discord.send_embed(self.message.channel, text, author=self.message.author)


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


class ShopCommand(Command):
    name = "shop"
    help = "CandyBot shop commands."
    aliases = []
    argument_spec = ArgumentSpec([CommandArgument], False)
    admin = False
    ignore = False

    @property
    def examples(self):
        raise NotImplementedError

    @property
    def clean(self):
        raise NotImplementedError

    def _run(self):
        print("hi")


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
