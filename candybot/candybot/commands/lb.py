from candybot import data, converters
from candybot.engine import CandyValue
from candybot.commands.framework import Command, ArgumentSpec, CandyArgument


class LeaderboardCommand(Command):
    name = "lb"
    help = "Shows the CandyBot Leaderboard."
    aliases = ["leaderboard"]
    examples = ["", "🍎"]
    argument_spec = ArgumentSpec([CandyArgument], True)
    clean = False
    admin = False
    ignore = False

    title = ":checkered_flag: CandyBot Leaderboard"
    emojis = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten"]

    async def _run(self):
        candy = self.args[0]
        users = data.get_users(self.server.id)
        sorted_users = sorted(users, key=self._sorting_func, reverse=True)
        lines = await self._generate_lines(sorted_users, candy)
        await self.send("\n".join(lines))

    async def _generate_lines(self, sorted_users, candy):
        lines = []
        max_lines = len(self.emojis)
        for i, user in enumerate(sorted_users):
            # Break when we run out of emojis (ie. only show top 10)
            if i == max_lines:
                break
            # If the user didn't have any candy, exclude them from the leaderboard
            # The case where a user has candy but none of the given candy is checked later
            if not user.inv:
                continue
            # If the user couldn't be found, exclude them from the leaderboard
            u = await converters.to_user(str(user.id), self.message.guild)
            if u is None:
                continue
            # Add a leaderboard line
            if candy is None:
                # No given candy
                lines.append(f":{self.emojis[i]}: {u.mention} {user.inv.line_str}")
            else:
                # Specific candy given
                value = user.inv[candy]
                if value:
                    lines.append(f":{self.emojis[i]}: {u.mention} {CandyValue(candy, value).small_str}")
        return lines

    def _sorting_func(self, x):
        candy = self.args[0]
        return x.inv[candy] if candy else x.inv.total
