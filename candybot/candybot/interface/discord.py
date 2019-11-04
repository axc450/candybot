import discord


async def send_embed(channel, text=None, title=None, color=None, author=None, fields=[]):
    color = color if color else author.color
    embed = discord.Embed(description=text, title=title, color=color)
    if author:
        embed.set_author(name=author.name, icon_url=author.avatar_url)
    for field in fields:
        embed.add_field(name=f"-- {field[0].capitalize()} --", value=field[1], inline=field[2])
    await channel.send(embed=embed)


def get_user(server, user_id):
    return server.get_member(user_id)


def get_role(server, role_id):
    return server.get_role(role_id)


def get_channel(server, channel_id):
    return server.get_channel(channel_id)


async def apply_role(user, role):
    await user.add_roles(role, reason="CandyBot")
