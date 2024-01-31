import json
import os

from source.exceptions import IncorrectInputTypeError
from settings import INPUT_ASSETS_PATH, ASSETS_FORMAT, INPUT_BASIC_TEXT, BASIC_OPTION_TEXTS


class InputGenerator:
    """
    Class to generate text for inputs
    """
    text: str

    def __init__(self, type_of_input: str) -> None:
        """
        Constructor for input generator
        :param type_of_input: main menu, mode or attack
        """
        try:
            validate_type_of_input(type_of_input)
            self.generate_text(type_of_input)
        except IncorrectInputTypeError:
            raise

    def generate_text(self, type_of_input: str) -> None:
        with open(INPUT_ASSETS_PATH + type_of_input + ASSETS_FORMAT) as asset:
            options = json.load(asset)
            final_text = INPUT_BASIC_TEXT
            final_text += f"{BASIC_OPTION_TEXTS[type_of_input]}\n"
            for option, text in options.items():
                final_text += f"{option} - {text}\n"
            self.text = final_text


def get_list_of_possible_types() -> list[str]:
    return [filename[:-5] for filename in os.listdir(INPUT_ASSETS_PATH)]


def validate_type_of_input(type_of_input: str) -> None:
    if type_of_input not in get_list_of_possible_types():
        raise IncorrectInputTypeError
