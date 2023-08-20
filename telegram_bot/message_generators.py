import datetime as dt
import math

from aiogram import types

import Sudoku.Board
import callback_datas as cbds
import enums
import markdown as md
import utils
from CustomMessage import CustomMessage
from database import models as dbm
from database.base import session_pool, func, select
import config


def get_start_message() -> CustomMessage:
    return CustomMessage(
        text=md.text(
            md.bold('👋 Hello!'),
            md.text(
                '🚀 This is a sudoku bot on the',
                md.bold('Aleo'),
                'blockchain'
            ),
            md.quote(
                '1️⃣ First, you need to create a wallet. To do this, ' +
                'open the profile with the /profile command',
                '2️⃣ To start a new game, use the /newgame command',
                sep='\n'
            ),
            sep='\n\n'
        )
    )


async def get_profile_message(
    user_id: int,
    show_sensitive_info: bool = False
) -> CustomMessage:
    user = await dbm.User.get_pk(user_id)

    if user.private_key:
        if show_sensitive_info:
            address = md.spoiler(user.address)
            view_key = md.spoiler(user.view_key)
            private_key = md.spoiler(user.private_key)
        else:
            address = md.bold('***')
            view_key = md.bold('***')
            private_key = md.bold('***')
    else:
        address = md.bold('Not created')
        view_key = md.bold('Not created')
        private_key = md.bold('Not created')

    profile_message = CustomMessage(
        text=md.text(
            md.bold('👤 Profile'),
            md.text(
                md.text(
                    md.bold('💵 Wallet address:'),
                    address
                ),
                md.text(
                    md.bold('🔐View key:'),
                    view_key
                ),
                md.text(
                    md.bold('🔑 Private key:'),
                    private_key
                ),
                sep='\n'
            ),
            md.italic(
                'You can also specify whether to display your address in the ' +
                'ranking of the best players: you can display it in full, in ' +
                'part or not at all'
            ),
            sep='\n\n'
        )
    )

    if user.private_key:
        if show_sensitive_info:
            sensitive_info_text = 'Hide'
        else:
            sensitive_info_text = 'Show'

        if user.address_privacy == enums.AddressPrivacy.PUBLIC:
            address_privacy_text = 'show full address'
        elif user.address_privacy == enums.AddressPrivacy.HIDDEN:
            address_privacy_text = 'show part of address'
        else:
            address_privacy_text = 'hide address'

        next_privacy_val = user.address_privacy.value + 1 if user.address_privacy.value < 3 else 1

        profile_message.add_rows(
            types.InlineKeyboardButton(
                text=f'{sensitive_info_text} sensitive info',
                callback_data=cbds.ShowProfile(
                    show_sensitive_info=not show_sensitive_info
                ).pack()
            ),
            types.InlineKeyboardButton(
                text=f'Address privacy: {address_privacy_text}',
                callback_data=cbds.ChangeAddressPrivacy(
                    privacy_value=next_privacy_val,
                    show_sensitive_info=show_sensitive_info
                ).pack()
            )
        )
    else:
        profile_message.add_rows(
            types.InlineKeyboardButton(
                text='Create wallet',
                callback_data=cbds.CreateWallet().pack()
            )
        )

    return profile_message


def get_new_game_message() -> CustomMessage:
    new_game_message = CustomMessage(
        text=md.text(
            md.bold('🔵 NEW GAME 🔵'),
            md.quote('Select difficulty:'),
            sep='\n'
        )
    )

    emojis = ['😀', '🙂', '😎', '🥶']

    for difficulty, emoji in zip(enums.SudokuDifficulty, emojis):
        new_game_message.add_rows(
            types.InlineKeyboardButton(
                text=f'{emoji} {difficulty.name.title()} {emoji}',
                callback_data=cbds.CreateNewGame(
                    difficulty=difficulty.value
                ).pack()
            )
        )

    return new_game_message


async def get_game_message(game_id: int, square: int = 0) -> CustomMessage:
    game = await dbm.game.Game.get_pk(game_id)
    board_nums = list(map(int, list(game.board_str)))
    board = Sudoku.Board.Board(board_nums.copy())

    elapsed_time = dt.datetime.now(dt.timezone.utc) - game.start_time
    elapsed_time = dt.timedelta(seconds=math.ceil(elapsed_time.total_seconds()))

    game_message = CustomMessage(
        text=md.text(
            md.bold('🟢 CURRENT GAME: 🟢'),
            md.text(
                md.text(
                    '🚀 Difficulty:',
                    md.italic(game.difficulty.name.title())
                ),
                md.text(
                    '🕛 Start time:',
                    md.italic(f'{game.start_time:%Y-%m-%d %H:%M:%S} UTC')
                ),
                md.text(
                    '🕝 Time elapsed:',
                    md.italic(utils.format_timedelta(elapsed_time))
                ),
                sep='\n'
            ),
            md.quote(board),
            md.italic('To check the board, click the button below'),
            sep='\n\n'
        )
    )

    first_row = square // 3 * 3
    first_col = square % 3 * 3

    for row in range(first_row, first_row + 3):
        row_buttons = []
        for col in range(first_col, first_col + 3):
            row_buttons.append(
                types.InlineKeyboardButton(
                    text=utils.emojize_number(board_nums[row * 9 + col]),
                    callback_data=cbds.EditValue(
                        game_id=game_id,
                        row=row,
                        column=col
                    ).pack()
                )
            )
        game_message.add_rows(row_buttons)

    row_move_buttons = []
    if square // 3 != 0:
        row_move_buttons.append(
            types.InlineKeyboardButton(
                text='⬆️',
                callback_data=cbds.ShowGame(
                    game_id=game_id,
                    square=square - 3
                ).pack()
            )
        )
    if square // 3 != 2:
        row_move_buttons.append(
            types.InlineKeyboardButton(
                text='⬇️',
                callback_data=cbds.ShowGame(
                    game_id=game_id,
                    square=square + 3
                ).pack()
            )
        )

    game_message.add_rows(row_move_buttons)

    col_move_buttons = []
    if square % 3 != 0:
        col_move_buttons.append(
            types.InlineKeyboardButton(
                text='⬅️',
                callback_data=cbds.ShowGame(
                    game_id=game_id,
                    square=square - 1
                ).pack()
            )
        )
    if square % 3 != 2:
        col_move_buttons.append(
            types.InlineKeyboardButton(
                text='➡️',
                callback_data=cbds.ShowGame(
                    game_id=game_id,
                    square=square + 1
                ).pack()
            )
        )

    game_message.add_rows(col_move_buttons)

    game_message.add_rows(
        [
            types.InlineKeyboardButton(
                text='🔄 Update',
                callback_data=cbds.ShowGame(
                    game_id=game_id,
                    square=square
                ).pack()
            ),
            types.InlineKeyboardButton(
                text='🚀 Check the board',
                callback_data=cbds.SendGame(
                    game_id=game_id
                ).pack()
            )
        ]
    )

    return game_message


