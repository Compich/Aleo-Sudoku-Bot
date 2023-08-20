from enum import Enum


class SudokuDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXTREME = 4


class AddressPrivacy(Enum):
    PUBLIC = 1
    HIDDEN = 2
    PRIVATE = 3
