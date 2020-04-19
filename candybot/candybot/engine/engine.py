from asyncio.locks import Lock
from candybot import utils, commands, data
from candybot.engine import CandyValue, CandyDrop

# The current state of channels
# Channel ID -> Candy Drop
STATE = {}

# Mutex lock for STATE
STATE_LOCK = Lock()


async def handle_message(message):
    """
    Handles a Discord Message
    :param message: The Discord message
    """

    # Firstly, get the settings from the database
    server_settings = data.get_settings(message.guild.id)

    # Filter the message if we don't care about it
    if not filter_message(message, server_settings):
        return

    # Check if the message was a command or a normal message and process it accordingly
    if is_command(message, server_settings.prefix):
        await handle_command(message, server_settings)
    else:
        await handle_candy(message, server_settings)


def filter_message(message, server_settings):
    """
    Filters out messages
    :param message: The Discord message
    :param server_settings: The server settings
    """

    # Ignore any messages from bots
    if message.author.bot:
        return False

    # Ignore any messages in channels that CandyBot isn't set up for
    # If no channels are set up, allow every channel
    if server_settings.channels and message.channel.id not in server_settings.channels:
        return False

    # This message should be processed
    return True


def is_command(message, prefix):
    """
    Returns if the message was a CandyBot command by checking if there was
    content (if not, probably an image upload) and then the prefix
    :param message: The Discord message
    :param prefix: The set message prefix
    :return: True if the message was a CandyBot command
    """
    return message.content and message.content[0] == prefix


async def handle_command(message, server_settings):
    command, args = commands.parse_command(message.content[1:], True)
    # Check if the message was resolved to a command
    if command:
        command = command(server_settings, message, args)
        await command.run()
    # If not, might be a candy command
    elif len(args) == 1 and STATE.get(message.channel.id):
        command = commands.PickCommand(server_settings, message, invocation=args[0])
        await command.run()


async def handle_candy(message, server_settings):
    # The state is checked twice
    # Once to reduce database calls if there is candy proc'd (not async safe)
    # And once in proc (async safe)
    state = STATE.get(message.channel.id)
    if not state:
        if utils.roll(server_settings.chance):
            weights = [x.chance for x in server_settings.candy]
            candy_setting = utils.get_choice(server_settings.candy, weights)
            await proc(server_settings, message.channel, candy_setting, False)


async def proc(server_settings, channel, candy_setting, force):
    command = commands.PickCommand(server_settings, invocation=candy_setting.command)
    value = utils.get_value(server_settings.min, server_settings.max)
    candy_value = CandyValue(candy_setting.candy, value)
    candy_drop = CandyDrop(command, candy_setting.text, candy_value)
    # Need to obtain the lock to avoid multiple messages from proccing
    async with STATE_LOCK:
        if force or STATE.get(channel.id) is None:
            # This message will proc a candy drop
            # Must set the state inside the lock to avoid other messages from proccing
            STATE[channel.id] = candy_drop
        else:
            # An earlier message was chosen to be processed
            return
    # Code here will be run after the lock is released and should handle any additional processing
    stats = data.get_stats(channel.guild.id)
    stats.candy_dropped += candy_value
    data.set_stats(channel.guild.id, stats)
    candy_drop.message = await channel.send(candy_drop.drop_str)
