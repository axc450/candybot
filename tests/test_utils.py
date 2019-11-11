from unittest import TestCase
from unittest.mock import Mock

from candybot import utils


class Utils(TestCase):

    def test_chance_value_to_percent(self):
        test_input = [Mock(chance=2), Mock(chance=3), Mock(chance=5)]
        expected = {test_input[0]: 20, test_input[1]: 30, test_input[2]: 50}
        self.assertEqual(utils.chance_value_to_percent(test_input), expected)

    def test_chance_value_to_percent_all_zero(self):
        test_input = [Mock(chance=0), Mock(chance=0), Mock(chance=0)]
        expected = {test_input[0]: 0, test_input[1]: 0, test_input[2]: 0}
        self.assertEqual(utils.chance_value_to_percent(test_input), expected)

    def test_chance_value_to_percent_empty(self):
        test_input = []
        expected = {}
        self.assertEqual(utils.chance_value_to_percent(test_input), expected)
