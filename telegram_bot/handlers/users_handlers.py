import re
from contextlib import suppress

from aiogram import Bot, Router
from aiogram import exceptions as aioexc
from aiogram import filters, types

import callback_datas as cbds
import config
import enums
import message_generators as msggen
import run_leo
import sudoku_generator
import utils
from database import models as dbm
from run_leo import utils as leo_utils

user_router = Router()


@user_router.message(
    filters.Command(commands='start')
)
async def start(message: types.Message):
    start_message = msggen.get_start_message()

    await message.answer(
        text=start_message.text,
        reply_markup=start_message.keyboard
    )


@user_router.message(
    filters.Command(commands='profile')
)
async def profile(message: types.Message):
    profile_message = await msggen.get_profile_message(
        user_id=message.from_user.id
    )

    await message.answer(
        text=profile_message.text,
        reply_markup=profile_message.keyboard
    )


@user_router.callback_query(
    cbds.ShowProfile.filter()
)
async def show_profile_cb(
    call: types.CallbackQuery,
    callback_data: cbds.ShowProfile
):
    profile_message = await msggen.get_profile_message(
        user_id=call.from_user.id,
        show_sensitive_info=callback_data.show_sensitive_info
    )

    await call.message.edit_text(
        text=profile_message.text,
        reply_markup=profile_message.keyboard
    )


@user_router.callback_query(
    cbds.CreateWallet.filter()
)
async def create_wallet(
    call: types.CallbackQuery,
    user: dbm.User
):
    if user.private_key:
        await call.answer(
            text='You already have a wallet',
            show_alert=True
        )
        return

    new_wallet = run_leo.Account.new()

    await user.update(
        address=new_wallet.address,
        view_key=new_wallet.view_key,
        private_key=new_wallet.private_key
    )

    profile_message = await msggen.get_profile_message(
        user_id=call.from_user.id,
        show_sensitive_info=True
    )

    await call.message.edit_text(
        text=profile_message.text,
        reply_markup=profile_message.keyboard
    )


@user_router.message(
    filters.Command(commands='newgame')
)
async def new_game(message: types.Message):
    new_game_message = msggen.get_new_game_message()

    await message.answer(
        text=new_game_message.text,
        reply_markup=new_game_message.keyboard
    )


@user_router.callback_query(
    cbds.CreateNewGame.filter()
)
async def create_new_game_cb(
    call: types.CallbackQuery,
    callback_data: cbds.CreateNewGame,
    user: dbm.User
):
    if not user.private_key:
        await call.answer(
            text='You need to create a wallet first',
            show_alert=True
        )
        return

    board = sudoku_generator.generate(callback_data.difficulty)
    board_str = utils.int_list_to_str(board.to_int_list())

    game = await dbm.Game.add_new(
        user_id=call.from_user.id,
        difficulty=enums.SudokuDifficulty(callback_data.difficulty),
        start_game_str=board_str,
        board_str=board_str
    )

    game_message = await msggen.get_game_message(
        game_id=game.game_id
    )

    await call.message.edit_text(
        text=game_message.text,
        reply_markup=game_message.keyboard
    )


@user_router.callback_query(
    cbds.ShowGame.filter()
)
async def update_game_cb(
    call: types.CallbackQuery,
    callback_data: cbds.ShowGame
):
    game_message = await msggen.get_game_message(
        game_id=callback_data.game_id,
        square=callback_data.square
    )

    with suppress(aioexc.TelegramBadRequest):
        await call.message.edit_text(
            text=game_message.text,
            reply_markup=game_message.keyboard
        )


@user_router.callback_query(
    cbds.EditValue.filter()
)
async def edit_value_cb(
    call: types.CallbackQuery,
    callback_data: cbds.EditValue
):
    game = await dbm.Game.get_pk(callback_data.game_id)

    if game.user_id != call.from_user.id:
        return

    position = callback_data.row * 9 + callback_data.column

    if game.start_board_str[position] != '0':
        await call.answer(
            text='You can\'t change this value',
            show_alert=True
        )
        return

    edit_value_message = await msggen.get_edit_value_message(
        game_id=callback_data.game_id,
        user_id=call.from_user.id,
        message_id=call.message.message_id,
        row=callback_data.row,
        column=callback_data.column
    )

    await call.message.answer(
        text=edit_value_message.text,
        reply_markup=edit_value_message.keyboard
    )

    await call.answer(
        text='Select new value'
    )


