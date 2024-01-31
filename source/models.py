""" module contains Enemy Class and Player Class"""

from random import randint

from source.exceptions import GameOver, EnemyDown, QuitApp, WhiteSpaceInputError, EmptyInputError
from source.input_generator import InputGenerator
from source.validations import is_valid_input_attack, validate_name
from settings import (
    ALLOWED_ATTACKS,
    MODE_NORMAL,
    PLAYER_LIVES,
    POINTS_FOR_FIGHT,
    POINTS_FOR_KILLING,
    HARD_MODE_MULTIPLIER,
    ATTACK_PAIRS_OUTCOME
)


class Enemy:
    """
    Class represents the enemy bot player
    """
    lives: int
    level: int

    def __init__(self, mode: str, level: int):
        """
        Initializes the enemy instance
        """
        self.level = level
        self.lives = self.level if mode == MODE_NORMAL else self.level * HARD_MODE_MULTIPLIER

    @staticmethod
    def attack() -> str:
        """
        Randomly returns one of possible enemy's attack
        """
        return ALLOWED_ATTACKS[str(randint(1, 3))]

    def on_lose_fight(self) -> None:
        """
        Decrease enemy's lives
        """
        self.lives -= 1
        if self.lives == 0:
            raise EnemyDown


class Player:
    """
    Class describes user's player
    """
    name: str
    score: int = 0

    def __init__(self):
        """
        Initializes the player instance
        """
        self.input_name()
        self.lives = PLAYER_LIVES

    def input_name(self) -> None:
        """
        Input and return player name
        """
        while True:
            name = input("Enter your name: ")
            try:
                validate_name(name)
                self.name = name
                break
            except WhiteSpaceInputError:
                print("Whitespaces are not allowed in the name.")
            except EmptyInputError:
                print('Name cannot be empty.')

    @staticmethod
    def attack() -> str:
        """
        Asks for user attack input
        """
        while True:
            attack_input = input(InputGenerator('attacks').text)
            if is_valid_input_attack(attack_input):
                if attack_input == '0':
                    raise QuitApp
                return ALLOWED_ATTACKS[attack_input]
            print('Incorrect input.')

    def on_lose_fight(self) -> None:
        """
        Decreases player's lives
        """
        self.lives -= 1
        if self.lives == 0:
            raise GameOver

    def on_win_fight(self, mode) -> None:
        """
        Adds score in case successful fight
        """
        self.score += POINTS_FOR_FIGHT if mode == MODE_NORMAL else POINTS_FOR_FIGHT * HARD_MODE_MULTIPLIER

    def on_enemy_down(self, mode):
        """
        Adds score on enemy down
        """
        print("Congratulation! Enemy down.")
        self.score += POINTS_FOR_KILLING if mode == MODE_NORMAL else POINTS_FOR_KILLING * HARD_MODE_MULTIPLIER


class Battle:
    """
    Battle class with methods to fight
    """
    player: Player
    enemy: Enemy
    mode: str

    def __init__(self, player: Player, enemy: Enemy, mode: str) -> None:
        """
        Initializes battle
        """
        self.player = player
        self.enemy = enemy
        self.mode = mode

    def fight(self) -> None:
        """
        Resolves player's attack vs enemy's attack
        """
        enemy_attack = self.enemy.attack()
        player_attack = self.player.attack()
        print(f"Your attack: {player_attack}.  Enemy's attack: {enemy_attack}")
        fight_result = ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)]
        self.handle_fight_result(fight_result)

    def handle_fight_result(self, fight_result: int) -> None:
        """
        Handles results of the fight
        """
        if fight_result == 1:
            print('You attacked successfully!')
            self.player.on_win_fight(self.mode)
            self.enemy.on_lose_fight()
        elif fight_result == -1:
            print("You missed!")
            self.player.on_lose_fight()
        elif fight_result == 0:
            print("It's a draw!")
