from candybot.interface import converters


# TODO: Define a get index to get the args?
class ArgumentSpec:
    def __init__(self, args, optional):
        self.args = args
        self.optional = optional

    def __iter__(self):
        return iter(self.args)

    def __len__(self):
        return len(self.args)

    def __str__(self):
        args = []
        for arg in self.args:
            if arg == self.args[-1] and self.optional:
                args.append(f"[{arg.name}]")
            else:
                args.append(f"<{arg.name}>")
        return " ".join(args)


class Argument:
    ignore_spaces = False

    @property
    def name(self):
        raise NotImplementedError

    @property
    def help(self):
        raise NotImplementedError

    @staticmethod
    def parse(arg, server):
        raise NotImplementedError


class TextArgument(Argument):
    name = "text"
    help = "Text"
    ignore_spaces = True

    @staticmethod
    async def parse(arg, server):
        # TODO: Maybe do some validation here
        return arg


class NameArgument(Argument):
    name = "name"
    help = "Name of the candy"

    @staticmethod
    async def parse(arg, server):
        # TODO: Maybe do some validation here
        return arg


class UserArgument(Argument):
    name = "user"
    help = "Mention, Tag or ID of a Discord user"

    @staticmethod
    async def parse(arg, server):
        return await converters.to_user(arg, server)


class ChannelArgument(Argument):
    name = "channel"
    help = "Mention, Name or ID of a Discord channel"

    @staticmethod
    async def parse(arg, server):
        return await converters.to_channel(arg, server)


class RoleArgument(Argument):
    name = "role"
    help = "Mention, Name or ID of a Discord role"

    @staticmethod
    async def parse(arg, server):
        return await converters.to_role(arg, server)


class CommandArgument(Argument):
    name = "command"
    help = "CandyBot command"
    ignore_spaces = True

    @staticmethod
    async def parse(arg, server):
        return converters.to_command(arg)


class CommandNameArgument(Argument):
    name = "command"
    help = "CandyBot command"

    @staticmethod
    async def parse(arg, server):
        return converters.to_command_name(arg)


class CandyArgument(Argument):
    name = "candy"
    help = "Candy emoji"

    @staticmethod
    async def parse(arg, server):
        return converters.to_candy(arg, server)


class AmountArgument(Argument):
    name = "amount"
    help = "Amount of candy"

    @staticmethod
    async def parse(arg, server):
        return converters.to_amount(arg, True)


class ZeroAmountArgument(AmountArgument):
    @staticmethod
    async def parse(arg, server):
        return converters.to_amount(arg, False)


class ShopItemArgument(Argument):
    name = "item"
    help = "Shop item ID"

    @staticmethod
    async def parse(arg, server):
        return converters.to_shop_item(arg, server)


class PercentArgument(Argument):
    name = "percent"
    help = "Percentage"

    @staticmethod
    async def parse(arg, server):
        return converters.to_percent(arg)


class PrefixArgument(Argument):
    name = "prefix"
    help = "Prefix"

    @staticmethod
    async def parse(arg, server):
        return converters.to_prefix(arg)


class EmojiArgument(Argument):
    name = "emoji"
    help = "Emoji"

    @staticmethod
    async def parse(arg, server):
        return await converters.to_emoji(arg, server)