@user_router.callback_query(
    cbds.DeleteMessage.filter()
)
async def delete_message_cb(
    call: types.CallbackQuery,
    callback_data: cbds.DeleteMessage
):
    if call.from_user.id != callback_data.user_id:
        return

    await call.message.delete()


@user_router.callback_query(
    cbds.SumbitValue.filter()
)
async def submit_value_cb(
    call: types.CallbackQuery,
    callback_data: cbds.SumbitValue,
    bot: Bot
):
    game = await dbm.Game.get_pk(callback_data.game_id)

    if game.user_id != call.from_user.id:
        return

    board_nums = list(map(int, list(game.board_str)))

    board_nums[callback_data.row * 9 + callback_data.column] = callback_data.value
    board = sudoku_generator.Board.Board(board_nums)
    board_str = utils.int_list_to_str(board.to_int_list())

    await game.update(board_str=board_str)

    game_message = await msggen.get_game_message(
        game_id=callback_data.game_id,
        square=callback_data.row // 3 * 3 + callback_data.column // 3
    )

    await bot.edit_message_text(
        text=game_message.text,
        reply_markup=game_message.keyboard,
        chat_id=call.message.chat.id,
        message_id=callback_data.message_id,
    )

    await call.message.delete()


@user_router.callback_query(
    cbds.SendGame.filter()
)
async def send_value(
    call: types.CallbackQuery,
    callback_data: cbds.SendGame
):
    game = await dbm.Game.get_pk(callback_data.game_id)

    if game.user_id != call.from_user.id:
        return

    aleo_string = utils.string_to_aleo_format(game.board_str)

    try:
        result = leo_utils.run_command_in_directory(
            command=[
                'run',
                '--path',
                config.SUDOKU_ALEO_DIR,
                'check_for_complete',
                f'{aleo_string}'
            ]
        )
    except Exception as e:
        await call.answer(
            text='Error occurred while checking the board',
            show_alert=True
        )
        return

    res = re.search(r'• (?P<result>\d{1,2})u8', result)
    if not res:
        await call.answer(
            text='Error occurred while checking the board',
            show_alert=True
        )
        return

    result = int(res.group('result'))

    if result == 0:
        complete_message = await msggen.get_complete_message(
            game_id=callback_data.game_id
        )

        await call.message.edit_text(
            text=complete_message.text,
            reply_markup=complete_message.keyboard
        )
    elif 1 <= result <= 9:
        await call.answer(
            text=f'⚠️ You have a mistake in {result} row',
            show_alert=True
        )
    elif 10 <= result <= 18:
        await call.answer(
            text=f'⚠️ You have a mistake in {result - 9} column',
            show_alert=True
        )


@user_router.callback_query(
    cbds.ChangeAddressPrivacy.filter()
)
async def change_address_privacy_cb(
    call: types.CallbackQuery,
    callback_data: cbds.ChangeAddressPrivacy,
    user: dbm.User
):
    if user.private_key:
        await user.update(
            address_privacy=enums.AddressPrivacy(callback_data.privacy_value)
        )

        profile_message = await msggen.get_profile_message(
            user_id=call.from_user.id,
            show_sensitive_info=callback_data.show_sensitive_info
        )

        await call.message.edit_text(
            text=profile_message.text,
            reply_markup=profile_message.keyboard
        )
    else:
        await call.answer(
            text='You need to create a wallet first',
            show_alert=True
        )


@user_router.message(
    filters.Command(commands='top')
)
async def top(message: types.Message):
    top_difficulties_message = msggen.get_top_difficulties_message()

    await message.answer(
        text=top_difficulties_message.text,
        reply_markup=top_difficulties_message.keyboard
    )


@user_router.callback_query(
    cbds.ShowTopDifficulties.filter()
)
async def top_cb(
    call: types.CallbackQuery,
    callback_data: cbds.ShowTopDifficulties
):
    top_difficulties_message = msggen.get_top_difficulties_message()

    await call.message.edit_text(
        text=top_difficulties_message.text,
        reply_markup=top_difficulties_message.keyboard
    )


@user_router.callback_query(
    cbds.SelectTopDifficulty.filter()
)
async def select_top_difficulty_cb(
    call: types.CallbackQuery,
    callback_data: cbds.SelectTopDifficulty
):
    top_players_message = await msggen.get_top_message(
        difficulty=enums.SudokuDifficulty(callback_data.difficulty)
    )

    await call.message.edit_text(
        text=top_players_message.text,
        reply_markup=top_players_message.keyboard
    )
