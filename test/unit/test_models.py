import unittest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from settings import PLAYER_LIVES, ATTACK_PAIRS_OUTCOME, PAPER, STONE, SCISSORS, WIN, LOSE, DRAW
from source.exceptions import IncorrectLevelError, IncorrectModeError, EnemyDown, GameOver, IncorrectFightResult
from source.models import Enemy, Player, QuitApp, Battle


class TestEnemyCreation(unittest.TestCase):
    def test_enemy_creation_incorrect_mode(self):
        with self.assertRaises(IncorrectModeError):
            Enemy(mode='wrong', level=1)

    def test_enemy_creation_incorrect_level_str(self):
        with self.assertRaises(IncorrectLevelError):
            Enemy(mode='Normal', level='wrong')

    def test_enemy_creation_incorrect_level_minus(self):
        with self.assertRaises(IncorrectLevelError):
            Enemy(mode='Normal', level=-4)

    def test_enemy_creation_incorrect_level_and_mode(self):
        with self.assertRaises(IncorrectModeError):
            Enemy(mode='wrong', level=-4)


class TestEnemyDecreaseLives(unittest.TestCase):

    def test_enemy_not_died(self):
        enemy = Enemy(mode='Normal', level=3)
        with does_not_raise():
            enemy.on_lose_fight()

    def test_enemy_died(self):
        enemy = Enemy(mode='Normal', level=3)
        with self.assertRaises(EnemyDown):
            enemy.on_lose_fight()
            enemy.on_lose_fight()
            enemy.on_lose_fight()


class TestPlayerCreation(unittest.TestCase):
    @patch('builtins.input')
    def test_player_creation(self, mock_input):
        mock_input.return_value = 'Vlad'
        with does_not_raise():
            player = Player()
        self.assertEqual(player.name, 'Vlad')

    @patch('builtins.input')
    def test_player_creation_empty_name(self, mock_input):
        mock_input.side_effect = ['', 'Vlad']
        with does_not_raise():
            player = Player()
        self.assertEqual(player.name, 'Vlad')
        self.assertEqual(mock_input.call_count, 2)

    @patch('builtins.input')
    def test_player_creation_space_in_name(self, mock_input):
        mock_input.side_effect = ['test test', 'Vlad']
        with does_not_raise():
            player = Player()
        self.assertEqual(player.name, 'Vlad')
        self.assertEqual(mock_input.call_count, 2)


class TestPlayerAttack(unittest.TestCase):
    @patch('source.models.InputGenerator')
    @patch('builtins.input')
    def test_player_attack_quit(self, mock_input, mock_input_generator):
        mock_input.side_effect = ['Vlad', '0']
        mock_input_generator.text.return_value = "doesn't matter"
        with self.assertRaises(QuitApp):
            player = Player()
            player.attack()

    @patch('source.models.InputGenerator')
    @patch('builtins.input')
    def test_player_attack_incorrect(self, mock_input, mock_input_generator):
        mock_input.side_effect = ['Vlad', 'wrong', '1']
        mock_input_generator.text.return_value = "doesn't matter"
        with does_not_raise():
            player = Player()
            player.attack()
        self.assertEqual(mock_input.call_count, 3)

    @patch('source.models.InputGenerator')
    @patch('builtins.input')
    def test_player_attack_correct(self, mock_input, mock_input_generator):
        mock_input.side_effect = ['Vlad', '1']
        mock_input_generator.text.return_value = "doesn't matter"
        with does_not_raise():
            player = Player()
            player.attack()
        self.assertEqual(mock_input.call_count, 2)


