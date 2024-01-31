""" User defined Exceptions """


class GameOver(Exception):
    """raised if player lost all lives"""


class EnemyDown(Exception):
    """Raised in case enemy lost all lives"""


class QuitApp(Exception):
    """Raised if user send command to exit the unfinished game"""


class WhiteSpaceInputError(Exception):
    """ Raised if user input contains white spaces"""


class EmptyInputError(Exception):
    """ Raised if user input is an empty string"""


class RecordInRecordsError(Exception):
    """ Raised if user record already exists"""


class IncorrectInputTypeError(Exception):
    """ Raised if input type is incorrect """
