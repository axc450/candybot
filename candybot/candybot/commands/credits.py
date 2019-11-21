from candybot.interface import database
from candybot.commands.framework import Command, ArgumentSpec


class CreditsCommand(Command):
    name = "credits"
    help = "Shows CandyBot credits."
    aliases = []
    examples = [""]
    argument_spec = ArgumentSpec([], False)
    clean = False
    admin = False
    ignore = False

    title = ":heart: CandyBot Credits"
    donate_link = "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4MA3ZWKYSYNB6"
    add_link = "https://discordapp.com/api/oauth2/authorize?client_id=409047597572030484&permissions=8224&scope=bot"
    github = "https://github.com/axc450/CandyBot"

    async def _run(self):
        donators = database.get_donators()
        donators_list_1 = "\n".join(donators[:len(donators)//2])
        donators_list_2 = "\n".join(donators[len(donators)//2:])
        credits_str = ":candy: CandyBot Created By **Super#0010**\n" \
                      f":computer: [Add CandyBot to your server!]({self.add_link}) | [Github]({self.github})\n" \
                      f":moneybag: Please consider donating [here]({self.donate_link}) to support CandyBot!"
        await self.send(credits_str, fields=[("Donators", donators_list_2, True), ("Donators", donators_list_1, True)])