async def get_edit_value_message(
    game_id: int,
    user_id: int,
    message_id: int,
    row: int,
    column: int
) -> CustomMessage:
    game = await dbm.Game.get_pk(game_id)

    board_nums = list(map(int, list(game.board_str)))

    edit_value_message = CustomMessage(
        text=md.text(
            md.bold('✏️ EDIT VALUE ✏️'),
            md.quote(
                'Select new value for cell',
                f'({row + 1}, {column + 1}), current value:',
                utils.emojize_number(board_nums[row * 9 + column])
            ),
            sep='\n'
        )
    )

    values_buttons = []

    for value in range(1, 10):
        values_buttons.append(
            types.InlineKeyboardButton(
                text=utils.emojize_number(value),
                callback_data=cbds.SumbitValue(
                    game_id=game_id,
                    message_id=message_id,
                    row=row,
                    column=column,
                    value=value
                ).pack()
            )
        )
        if value % 3 == 0:
            edit_value_message.add_rows(values_buttons)
            values_buttons = []

    edit_value_message.add_rows(
        types.InlineKeyboardButton(
            text='❌ CANCEL ❌',
            callback_data=cbds.DeleteMessage(user_id=user_id).pack()
        )
    )

    return edit_value_message


def get_top_difficulties_message():
    top_difficulties_message = CustomMessage(
        text=md.text(
            md.bold('Top difficulties'),
            md.quote('Select difficulty:'),
            sep='\n'
        )
    )

    emojis = ['😀', '🙂', '😎', '🥶']

    for difficulty, emoji in zip(enums.SudokuDifficulty, emojis):
        top_difficulties_message.add_rows(
            types.InlineKeyboardButton(
                text=f'{emoji} {difficulty.name.title()} {emoji}',
                callback_data=cbds.SelectTopDifficulty(
                    difficulty=difficulty.value
                ).pack()
            )
        )

    return top_difficulties_message


async def get_top_message(difficulty: enums.SudokuDifficulty) -> CustomMessage:
    async with session_pool() as session:
        max_time = func.min(dbm.Game.end_time - dbm.Game.start_time)
        top_positions = (await session.execute(
            select(
                dbm.Game.user_id,
                dbm.User.address,
                dbm.User.address_privacy,
                max_time
            ).join(
                dbm.User,
                dbm.User.user_id == dbm.Game.user_id
            ).filter(
                dbm.Game.end_time.isnot(None) &
                (dbm.Game.difficulty == difficulty)
            ).order_by(
                max_time
            ).group_by(
                dbm.Game.user_id,
                dbm.User.address,
                dbm.User.address_privacy
            ).limit(10)
        )).all()

    if not top_positions:
        return CustomMessage(
            text=md.text(
                'Unfortunately, the top is currently empty. You have every ' +
                'chance to be the first!'
            )
        )

    top_message = CustomMessage(
        text=md.bold(f'🏆 Top {difficulty.name.title()} players\n')
    )

    for position, top_player in enumerate(top_positions, 1):
        user_id, address, address_privacy, max_time = top_player
        if address_privacy == enums.AddressPrivacy.HIDDEN:
            address = address[:10] + '...' + address[-8:]
        elif address_privacy == enums.AddressPrivacy.PRIVATE:
            address = 'Anonymous'

        address = md.code(address)

        elapsed_time = dt.timedelta(seconds=math.ceil(max_time.total_seconds()))

        top_message.add_text(
            f'{position}\\. {address} \\- {utils.format_timedelta(elapsed_time)}'
        )

    top_message.add_rows(
        types.InlineKeyboardButton(
            text=config.RETURN_BUTTON,
            callback_data=cbds.ShowTopDifficulties().pack()
        )
    )

    return top_message


async def get_complete_message(
    game_id: int
) -> CustomMessage:
    game = await dbm.Game.get_pk(game_id)
    game = await game.update(end_time=func.now())

    result_message = CustomMessage(
        text=md.text(
            md.bold('🎉🚀 CONGRATULATIONS! 🚀'),
            md.quote(
                'You have successfully solved the Sudoku puzzle! Your ' +
                'logic and strategy skills are impressive. 🧠',
                f'Time spent: {utils.format_timedelta(game.end_time - game.start_time)}',
                'Are you ready for the next challenge?',
                sep='\n'
            ),
            sep='\n'
        )
    )

    return result_message
