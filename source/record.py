from source.exceptions import RecordInRecordsError
from source.models import Player
from settings import SCORE_FILE, MAX_RECORDS_NUMBER, NAME_ADDITIONAL_SPACES, ROOT_DIR
from source.validations import validated_score_row_size, validate_mode


def record_file_title_row(name_column_size: int = 0) -> str:
    """
    Create title for a score file
    :param name_column_size: size of the column for name
    """
    name_column_size = validated_score_row_size(name_column_size)
    return f'{"NAME".ljust(name_column_size)}{"MODE".ljust(10)}SCORE\n'


def get_score_file_path() -> str:
    """
    Get score file path
    """
    return f'{ROOT_DIR}/{SCORE_FILE}'


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
        validate_mode(mode)
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

    def __str__(self):
        """
        To print pretty text :)
        """
        size = len("NAME") + 1
        if len(self.name) > size:
            size = len(self.name) + 1

        return self.as_file_row(size)

    def as_file_row(self, name_column_size: int) -> str:
        """
        Create record for a score file
        :param name_column_size: - size of the column for name
        """
        name_column_size = validated_score_row_size(name_column_size)
        return f'{self.name.ljust(name_column_size)}{self.mode.ljust(10)}{self.score}\n'

    @classmethod
    def from_player(cls, player: Player, mode: str) -> "PlayerRecord":
        validate_mode(mode)
        return PlayerRecord(name=player.name, mode=mode, score=player.score)


class GameRecord:
    """
    Class for full game records
    """
    records: list[PlayerRecord]
    mode: str

    def __init__(self, mode: str):
        """
        Initialize the game record
        :param mode: - mode of the game
        """
        validate_mode(mode)
        self.mode = mode
        self.read_records()

    def read_records(self) -> None:
        """
        Read records from score file
        """
        self.records = []
        try:
            with open(get_score_file_path(), 'r') as file:
                lines = file.readlines()
            del lines[0]  # remove table title
            for line in lines:
                name, mode, score = line.split()
                self.records.append(PlayerRecord(name, mode, int(score)))
        except FileNotFoundError:
            with open(get_score_file_path(), 'w') as file:
                file.write(record_file_title_row())
            self.read_records()

    def _validate_record(self, record: PlayerRecord) -> None:
        """
        Validate record to check if record exists in the list
        :param record:"""
        if record in self.records:
            raise RecordInRecordsError

    def add_record_from_player(self, player: Player) -> None:
        """
        Add a record from player
        :param player: based on player
        """
        player_record = PlayerRecord.from_player(player, self.mode)
        self.add_record(player_record)

    def add_record(self, player_record: PlayerRecord) -> None:
        """
        Add a record to the game records
        :param player_record: based on player
        """
        try:
            self._validate_record(player_record)
            self.records.append(player_record)
        except RecordInRecordsError:
            raise

    def _sort_records(self):
        """
        Sort the records by score
        """
        self.records = sorted(self.records, key=lambda x: int(x.score), reverse=True)

    def _cut_records(self):
        """
        Cut records by max size of score table
        """
        self.records = self.records[:MAX_RECORDS_NUMBER]

    def _prepare_records_to_save(self):
        """
        Prepare the records to save
        """
        self._sort_records()
        self._cut_records()

    def save_to_file(self) -> None:
        """
        Save scores to the file
        """
        self._prepare_records_to_save()
        name_column_size = len(max(self.records).name) + NAME_ADDITIONAL_SPACES
        name_column_size = validated_score_row_size(name_column_size)
        if name_column_size < len("NAME"):
            name_column_size = len("NAME")
        with open(get_score_file_path(), 'w') as file:
            file.write(record_file_title_row(name_column_size))
            for record in self.records:
                file.write(record.as_file_row(name_column_size))
