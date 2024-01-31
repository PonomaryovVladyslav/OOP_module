from source.exceptions import RecordInRecordsError
from source.models import Player
from settings import SCORE_FILE, MAX_RECORDS_NUMBER, NAME_ADDITIONAL_SPACES


def record_file_title_row(name_column_size: int) -> str:
    """
    Create title for a score file
    :param name_column_size: size of the column for name
    """
    return f'{"NAME".ljust(name_column_size)}{"MODE".ljust(10)}SCORE\n'


class PlayerRecord:
    """
    Class for one player record in score table
    """
    name: str
    mode: str
    score: int

    def __init__(self, name: str, mode: str, score: int) -> None:
        """
        Initialize the player record
        :param name: - name of the player
        :param mode: - mode of the game
        :param score: - score of the player
        """
        self.name = name
        self.mode = mode
        self.score = score

    def __eq__(self, other):
        """
        To find record in the list of records
        """
        return self.name == other.name and self.mode == other.mode and self.score == other.score

    def __gt__(self, other):
        """
        To find name in score list with the bigger name size
        """
        return len(self.name) > len(other.name)

    def as_file_row(self, name_column_size: int) -> str:
        """
        Create record for a score file
        :param name_column_size: - size of the column for name
        """
        return f'{self.name.ljust(name_column_size)}{self.mode.ljust(10)}{self.score}\n'


class GameRecord:
    """
    Class for full game records
    """
    records: list[PlayerRecord] = []
    mode: str

    def __init__(self, mode: str):
        """
        Initialize the game record
        :param mode: - mode of the game
        """
        self.mode = mode
        self.read_records()

    def read_records(self) -> None:
        """
        Read records from score file
        """
        with open(SCORE_FILE, 'r') as file:
            lines = file.readlines()
        del lines[0]  # remove table title
        for line in lines:
            name, mode, score = line.split()
            self.records.append(PlayerRecord(name, mode, int(score)))

    def _validate_record(self, record: PlayerRecord) -> None:
        """
        Validate record to check if record exists in the list
        :param record:"""
        if record in self.records:
            raise RecordInRecordsError

    def add_record(self, player: Player) -> None:
        """
        Add a record to the game records
        :param player: based on player
        """
        player_record = PlayerRecord(player.name, self.mode, player.score)
        try:
            self._validate_record(player_record)
            self.records.append(player_record)
        except RecordInRecordsError:
            raise

    def _sort_records(self) -> list[PlayerRecord]:
        """
        Sort the records by score
        """
        return sorted(self.records, key=lambda x: int(x.score), reverse=True)

    @staticmethod
    def _cut_records(records: list[PlayerRecord]) -> list[PlayerRecord]:
        """
        Cut records by max size of score table
        """
        return records[:MAX_RECORDS_NUMBER]

    @property
    def _prepared_records_to_save(self) -> list[PlayerRecord]:
        """
        Prepare the records to save
        """
        records = self._sort_records()
        return self._cut_records(records)

    def save_to_file(self) -> None:
        """
        Save scores to the file
        """
        records = self._prepared_records_to_save
        name_column_size = len(max(records).name) + NAME_ADDITIONAL_SPACES
        with open(SCORE_FILE, 'w') as file:
            file.write(record_file_title_row(name_column_size))
            for record in records:
                file.write(record.as_file_row(name_column_size))
