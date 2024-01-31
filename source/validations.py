from settings import MODES, ALLOWED_ATTACKS, ATTACK_PAIRS_OUTCOME, MAIN_MENU_OPTIONS
from source.exceptions import WhiteSpaceInputError, EmptyInputError, IncorrectModeError, IncorrectLevelError, \
    IncorrectFightResult


def validate_name(name: str) -> None:
    """
    Validates user input name
    :param name: - name to validate
    """
    if ' ' in name:
        raise WhiteSpaceInputError
    elif not name:
        raise EmptyInputError


def validate_mode(mode: str) -> None:
    """
    Validate mode
    :param mode: - mode to validate
    """
    if mode not in MODES.values():
        raise IncorrectModeError


def validate_level(level: int) -> None:
    """
    Validate mode
    :param level: - level to validate
    """
    try:
        if not isinstance(level, int) or level <= 0:
            raise IncorrectLevelError
    except ValueError:
        raise IncorrectLevelError


def validate_fight_result(result: int) -> None:
    """
    Validate result of battle
    :param result: should be one of [1, 0, -1]
    """
    if result not in set(ATTACK_PAIRS_OUTCOME.values()):
        raise IncorrectFightResult


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


def is_valid_input_menu(menu_input: str) -> bool:
    """
    Validates menu user input
    :param menu_input: - menu user input
    :return: True if menu in allowed modes, False otherwise
    """
    return menu_input in get_allowed_options(MAIN_MENU_OPTIONS)


def is_valid_input_attack(attack_input: str) -> bool:
    """
    Validates attack input
    :param attack_input: - attack user input
    :return: True if attack_input in allowed attacks, False otherwise
    """
    return attack_input in get_allowed_options(ALLOWED_ATTACKS)


def validated_score_row_size(row_size: int) -> int:
    """
    Validates the title for score file

    :param row_size: - number of symbols to NAME field
    :return: - number of symbols to write
    """
    if not isinstance(row_size, int) or row_size <= len("NAME"):
        return len("NAME") + 1
    else:
        return row_size
