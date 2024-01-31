import unittest
from contextlib import nullcontext as does_not_raise

from settings import MODE_NORMAL, MODE_HARD, MODES, ALLOWED_ATTACKS, MAIN_MENU_OPTIONS
from source.exceptions import WhiteSpaceInputError, EmptyInputError, IncorrectModeError, IncorrectLevelError, \
    IncorrectFightResult
from source.validations import validate_mode, validate_name, validate_fight_result, validate_level, is_valid_input_mode, \
    is_valid_input_menu, is_valid_input_attack, get_allowed_options, validated_score_row_size


class TestValidateName(unittest.TestCase):
    def test_validate_name_valid(self):
        with does_not_raise():
            validate_name('name')

    def test_validate_name_invalid_empty(self):
        with self.assertRaises(EmptyInputError):
            validate_name('')

    def test_validate_name_invalid_space(self):
        with self.assertRaises(WhiteSpaceInputError):
            validate_name('bla bla')


class TestValidateMode(unittest.TestCase):
    def test_validate_mode_valid_normal(self):
        with does_not_raise():
            validate_mode(MODE_NORMAL)

    def test_validate_mode_valid_hard(self):
        with does_not_raise():
            validate_mode(MODE_HARD)

    def test_validate_mode_invalid(self):
        with self.assertRaises(IncorrectModeError):
            validate_mode('wrong')


class TestValidateLevel(unittest.TestCase):
    def test_validate_level_valid(self):
        with does_not_raise():
            validate_level(4)

    def test_validate_level_invalid_negative(self):
        with self.assertRaises(IncorrectLevelError):
            validate_level(-5)

    def test_validate_level_invalid_str(self):
        with self.assertRaises(IncorrectLevelError):
            validate_level('text')

    def test_validate_level_invalid_num(self):
        with self.assertRaises(IncorrectLevelError):
            validate_level('4')


class TestValidateFightResult(unittest.TestCase):
    def test_validate_incorrect(self):
        with self.assertRaises(IncorrectFightResult):
            validate_fight_result(2)

    def test_validate_1(self):
        with does_not_raise():
            validate_fight_result(1)

    def test_validate_0(self):
        with does_not_raise():
            validate_fight_result(0)

    def test_validate_negative_1(self):
        with does_not_raise():
            validate_fight_result(-1)


class TestGetAllowedOptions(unittest.TestCase):
    def test_get_allowed_options_mode(self):
        self.assertEqual(get_allowed_options(MODES), ('1', '2'))

    def test_get_allowed_options_attack(self):
        self.assertEqual(get_allowed_options(ALLOWED_ATTACKS), ('1', '2', '3', '0'))

    def test_get_allowed_options_menu(self):
        self.assertEqual(get_allowed_options(MAIN_MENU_OPTIONS), ('1', '2', '3'))


class TestIsValidInputMode(unittest.TestCase):

    def test_invalid(self):
        self.assertFalse(is_valid_input_mode('5'))

    def test_valid_1(self):
        self.assertTrue(is_valid_input_mode('1'))

    def test_valid_2(self):
        self.assertTrue(is_valid_input_mode('2'))


class TestIsValidInputMenu(unittest.TestCase):

    def test_invalid(self):
        self.assertFalse(is_valid_input_menu('5'))

    def test_valid_1(self):
        self.assertTrue(is_valid_input_menu('1'))

    def test_valid_2(self):
        self.assertTrue(is_valid_input_menu('2'))

    def test_valid_3(self):
        self.assertTrue(is_valid_input_menu('3'))

    def test_invalid_0(self):
        self.assertFalse(is_valid_input_menu('0'))


class TestIsValidInputAttack(unittest.TestCase):

    def test_invalid(self):
        self.assertFalse(is_valid_input_attack('5'))

    def test_valid_1(self):
        self.assertTrue(is_valid_input_attack('1'))

    def test_valid_2(self):
        self.assertTrue(is_valid_input_attack('2'))

    def test_valid_3(self):
        self.assertTrue(is_valid_input_attack('3'))

    def test_valid_0(self):
        self.assertTrue(is_valid_input_attack('0'))


class TestValidatedTitleSize(unittest.TestCase):
    def test_invalid_small_num(self):
        size = validated_score_row_size(2)
        self.assertEqual(size, len("NAME") + 1)

    def test_invalid_str(self):
        size = validated_score_row_size("wrong")
        self.assertEqual(size, len("NAME") + 1)

    def test_valid(self):
        size = validated_score_row_size(10)
        self.assertEqual(size, 10)
