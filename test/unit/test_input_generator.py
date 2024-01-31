import unittest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from source.exceptions import IncorrectInputTypeError
from source.input_generator import InputGenerator


class TestInputGeneratorInitialization(unittest.TestCase):

    @patch('source.input_generator.InputGenerator.validate_type_of_input')
    def test_input_generator(self, mock_validate):
        with does_not_raise():
            InputGenerator("success")

    @patch('source.input_generator.InputGenerator.get_list_of_possible_types')
    def test_input_generator_init_with_mocked_get_list(self, mock_get_list_of_possible_types):
        mock_get_list_of_possible_types.return_value = ['valid1', 'valid2', 'valid3']
        with does_not_raise():
            InputGenerator("valid1")

    @patch('source.input_generator.InputGenerator.get_list_of_possible_types')
    def test_input_generator_init_with_mocked_get_list_failed(self, mock_get_list_of_possible_types):
        mock_get_list_of_possible_types.return_value = ['valid1', 'valid2', 'valid3']
        with self.assertRaises(IncorrectInputTypeError):
            InputGenerator("invalid")

    def test_input_generator_init_attacks(self):
        with does_not_raise():
            InputGenerator("attacks")

    def test_input_generator_init_main_menu(self):
        with does_not_raise():
            InputGenerator("main_menu")

    def test_input_generator_init_mode(self):
        with does_not_raise():
            InputGenerator("mode")

    def test_input_generator_init_incorrect(self):
        with self.assertRaises(IncorrectInputTypeError):
            InputGenerator("incorrect")


class InputGeneratorTexts(unittest.TestCase):

    def test_attacks(self):
        self.assertEqual(InputGenerator("attacks").text,
                         """Please select an option from the list:
----Attack----
1 - Paper
2 - Stone
3 - Scissors
0 - Exit Game
"""
                         )

    def test_main_menu(self):
        self.assertEqual(InputGenerator("main_menu").text,
                         """Please select an option from the list:
----Main Menu----
1 - Start new game
2 - Show scores
3 - Exit game
"""
                         )

    def test_mode(self):
        self.assertEqual(InputGenerator("mode").text,
                         """Please select an option from the list:
----Mode----
1 - Normal
2 - Hard
"""
                         )
