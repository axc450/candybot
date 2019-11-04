import asyncio
from unittest import TestCase
from unittest.mock import Mock
from candybot.commands.framework import parse_command, parse_args, ArgumentSpec
from candybot.commands.candy import CandyCommand
from candybot.commands.lb import LeaderboardCommand
from candybot.commands.settings.max import MaxCommand
from candybot.commands.settings.chance import ChanceCommand
from candybot.commands.settings.candy.add import AddCandyCommand
from candybot.commands.framework import SettingsCommand
from candybot.commands.framework import CandySettingsCommand


def resolve(c):
    return asyncio.get_event_loop().run_until_complete(c)


class Commands(TestCase):

    def test_basic(self):
        self.assertEqual(parse_command("candy", False), (CandyCommand, []))
        self.assertEqual(parse_command("settings", False), (SettingsCommand, []))
        self.assertEqual(parse_command("settings max", False), (MaxCommand, []))
        self.assertEqual(parse_command("settings candy", False), (CandySettingsCommand, []))
        self.assertEqual(parse_command("settings candy add", False), (AddCandyCommand, []))
        self.assertEqual(parse_command("abc", False), (None, ["abc"]))

    def test_short(self):
        self.assertEqual(parse_command("max", False), (MaxCommand, []))
        self.assertEqual(parse_command("chance", False), (ChanceCommand, []))

    def test_alias(self):
        self.assertEqual(parse_command("leaderboard", False), (LeaderboardCommand, []))
        self.assertEqual(parse_command("addcandy", False), (AddCandyCommand, []))

    def test_args(self):
        self.assertEqual(parse_command("candy a b c", False), (CandyCommand, ["a", "b", "c"]))
        self.assertEqual(parse_command("settings candy add a b c", False), (AddCandyCommand, ["a", "b", "c"]))

    def test_leaf_only(self):
        self.assertEqual(parse_command("candy", True), (CandyCommand, []))
        self.assertEqual(parse_command("settings", True), (None, ["settings"]))
        self.assertEqual(parse_command("settings candy add", True), (AddCandyCommand, []))
        self.assertEqual(parse_command("settings candy a", True), (None, ["settings", "candy", "a"]))

    def test_ignore(self):
        self.assertEqual(parse_command("pick a b c", False), (None, ["pick", "a", "b", "c"]))


class Args(TestCase):

    @staticmethod
    def mock_argument(name, ignore_spaces):
        mock = Mock()
        mock.name = f"name_{name}"
        mock.ignore_spaces = ignore_spaces
        mock.parse.return_value = asyncio.Future()
        mock.parse.return_value.set_result(f"parsed_{name}")
        return mock

    def test_basic(self):
        argument_a = self.mock_argument("a", False)
        argument_b = self.mock_argument("b", False)
        argument_c = self.mock_argument("c", False)
        spec = ArgumentSpec([argument_a, argument_b, argument_c], False)

        args = ["a", "b", "c"]
        result = parse_args(args, spec, "server")
        self.assertEqual(resolve(result), {"name_a": "parsed_a", "name_b": "parsed_b", "name_c": "parsed_c"})

        args = ["a", "b"]
        result = parse_args(args, spec, "server")
        self.assertRaises(IndexError, resolve, result)

        args = ["a", "b", "c", "d"]
        result = parse_args(args, spec, "server")
        self.assertRaises(IndexError, resolve, result)

    def test_empty(self):
        spec = ArgumentSpec([], False)

        args = []
        result = parse_args(args, spec, "server")
        self.assertEqual(resolve(result), {})

    def test_optional(self):
        argument_a = self.mock_argument("a", False)
        argument_b = self.mock_argument("b", False)
        argument_c = self.mock_argument("c", False)
        spec = ArgumentSpec([argument_a, argument_b, argument_c], True)

        args = ["a", "b", "c"]
        result = parse_args(args, spec, "server")
        self.assertEqual(resolve(result), {"name_a": "parsed_a", "name_b": "parsed_b", "name_c": "parsed_c"})

        args = ["a", "b"]
        result = parse_args(args, spec, "server")
        self.assertEqual(resolve(result), {"name_a": "parsed_a", "name_b": "parsed_b"})

    def test_ignore_spaces(self):
        argument_a = self.mock_argument("a", False)
        argument_b = self.mock_argument("b", False)
        argument_c = self.mock_argument("c", True)
        spec = ArgumentSpec([argument_a, argument_b, argument_c], False)

        args = ["a", "b", "c", "d"]
        result = parse_args(args, spec, "server")
        self.assertEqual(resolve(result), {"name_a": "parsed_a", "name_b": "parsed_b", "name_c": "parsed_c"})
        argument_c.parse.assert_called_once_with("c d", "server")
