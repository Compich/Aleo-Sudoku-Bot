program sudoku_aleo.aleo {
    struct Row {
        c1: u8,
        c2: u8,
        c3: u8,
        c4: u8,
        c5: u8,
        c6: u8,
        c7: u8,
        c8: u8,
        c9: u8,
    }

    struct Board {
        r1: Row,
        r2: Row,
        r3: Row,
        r4: Row,
        r5: Row,
        r6: Row,
        r7: Row,
        r8: Row,
        r9: Row,
    }

    inline check_sequence(r1: u8, r2: u8, r3: u8, r4: u8, r5: u8, r6: u8, r7: u8, r8: u8, r9: u8) -> bool {
        return (
            r1 != 0u8 && r2 != 0u8 && r3 != 0u8 && r4 != 0u8 && r5 != 0u8 && r6 != 0u8 && r7 != 0u8 && r8 != 0u8 && r9 != 0u8 && 
            r1 != r2 && r1 != r3 && r1 != r4 && r1 != r5 && r1 != r6 && r1 != r7 && r1 != r8 && r1 != r9 &&
            r2 != r3 && r2 != r4 && r2 != r5 && r2 != r6 && r2 != r7 && r2 != r8 && r2 != r9 &&
            r3 != r4 && r3 != r5 && r3 != r6 && r3 != r7 && r3 != r8 && r3 != r9 &&
            r4 != r5 && r4 != r6 && r4 != r7 && r4 != r8 && r4 != r9 &&
            r5 != r6 && r5 != r7 && r5 != r8 && r5 != r9 &&
            r6 != r7 && r6 != r8 && r6 != r9 &&
            r7 != r8 && r7 != r9 &&
            r8 != r9
        );
    }

    transition check_for_complete(board: Board) -> u8 {
        if (!check_sequence(board.r1.c1, board.r1.c2, board.r1.c3, board.r1.c4, board.r1.c5, board.r1.c6, board.r1.c7, board.r1.c8, board.r1.c9)) {
            return 1u8;
        }
        else if (!check_sequence(board.r2.c1, board.r2.c2, board.r2.c3, board.r2.c4, board.r2.c5, board.r2.c6, board.r2.c7, board.r2.c8, board.r2.c9)) {
            return 2u8;
        }
        else if (!check_sequence(board.r3.c1, board.r3.c2, board.r3.c3, board.r3.c4, board.r3.c5, board.r3.c6, board.r3.c7, board.r3.c8, board.r3.c9)) {
            return 3u8;
        }
        else if (!check_sequence(board.r4.c1, board.r4.c2, board.r4.c3, board.r4.c4, board.r4.c5, board.r4.c6, board.r4.c7, board.r4.c8, board.r4.c9)) {
            return 4u8;
        }
        else if (!check_sequence(board.r5.c1, board.r5.c2, board.r5.c3, board.r5.c4, board.r5.c5, board.r5.c6, board.r5.c7, board.r5.c8, board.r5.c9)) {
            return 5u8;
        }
        else if (!check_sequence(board.r6.c1, board.r6.c2, board.r6.c3, board.r6.c4, board.r6.c5, board.r6.c6, board.r6.c7, board.r6.c8, board.r6.c9)) {
            return 6u8;
        }
        else if (!check_sequence(board.r7.c1, board.r7.c2, board.r7.c3, board.r7.c4, board.r7.c5, board.r7.c6, board.r7.c7, board.r7.c8, board.r7.c9)) {
            return 7u8;
        }
        else if (!check_sequence(board.r8.c1, board.r8.c2, board.r8.c3, board.r8.c4, board.r8.c5, board.r8.c6, board.r8.c7, board.r8.c8, board.r8.c9)) {
            return 8u8;
        }
        else if (!check_sequence(board.r9.c1, board.r9.c2, board.r9.c3, board.r9.c4, board.r9.c5, board.r9.c6, board.r9.c7, board.r9.c8, board.r9.c9)) {
            return 9u8;
        }
        else if (!check_sequence(board.r1.c1, board.r2.c1, board.r3.c1, board.r4.c1, board.r5.c1, board.r6.c1, board.r7.c1, board.r8.c1, board.r9.c1)) {
            return 10u8;
        }
        else if (!check_sequence(board.r1.c2, board.r2.c2, board.r3.c2, board.r4.c2, board.r5.c2, board.r6.c2, board.r7.c2, board.r8.c2, board.r9.c2)) {
            return 11u8;
        }
        else if (!check_sequence(board.r1.c3, board.r2.c3, board.r3.c3, board.r4.c3, board.r5.c3, board.r6.c3, board.r7.c3, board.r8.c3, board.r9.c3)) {
            return 12u8;
        }
        else if (!check_sequence(board.r1.c4, board.r2.c4, board.r3.c4, board.r4.c4, board.r5.c4, board.r6.c4, board.r7.c4, board.r8.c4, board.r9.c4)) {
            return 13u8;
        }
        else if (!check_sequence(board.r1.c5, board.r2.c5, board.r3.c5, board.r4.c5, board.r5.c5, board.r6.c5, board.r7.c5, board.r8.c5, board.r9.c5)) {
            return 14u8;
        }
        else if (!check_sequence(board.r1.c6, board.r2.c6, board.r3.c6, board.r4.c6, board.r5.c6, board.r6.c6, board.r7.c6, board.r8.c6, board.r9.c6)) {
            return 15u8;
        }
        else if (!check_sequence(board.r1.c7, board.r2.c7, board.r3.c7, board.r4.c7, board.r5.c7, board.r6.c7, board.r7.c7, board.r8.c7, board.r9.c7)) {
            return 16u8;
        }
        else if (!check_sequence(board.r1.c8, board.r2.c8, board.r3.c8, board.r4.c8, board.r5.c8, board.r6.c8, board.r7.c8, board.r8.c8, board.r9.c8)) {
            return 17u8;
        }
        else if (!check_sequence(board.r1.c9, board.r2.c9, board.r3.c9, board.r4.c9, board.r5.c9, board.r6.c9, board.r7.c9, board.r8.c9, board.r9.c9)) {
            return 18u8;
        }

        return 0u8;
    }
}
