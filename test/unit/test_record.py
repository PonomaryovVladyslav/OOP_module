import os
import unittest
from contextlib import nullcontext as does_not_raise
from unittest.mock import patch

from settings import MODE_NORMAL, MODE_HARD, TEST_FILE_PATH, WRONG_TEST_FILE_PATH, \
    NEW_TEST_FILE_PATH
from source.exceptions import IncorrectModeError, RecordInRecordsError
from source.models import Player
from source.record import record_file_title_row, PlayerRecord, GameRecord

BASIC_TEST_RECORDS = [
    PlayerRecord("test1", MODE_NORMAL, 10),
    PlayerRecord("test2", MODE_HARD, 8),
    PlayerRecord("test3", MODE_NORMAL, 6),
    PlayerRecord("test4", MODE_HARD, 4),
    PlayerRecord("test5", MODE_NORMAL, 2),
]


class TestRecordTitleRow(unittest.TestCase):
    def test_correct_title_size(self):
        self.assertEqual(record_file_title_row(10), "NAME      MODE      SCORE\n")

    def test_incorrect_title_size(self):
        self.assertEqual(record_file_title_row(2), "NAME MODE      SCORE\n")


class TestPlayerRecordInit(unittest.TestCase):
    def test_player_record_init_invalid(self):
        with self.assertRaises(IncorrectModeError):
            PlayerRecord("Vlad", "wrong", 20)

    def test_player_record_init_valid_normal(self):
        with does_not_raise():
            PlayerRecord("Vlad", MODE_NORMAL, 20)

    def test_player_record_init_valid_hard(self):
        with does_not_raise():
            PlayerRecord("Vlad", MODE_HARD, 20)


class TestPlayerRecordAsFileRow(unittest.TestCase):
    def test_valid_size(self):
        pr = PlayerRecord("Vlad", MODE_NORMAL, 20)
        self.assertEqual(pr.as_file_row(10), "Vlad      Normal    20\n")

    def test_invalid_size(self):
        pr = PlayerRecord("Vlad", MODE_NORMAL, 20)
        self.assertEqual(pr.as_file_row(0), "Vlad Normal    20\n")


class TestPlayerRecordEq(unittest.TestCase):
    def test_player_record_eq(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 20)
        pr2 = PlayerRecord("Vlad", MODE_NORMAL, 20)
        self.assertEqual(pr1, pr2)

    def test_player_record_eq_in_list(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 20)
        pr2 = PlayerRecord("Vlad", MODE_NORMAL, 30)
        pr3 = PlayerRecord("Vlad", MODE_NORMAL, 40)
        self.assertTrue(pr1 in [pr1, pr2])
        self.assertFalse(pr2 in [pr1, pr3])


class TestPlayerRecordGt(unittest.TestCase):
    def test_player_record_gt(self):
        with does_not_raise():
            pr1 = PlayerRecord("Vlad", MODE_NORMAL, 20)
            pr2 = PlayerRecord("Vlad", MODE_NORMAL, 30)
            self.assertFalse(pr1 > pr2)

    def test_player_record_sorting(self):
        pr1 = PlayerRecord("Vlad", MODE_NORMAL, 20)
        pr2 = PlayerRecord("SomeLongName", MODE_NORMAL, 40)
        pr3 = PlayerRecord("Vlad", MODE_NORMAL, 30)

        self.assertEqual([pr1, pr3, pr2], sorted([pr1, pr2, pr3]))


class TestPlayerRecordFromPlayer(unittest.TestCase):
    @patch("builtins.input")
    def test_from_player_valid_norm(self, mock_input):
        mock_input.return_value = "Vlad"
        player = Player()
        with (does_not_raise()):
            pr = PlayerRecord.from_player(player, MODE_NORMAL)
            self.assertEqual(pr.name, player.name)
            self.assertEqual(pr.mode, MODE_NORMAL)
            self.assertEqual(pr.score, player.score)

    @patch("builtins.input")
    def test_from_player_valid_hard(self, mock_input):
        mock_input.return_value = "Vlad"
        player = Player()
        with does_not_raise():
            pr = PlayerRecord.from_player(player, MODE_HARD)
            self.assertEqual(pr.name, player.name)
            self.assertEqual(pr.mode, MODE_HARD)
            self.assertEqual(pr.score, player.score)

    @patch("builtins.input")
    def test_from_player_invalid(self, mock_input):
        mock_input.return_value = "Vlad"
        player = Player()
        with self.assertRaises(IncorrectModeError):
            PlayerRecord.from_player(player, "wrong")


