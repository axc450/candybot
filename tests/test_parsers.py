from asynctest import TestCase, CoroutineMock
from unittest.mock import Mock, MagicMock, patch
from candybot.commands.framework import parse_command, parse_args


class Commands(TestCase):

    @staticmethod
    def mock_command(name, aliases=[], ignore=False, subcommands=[]):
        mock = Mock(aliases=aliases, ignore=ignore, subcommands=subcommands)
        mock.name = name
        return mock

    def setUp(self):
        # Build command tree similar to the real one
        self.c = self.mock_command("c")
        self.d = self.mock_command("d", aliases=["D"])
        self.e = self.mock_command("e", ignore=True)
        self.f = self.mock_command("f")
        self.g = self.mock_command("g", subcommands=[self.mock_command("f")])
        self.b = self.mock_command("b", subcommands=[self.f, self.g])
        self.a = self.mock_command("a", ignore=True, subcommands=[self.b, self.c, self.d, self.e])

        # Patch the real one with the one we just built
        p = patch("candybot.commands.framework.parsers.commands.Command", self.a)
        p.start()
        self.addCleanup(p.stop)

    def test_basic(self):
        self.assertEqual(parse_command("c", False), (self.c, []))
        self.assertEqual(parse_command("b", False), (self.b, []))
        self.assertEqual(parse_command("b f", False), (self.f, []))
        self.assertEqual(parse_command("x", False), (None, ["x"]))

    def test_short(self):
        self.assertEqual(parse_command("f", False), (self.f, []))

    def test_alias(self):
        self.assertEqual(parse_command("D", False), (self.d, []))

    def test_args(self):
        self.assertEqual(parse_command("c 1 2 3", False), (self.c, ["1", "2", "3"]))
        self.assertEqual(parse_command("b f 1 2 3", False), (self.f, ["1", "2", "3"]))

    def test_leaf_only(self):
        self.assertEqual(parse_command("c", True), (self.c, []))
        self.assertEqual(parse_command("b", True), (None, ["b"]))
        self.assertEqual(parse_command("b f", True), (self.f, []))
        self.assertEqual(parse_command("b g 1", True), (None, ["b", "g", "1"]))

    def test_ignore(self):
        self.assertEqual(parse_command("e 1 2 3", False), (None, ["e", "1", "2", "3"]))


class Args(TestCase):

    @staticmethod
    def mock_argument(ignore_spaces=False):
        return Mock(parse=CoroutineMock(), ignore_spaces=ignore_spaces)

    @staticmethod
    def mock_spec(args=[], optional=False):
        spec = MagicMock(optional=optional, args=args)
        spec.__iter__.return_value = spec.args
        spec.__len__.return_value = len(spec.args)
        return spec

    async def test_basic(self):
        spec = self.mock_spec([self.mock_argument(), self.mock_argument(), self.mock_argument()])
        args = ["a", "b", "c"]
        expected = {spec.args[0].name: spec.args[0].parse.return_value,
                    spec.args[1].name: spec.args[1].parse.return_value,
                    spec.args[2].name: spec.args[2].parse.return_value}
        result = await parse_args(args, spec, "server")
        self.assertEqual(result, expected)

    async def test_incorrect_number_of_args(self):
        spec = self.mock_spec([self.mock_argument(), self.mock_argument(), self.mock_argument()])
        for args in [["a", "b"], ["a", "b", "c", "d"], []]:
            with self.subTest(args=args):
                await self.assertAsyncRaises(IndexError, parse_args(args, spec, "server"))

    async def test_no_args(self):
        spec = self.mock_spec()
        spec.args = []
        result = await parse_args([], spec, "server")
        self.assertEqual(result, {})

    async def test_optional_last_arg(self):
        spec = self.mock_spec([self.mock_argument(), self.mock_argument(), self.mock_argument()], True)

        args = ["a", "b", "c"]
        expected = {spec.args[0].name: spec.args[0].parse.return_value,
                    spec.args[1].name: spec.args[1].parse.return_value,
                    spec.args[2].name: spec.args[2].parse.return_value}
        result = await parse_args(args, spec, "server")
        self.assertEqual(result, expected)

        args = ["a", "b"]
        expected = {spec.args[0].name: spec.args[0].parse.return_value,
                    spec.args[1].name: spec.args[1].parse.return_value}
        result = await parse_args(args, spec, "server")
        self.assertEqual(result, expected)

    async def test_ignore_spaces(self):
        spec = self.mock_spec([self.mock_argument(), self.mock_argument(), self.mock_argument(True)], True)

        args = ["a", "b", "c", "d"]
        expected = {spec.args[0].name: spec.args[0].parse.return_value,
                    spec.args[1].name: spec.args[1].parse.return_value,
                    spec.args[2].name: spec.args[2].parse.return_value}
        result = await parse_args(args, spec, "server")
        self.assertEqual(result, expected)
        spec.args[2].parse.assert_called_once_with("c d", "server")
