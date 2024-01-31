import unittest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from settings import MODE_NORMAL, MODE_HARD, TEST_FILE_PATH
from source.game import Game
from source.record import GameRecord


class TestGameInitAndInputMode(unittest.TestCase):

    @patch("builtins.input")
    def test_game_init(self, mock_input):
        mock_input.side_effect = ['Vlad', "1"]
        with does_not_raise():
            game = Game()
        self.assertEqual(game.mode, MODE_NORMAL)

    @patch("builtins.input")
    def test_game_init_hard(self, mock_input):
        mock_input.side_effect = ['Vlad', "2"]
        with does_not_raise():
            game = Game()
        self.assertEqual(game.mode, MODE_HARD)

    @patch("builtins.input")
    def test_game_init_incorect_mode(self, mock_input):
        mock_input.side_effect = ['Vlad', "3", "1"]
        with does_not_raise():
            Game()

    @patch("builtins.input")
    def test_game_init_incorrect_mode(self, mock_input):
        mock_input.side_effect = ['Vlad', "blabla", "1"]
        with does_not_raise():
            Game()


class TestGameNewEnemy(unittest.TestCase):

    @patch("builtins.input")
    def test_game_init(self, mock_input):
        mock_input.side_effect = ['Vlad', "1"]
        game = Game()
        game.new_enemy()
        self.assertEqual(game.enemy.level, 1)
        game.new_enemy()
        self.assertEqual(game.enemy.level, 2)


class TestGameSaveScore(unittest.TestCase):

    @patch("source.record.get_score_file_path")
    @patch("builtins.input")
    def test_game_init(self, mock_input, mock_get_score_file_path):
        mock_input.side_effect = ['Vlad', "1"]
        game = Game()
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        game.save_score()
        new_gr = GameRecord(MODE_NORMAL)
        self.assertEqual(new_gr.records, game.game_record.records)


class TestGameStartPlay(unittest.TestCase):

    @patch("source.game.Game.save_score")
    @patch("source.models.randint")
    @patch("builtins.input")
    def test_start_game(self, mock_input, mock_randint, mock_save_score):
        mock_input.side_effect = ['Vlad', "1", "3", "2", "2"]
        mock_randint.return_value = 1
        with does_not_raise():
            game = Game()
            game.start_game()


