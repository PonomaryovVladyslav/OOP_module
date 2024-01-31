import json
import os

from settings import INPUT_ASSETS_PATH, ASSETS_FORMAT, INPUT_BASIC_TEXT, BASIC_OPTION_TEXTS, ROOT_DIR
from source.exceptions import IncorrectInputTypeError


class InputGenerator:
    """
    Class to generate text for inputs
    """
    type_of_input: str

    def __init__(self, type_of_input: str) -> None:
        """
        Constructor for input generator
        :param type_of_input: main menu, mode or attack
        """
        try:
            self.validate_type_of_input(type_of_input)
            self.type_of_input = type_of_input
        except IncorrectInputTypeError:
            raise

    @property
    def text(self) -> str:
        with open(f"{ROOT_DIR}/{INPUT_ASSETS_PATH}{self.type_of_input}{ASSETS_FORMAT}") as asset:
            options = json.load(asset)
            final_text = INPUT_BASIC_TEXT
            final_text += f"{BASIC_OPTION_TEXTS[self.type_of_input]}\n"
            for option, text in options.items():
                final_text += f"{option} - {text}\n"
            return final_text

    def validate_type_of_input(self, type_of_input: str) -> None:
        if type_of_input not in self.get_list_of_possible_types():
            raise IncorrectInputTypeError

    @staticmethod
    def get_list_of_possible_types() -> list[str]:
        return [filename[:-len(ASSETS_FORMAT)] for filename in os.listdir(f"{ROOT_DIR}/{INPUT_ASSETS_PATH}")]
