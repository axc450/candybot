# TODO: Everywhere these are used in the code should have a message attached


class CandyBotError(Exception):
    """Generic CandyBot Error"""


class MessageError(CandyBotError):
    """Message Error"""


class CommandError(CandyBotError):
    """Command Error"""


class CandyError(CandyBotError):
    """Candy Error"""


class ArgumentError(CandyBotError):
    """Argument Error"""