class TestPlayerLoseLives(unittest.TestCase):
    @patch('builtins.input')
    def test_player_lose_lives(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with does_not_raise():
            player = Player()
            player.on_lose_fight()

    @patch('builtins.input')
    def test_player_lose_lives_and_die(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with self.assertRaises(GameOver):
            player = Player()
            player.on_lose_fight()
            player.on_lose_fight()


class TestPlayerOnWinFight(unittest.TestCase):
    @patch('builtins.input')
    def test_player_win_fight_incorrect_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with self.assertRaises(IncorrectModeError):
            player = Player()
            player.on_win_fight('wrong')

    @patch('builtins.input')
    def test_player_win_fight_normal_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Normal')
        self.assertEqual(player.score, 1)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Hard')
        self.assertEqual(player.score, 2)

    @patch('builtins.input')
    def test_player_win_fight_normal_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Normal')
        player.on_win_fight('Normal')
        self.assertEqual(player.score, 2)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_win_fight('Hard')
        player.on_win_fight('Hard')
        self.assertEqual(player.score, 4)


class TestPlayerOnEnemyDown(unittest.TestCase):
    @patch('builtins.input')
    def test_player_win_fight_incorrect_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        with self.assertRaises(IncorrectModeError):
            player = Player()
            player.on_enemy_down('wrong')

    @patch('builtins.input')
    def test_player_win_fight_normal_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Normal')
        self.assertEqual(player.score, 5)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Hard')
        self.assertEqual(player.score, 10)

    @patch('builtins.input')
    def test_player_win_fight_normal_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Normal')
        player.on_enemy_down('Normal')
        self.assertEqual(player.score, 10)

    @patch('builtins.input')
    def test_player_win_fight_hard_mode_twice(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        player.on_enemy_down('Hard')
        player.on_enemy_down('Hard')
        self.assertEqual(player.score, 20)


class TestBattleInit(unittest.TestCase):
    @patch('builtins.input')
    def test_incorrect_init(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        enemy = Enemy(mode='Normal', level=1)
        with self.assertRaises(IncorrectModeError):
            Battle(player=player, enemy=enemy, mode='wrong')

    @patch('builtins.input')
    def test_correct_init(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        enemy = Enemy(mode='Normal', level=1)
        with does_not_raise():
            Battle(player=player, enemy=enemy, mode='Normal')


class TestBattleHandleFight(unittest.TestCase):

    @patch('builtins.input')
    def setUp(self, mock_input):
        mock_input.side_effect = ['Vlad']
        player = Player()
        enemy = Enemy(mode='Normal', level=3)
        self.battle = Battle(player=player, enemy=enemy, mode='Normal')

    def test_handle_incorrect_fight_result(self):
        with self.assertRaises(IncorrectFightResult):
            self.battle.handle_fight_result(2)

    def test_handle_1_fight_result(self):
        self.battle.handle_fight_result(1)
        self.assertEqual(self.battle.player.score, 1)
        self.assertEqual(self.battle.player.lives, PLAYER_LIVES)
        self.assertEqual(self.battle.enemy.lives, 2)

    def test_handle_0_fight_result(self):
        self.battle.handle_fight_result(0)
        self.assertEqual(self.battle.player.score, 0)
        self.assertEqual(self.battle.player.lives, PLAYER_LIVES)
        self.assertEqual(self.battle.enemy.lives, 3)

    def test_handle_minus_1_fight_result(self):
        self.battle.handle_fight_result(-1)
        self.assertEqual(self.battle.player.score, 0)
        self.assertEqual(self.battle.player.lives, PLAYER_LIVES - 1)
        self.assertEqual(self.battle.enemy.lives, 3)

    def test_handle_player_die(self):
        with self.assertRaises(GameOver):
            self.battle.handle_fight_result(-1)
            self.battle.handle_fight_result(-1)
        self.assertEqual(self.battle.player.score, 0)
        self.assertEqual(self.battle.player.lives, 0)
        self.assertEqual(self.battle.enemy.lives, 3)

    def test_handle_enemy_die(self):
        with self.assertRaises(EnemyDown):
            self.battle.handle_fight_result(1)
            self.battle.handle_fight_result(1)
            self.battle.handle_fight_result(1)
        self.assertEqual(self.battle.player.score, 8)
        self.assertEqual(self.battle.player.lives, 2)
        self.assertEqual(self.battle.enemy.lives, 0)


class TestAttackPairs(unittest.TestCase):
    def test_paper_paper(self):
        player_attack = PAPER
        enemy_attack = PAPER
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], DRAW)

    def test_paper_stone(self):
        player_attack = PAPER
        enemy_attack = STONE
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], WIN)

    def test_paper_scissors(self):
        player_attack = PAPER
        enemy_attack = SCISSORS
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], LOSE)

    def test_scissios_paper(self):
        player_attack = SCISSORS
        enemy_attack = PAPER
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], WIN)

    def test_scissors_stone(self):
        player_attack = SCISSORS
        enemy_attack = STONE
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], LOSE)

    def test_scissors_scissors(self):
        player_attack = SCISSORS
        enemy_attack = SCISSORS
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], DRAW)

    def test_stone_paper(self):
        player_attack = STONE
        enemy_attack = PAPER
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], LOSE)

    def test_stone_scissors(self):
        player_attack = STONE
        enemy_attack = SCISSORS
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], WIN)

    def test_stone_stone(self):
        player_attack = STONE
        enemy_attack = STONE
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)], DRAW)
