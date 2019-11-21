from candybot.interface import database, converters
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
        invs = database.get_inv(self.message.guild.id)
        sorted_invs = sorted(invs.items(), key=self._sorting_func, reverse=True)
        lines = await self._generate_lines(sorted_invs, self.candy)
        await self.send("\n".join(lines))

    async def _generate_lines(self, sorted_invs, candy):
        lines = []
        for i, (user, inv) in enumerate(sorted_invs):
            # Break when we run out of emojis (ie. only show top 10)
            if i == len(self.emojis):
                break
            # If the user couldn't be found, exclude them from the leaderboard
            u = await converters.to_user(str(user), self.message.guild)
            if u is None:
                continue
            # Add a leaderboard line
            if candy is None:
                lines.append(f":{self.emojis[i]}: {u.mention} {inv.line_str}")
            else:
                v = inv[candy]
                if v:
                    v = f"{candy} x **{v:,}**"
                    lines.append(f":{self.emojis[i]}: {u.mention} {v}")
        return lines

    def _sorting_func(self, x):
        return x[1][self.candy] if self.candy else x[1].total
