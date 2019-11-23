from asyncio.locks import Lock
from candybot import exceptions, utils, commands
from candybot.interface import database
from candybot.engine import CandyValue, CandyDrop

# The current state of channels
# Channel ID -> Candy Drop
STATE = {}

# Mutex lock for STATE
STATE_LOCK = Lock()


async def setup(guild):
    database.set_settings(guild, ".", 0.2, 3, 5, 10, 100)
    database.set_settings_candy_add(guild, "candy", "🍬", 1)


async def teardown(guild):
    database.teardown(guild)


async def handle_message(message):
    """
    Handles a Discord Message
    :param message: The Discord message
    """

    # Firstly, filter the message if we don't care about it
    if not filter_message(message):
        return

    # This message will be processed, so get the settings from the database
    server_settings = database.get_settings(message.guild.id)

    # Check if the message was a command or a normal message and process it accordingly
    if is_command(message, server_settings.prefix):
        await handle_command(message, server_settings)
    else:
        await handle_candy(message, server_settings)


def filter_message(message):
    """
    Filters out messages
    :param message: The Discord message
    """

    # Ignore any messages from bots
    if message.author.bot:
        return False

    # Ignore any messages in channels that CandyBot isn't set up for
    # If no channels are set up, allow every channel
    channels = database.get_channels(message.guild.id)
    if channels and message.channel.id not in channels:
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
            candy = get_random_candy(message.guild.id)
            await proc(server_settings, message.channel, candy, False)


def get_random_candy(server):
    candy = database.get_candy(server)
    if not candy:
        raise exceptions.CandyError(f"This server has not set up any Candy")
    weights = [x.chance for x in candy]
    return utils.get_choice(candy, weights)


async def proc(server_settings, channel, candy, force):
    command = commands.PickCommand(server_settings, invocation=candy.command)
    value = utils.get_value(server_settings.min, server_settings.max)
    candy_value = CandyValue(candy, value)
    candy_drop = CandyDrop(command, candy_value)
    async with STATE_LOCK:
        # Keep this critical section as small as possible
        if force or STATE.get(channel.id) is None:
            STATE[channel.id] = candy_drop
            database.set_stats_candy(channel.guild.id, candy_drop.candy_value)
            # TODO: Remove this from critical section?
            candy_drop.message = await channel.send(candy_drop.drop_str)