class TestGameRecordInit(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_player_record_init_invalid(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        with self.assertRaises(IncorrectModeError):
            GameRecord("wrong")

    @patch("source.record.get_score_file_path")
    def test_player_record_init_valid_normal(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        with does_not_raise():
            GameRecord(MODE_NORMAL)

    @patch("source.record.get_score_file_path")
    def test_player_record_init_valid_hard(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        with does_not_raise():
            GameRecord(MODE_HARD)


class TestGameRecordReadfile(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_read_records(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        gr = GameRecord(MODE_NORMAL)
        self.assertEqual(gr.records, BASIC_TEST_RECORDS)

    @patch("source.record.get_score_file_path")
    def test_read_records_wrong_file(self, mock_get_score_file_path):
        filepath = WRONG_TEST_FILE_PATH
        mock_get_score_file_path.return_value = filepath
        gr = GameRecord(MODE_NORMAL)
        # TODO: INCORRECT BEHAVIOUR SHOULD BE TEMPORARY FILE
        os.remove(filepath)
        self.assertEqual(gr.records, [])


class TestGameRecordAddRecord(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_add_record_success(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 12)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)

        self.assertEqual(gr.records, [*BASIC_TEST_RECORDS, pr_new])

    @patch("source.record.get_score_file_path")
    def test_add_record_fail(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test5", MODE_NORMAL, 2)
        gr = GameRecord(MODE_NORMAL)
        with self.assertRaises(RecordInRecordsError):
            gr.add_record(pr_new)
        self.assertEqual(gr.records, BASIC_TEST_RECORDS)


class TestGameRecordValidate(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_add_record_success(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 12)
        gr = GameRecord(MODE_NORMAL)
        with does_not_raise():
            gr._validate_record(pr_new)

    @patch("source.record.get_score_file_path")
    def test_add_record_fail(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test5", MODE_NORMAL, 2)
        gr = GameRecord(MODE_NORMAL)
        with self.assertRaises(RecordInRecordsError):
            gr._validate_record(pr_new)


class TestGameRecordSort(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_sort_records_middle(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 7)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._sort_records()
        self.assertEqual(gr.records, BASIC_TEST_RECORDS[:2] + [pr_new] + BASIC_TEST_RECORDS[2:])

    @patch("source.record.get_score_file_path")
    def test_sort_records_end(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 0)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._sort_records()
        self.assertEqual(gr.records, BASIC_TEST_RECORDS + [pr_new])

    @patch("source.record.get_score_file_path")
    def test_sort_records_start(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 20)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._sort_records()
        self.assertEqual(gr.records, [pr_new] + BASIC_TEST_RECORDS)


class TestGameRecordCut(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_cut_records(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 7)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._cut_records()
        self.assertEqual(gr.records, BASIC_TEST_RECORDS)


class TestGameRecordPrepare(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_sort_records_middle(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 7)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._prepare_records_to_save()
        self.assertEqual(gr.records, BASIC_TEST_RECORDS[:2] + [pr_new] + BASIC_TEST_RECORDS[2:4])

    @patch("source.record.get_score_file_path")
    def test_sort_records_end(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 0)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._prepare_records_to_save()
        self.assertEqual(gr.records, BASIC_TEST_RECORDS)

    @patch("source.record.get_score_file_path")
    def test_sort_records_start(self, mock_get_score_file_path):
        mock_get_score_file_path.return_value = TEST_FILE_PATH
        pr_new = PlayerRecord("test6", MODE_NORMAL, 20)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr._prepare_records_to_save()
        self.assertEqual(gr.records, [pr_new] + BASIC_TEST_RECORDS[:-1])


class TestGameRecordSaveToFile(unittest.TestCase):
    @patch("source.record.get_score_file_path")
    def test_save_middle(self, mock_get_score_file_path):
        mock_get_score_file_path.side_effect = [TEST_FILE_PATH, NEW_TEST_FILE_PATH, NEW_TEST_FILE_PATH]
        pr_new = PlayerRecord("test6", MODE_NORMAL, 7)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr.save_to_file()
        new_gr = GameRecord(MODE_NORMAL)
        os.remove(NEW_TEST_FILE_PATH)
        self.assertEqual(new_gr.records, BASIC_TEST_RECORDS[:2] + [pr_new] + BASIC_TEST_RECORDS[2:4])

    @patch("source.record.get_score_file_path")
    def test_save_end(self, mock_get_score_file_path):
        mock_get_score_file_path.side_effect = [TEST_FILE_PATH, NEW_TEST_FILE_PATH,
                                                NEW_TEST_FILE_PATH]
        pr_new = PlayerRecord("test6", MODE_NORMAL, 0)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr.save_to_file()
        new_gr = GameRecord(MODE_NORMAL)
        os.remove(NEW_TEST_FILE_PATH)
        self.assertEqual(new_gr.records, BASIC_TEST_RECORDS)

    @patch("source.record.get_score_file_path")
    def test_save_start(self, mock_get_score_file_path):
        mock_get_score_file_path.side_effect = [TEST_FILE_PATH, NEW_TEST_FILE_PATH,
                                                NEW_TEST_FILE_PATH]
        pr_new = PlayerRecord("test6", MODE_NORMAL, 20)
        gr = GameRecord(MODE_NORMAL)
        gr.add_record(pr_new)
        gr.save_to_file()
        new_gr = GameRecord(MODE_NORMAL)
        os.remove(NEW_TEST_FILE_PATH)
        self.assertEqual(new_gr.records, [pr_new] + BASIC_TEST_RECORDS[:-1])
