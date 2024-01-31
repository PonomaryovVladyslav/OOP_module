""" Constants and settings used in the project """
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

MODE_NORMAL = 'Normal'
MODE_HARD = 'Hard'
MODES = {'1': MODE_NORMAL,
         '2': MODE_HARD}
PLAYER_LIVES = 2
POINTS_FOR_FIGHT = 1
POINTS_FOR_KILLING = 5
MAX_RECORDS_NUMBER = 5
HARD_MODE_MULTIPLIER = 2
SCORE_FILE = 'scores.txt'
SCORE_TEST_FILE = 'scores_test.txt'
TEST_FILE_PATH = f'{ROOT_DIR}/{SCORE_TEST_FILE}'
NEW_TEST_FILE_PATH = f'{ROOT_DIR}/new_test_file.txt'
WRONG_TEST_FILE_PATH = f'{ROOT_DIR}/wrong_file.txt'
NAME_ADDITIONAL_SPACES = 4
PAPER = 'Paper'
STONE = 'Stone'
SCISSORS = 'Scissors'
WIN = 1
DRAW = 0
LOSE = -1
MAIN_MENU_OPTIONS = {"1": "Play", "2": "Score", "3": "Exit"}
ALLOWED_ATTACKS = {'1': PAPER,
                   '2': STONE,
                   '3': SCISSORS,
                   '0': 'Exit Game'}
ATTACK_PAIRS_OUTCOME = {(PAPER, PAPER): DRAW,
                        (PAPER, STONE): WIN,
                        (PAPER, SCISSORS): LOSE,
                        (STONE, PAPER): LOSE,
                        (STONE, STONE): DRAW,
                        (STONE, SCISSORS): WIN,
                        (SCISSORS, PAPER): WIN,
                        (SCISSORS, STONE): LOSE,
                        (SCISSORS, SCISSORS): DRAW}
INPUT_ASSETS_PATH = 'assets/input/'
ASSETS_FORMAT = '.json'
INPUT_BASIC_TEXT = 'Please select an option from the list:\n'
BASIC_OPTION_TEXTS = {
    'main_menu': '----Main Menu----',
    'attacks': '----Attack----',
    'mode': '----Mode----'
}
