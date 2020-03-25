from asynctest import TestCase, patch, Mock, MagicMock, CoroutineMock
from discord import Message, Guild, TextChannel, Member
from candybot.commands.pick import PickCommand
from candybot.engine import CandyDrop, CandyValue, CandyCollection, Candy, Settings
from candybot.interface import database


class CommandTestCase(TestCase):

    def patch(self, target, new):
        p = patch(target, new)
        p.start()
        self.addCleanup(p.stop)


@patch("candybot.engine.STATE_LOCK", MagicMock())
@patch("candybot.commands.Command.server", Mock(spec=Guild, id="A"))
@patch("candybot.commands.Command.author", Mock(spec=Member, id="A"))
@patch("candybot.commands.Command.channel", Mock(spec=TextChannel, id="A"))
class Pick(CommandTestCase):

    def setup(self, state="A", inv=0):
        mock_command = Mock(spec=PickCommand, invocation="A")
        mock_message = Mock(spec=Message)
        mock_candy_value = Mock(spec=CandyValue, candy=Mock(spec=Candy), value=10)
        self.mock_candy_drop = Mock(spec=CandyDrop, candy_value=mock_candy_value, command=mock_command, message=mock_message)
        self.mock_state = {state: self.mock_candy_drop}
        self.patch("candybot.engine.STATE", self.mock_state)
        mock_get_inv = Mock(spec=database.get_inv, return_value={"A": Mock(spec=CandyCollection, __getitem__=Mock(return_value=inv))})
        self.mock_database = Mock(spec=database, get_inv=mock_get_inv)
        self.patch("candybot.commands.pick.database", self.mock_database)
        self.mock_send = CoroutineMock()
        self.patch("candybot.commands.Command.send", self.mock_send)

    def assert_action(self, expected_candy):
        self.assertFalse(self.mock_state)
        self.mock_candy_drop.message.delete.assert_called_once_with()
        self.mock_database.set_inv.assert_called_once_with("A", "A", self.mock_candy_drop.candy_value, update=True)
        self.mock_send.assert_called_once_with(self.mock_candy_drop.pick_str)
        self.assertEqual(self.mock_candy_drop.candy_value.value, expected_candy)

    def assert_no_action(self):
        self.assertTrue(self.mock_state)
        self.mock_candy_drop.message.delete.assert_not_called()
        self.mock_database.set_inv.assert_not_called()
        self.mock_send.assert_not_called()

    def test_invocation_default(self):
        command = PickCommand(None)
        self.assertEqual(command.invocation, "pick")

    def test_invocation_set(self):
        command = PickCommand(None, invocation="A")
        self.assertEqual(command.invocation, "A")

    async def test_ignore_if_no_state(self):
        self.setup(state="B")
        command = PickCommand(None, invocation="A")
        await command._run()
        self.assert_no_action()

    async def test_ignore_if_invocations_differ(self):
        self.setup()
        command = PickCommand(None, invocation="B")
        await command._run()
        self.assert_no_action()

    async def test_ignore_if_at_cap(self):
        self.setup(inv=20)
        command = PickCommand(Mock(spec=Settings, cap=20), invocation="A")
        await command._run()
        self.assert_no_action()

    async def test_successful_full_pick(self):
        self.setup()
        command = PickCommand(Mock(spec=Settings, cap=20), invocation="A")
        await command._run()
        self.assert_action(10)

    async def test_successful_partial_pick(self):
        self.setup(inv=15)
        command = PickCommand(Mock(spec=Settings, cap=20), invocation="A")
        await command._run()
        self.assert_action(5)

