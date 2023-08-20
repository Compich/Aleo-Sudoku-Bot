from Sudoku import Generator, Board
import enums
from pathlib import Path

DIFFICULTIES = {
    enums.SudokuDifficulty.EASY: (35, 0),
    enums.SudokuDifficulty.MEDIUM: (81, 5),
    enums.SudokuDifficulty.HARD: (81, 10),
    enums.SudokuDifficulty.EXTREME: (81, 15)
}

def generate(difficulty: enums.SudokuDifficulty) -> Board.Board:
    difficulty_range = DIFFICULTIES[enums.SudokuDifficulty.EASY]

    gen = Generator.Generator(
        Path(__file__).parent / 'base.txt'
    )

    gen.randomize(100)

    initial = gen.board.copy()

    gen.reduce_via_logical(difficulty_range[0])

    if difficulty_range[1] != 0:
        gen.reduce_via_random(difficulty_range[1])


    final = gen.board.copy()

    return final
