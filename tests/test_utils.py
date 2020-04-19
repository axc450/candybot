from unittest import TestCase

from candybot import utils
from candybot.engine import CandySettings, Candy


class Utils(TestCase):

    def test_chance_value_to_percent(self):
        candy_settings_1 = CandySettings(Candy("EMOJI_1", "NAME_1"), chance=2)
        candy_settings_2 = CandySettings(Candy("EMOJI_2", "NAME_3"), chance=3)
        candy_settings_3 = CandySettings(Candy("EMOJI_3", "NAME_3"), chance=5)
        test_input = [candy_settings_1, candy_settings_2, candy_settings_3]
        expected = [(candy_settings_1.candy, 20), (candy_settings_2.candy, 30), (candy_settings_3.candy, 50)]
        self.assertEqual(utils.chance_value_to_percent(test_input), expected)

    def test_chance_value_to_percent_specific_candy(self):
        candy_settings_1 = CandySettings(Candy("EMOJI_1", "NAME_1"), chance=2)
        candy_settings_2 = CandySettings(Candy("EMOJI_2", "NAME_3"), chance=3)
        candy_settings_3 = CandySettings(Candy("EMOJI_3", "NAME_3"), chance=5)
        test_input = [candy_settings_1, candy_settings_2, candy_settings_3]
        expected = 30
        self.assertEqual(utils.chance_value_to_percent(test_input, candy=candy_settings_2.candy), expected)

    def test_chance_value_to_percent_all_zero(self):
        candy_settings_1 = CandySettings(Candy("EMOJI_1", "NAME_1"), chance=0)
        candy_settings_2 = CandySettings(Candy("EMOJI_2", "NAME_3"), chance=0)
        candy_settings_3 = CandySettings(Candy("EMOJI_3", "NAME_3"), chance=0)
        test_input = [candy_settings_1, candy_settings_2, candy_settings_3]
        expected = [(candy_settings_1.candy, 0), (candy_settings_2.candy, 0), (candy_settings_3.candy, 0)]
        self.assertEqual(utils.chance_value_to_percent(test_input), expected)

    def test_chance_value_to_percent_empty(self):
        test_input = []
        expected = []
        self.assertEqual(utils.chance_value_to_percent(test_input), expected)
