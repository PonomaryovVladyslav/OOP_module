from source.exceptions import WhiteSpaceInputError, EmptyInputError
from settings import MODES, ALLOWED_ATTACKS


def validate_name(name: str) -> None:
    """
    Validates user input name
    :param name: - name to validate
    """
    if ' ' in name:
        raise WhiteSpaceInputError
    elif not name:
        raise EmptyInputError


def get_allowed_options(options_dict: dict) -> tuple:
    """
    To get allowed options from dictionary from settings
    :param options_dict: dict from settings
    :return: tuple of keys of allowed options
    """
    return tuple(options_dict.keys())


def is_valid_input_mode(mode_input: str) -> bool:
    """
    Validates mode input
    :param mode_input: - mode of the game
    :return: True if mode in allowed modes, False otherwise
    """
    return mode_input in get_allowed_options(MODES)


def is_valid_menu_input(menu_input: str) -> bool:
    """
    Validates menu user input
    :param menu_input: - menu user input
    :return: True if menu in allowed modes, False otherwise
    """
    return menu_input in get_allowed_options(ALLOWED_ATTACKS)


def is_valid_input_attack(attack_input: str) -> bool:
    """
    Validates attack input
    :param attack_input: - attack user input
    :return: True if attack_input in allowed attacks, False otherwise
    """
    return attack_input in get_allowed_options(ALLOWED_ATTACKS)
