""" This file is the entry file. Run it to start."""
from source.input_generator import InputGenerator
from settings import MODES, SCORE_FILE
from source.exceptions import GameOver, EnemyDown, QuitApp, RecordInRecordsError
from source.models import Player, Enemy, Battle
from source.record import GameRecord
from source.validations import is_valid_input_mode, is_valid_menu_input

__version__ = '1'


class Game:
    """
    The game class to start game
    """
    _level: int = 0
    mode: str
    player: Player
    enemy: Enemy

    def __init__(self):
        """
        Initialize the game
        """
        self.player = Player()
        self.input_mode()

    def input_mode(self) -> None:
        """
        Input and return game mode
        """
        while True:
            mode_input = input(InputGenerator('mode').text)
            if is_valid_input_mode(mode_input):
                self.mode = MODES[mode_input]
                break
            print('Incorrect input.')

    def new_enemy(self) -> None:
        """
        Create new enemy with new level
        """
        self._level += 1
        self.enemy = Enemy(mode=self.mode, level=self._level)

    def print_status(self) -> None:
        """
        Prints the current game status to console
        """
        print(f"\nPlayer: {self.player.name}."
              f"\tMode: {self.mode}."
              f"\tPlayer Lives: {self.player.lives}."
              f"\tScore: {self.player.score}."
              f"\tLevel: {self.enemy.level}"
              f"\tEnemy's lives: {self.enemy.lives}")

    def save_score(self) -> None:
        """
        Saves score to board file
        """
        game_record = GameRecord(self.mode)
        try:
            game_record.add_record(self.player)
            game_record.save_to_file()
        except RecordInRecordsError:
            print('Record is already in list')

    def start_game(self) -> None:
        """
        Start game method
        """
        self.new_enemy()
        try:
            while True:
                self.print_status()
                battle = Battle(self.player, self.enemy, self.mode)
                try:
                    battle.fight()
                except EnemyDown:
                    self.player.on_enemy_down(self.mode)
                    self.new_enemy()
                    print("\nNew enemy comes.")
        except GameOver:
            print('You lose!')
            self.save_score()
        finally:
            self.print_status()


def play() -> None:
    """
    Runs the main game
    """
    game = Game()
    game.start_game()


def print_score() -> None:
    """
    Reads score from file and prints it
    """
    with open(SCORE_FILE) as file:
        print(file.read())


def main_menu_input() -> str:
    """
    Menu user input
    """
    while True:

        menu_choice = input(InputGenerator('main_menu').text)
        if is_valid_menu_input(menu_choice):
            return menu_choice
        print('Incorrect input.')


def main_menu() -> None:
    """
    Displays the main menu of the game
    """
    menu_choice = main_menu_input()
    if menu_choice == '1':
        play()
    elif menu_choice == '2':
        print_score()
        main_menu()
    elif menu_choice == '3':
        raise QuitApp


def main():
    """
    Main game loop
    """
    try:
        main_menu()
    except QuitApp:
        print('Good buy!')
    except KeyboardInterrupt:
        print('Good buy!')
