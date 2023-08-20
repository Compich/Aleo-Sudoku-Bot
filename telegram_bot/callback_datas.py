from aiogram.filters.callback_data import CallbackData


class CreateNewGame(CallbackData, prefix='CreateNewGame'):
    difficulty: int


class EditValue(CallbackData, prefix='EditValue'):
    game_id: int
    row: int
    column: int


class SumbitValue(CallbackData, prefix='SumbitValue'):
    game_id: int
    message_id: int
    row: int
    column: int
    value: int


class CreateWallet(CallbackData, prefix='CreateWallet'):
    ...


class ShowProfile(CallbackData, prefix='ShowProfile'):
    show_sensitive_info: bool = False


class ShowGame(CallbackData, prefix='ShowGame'):
    game_id: int
    square: int = 0


class SendGame(CallbackData, prefix='SendGame'):
    game_id: int


class DoNothing(CallbackData, prefix='DoNothing'):
    ...


class DeleteMessage(CallbackData, prefix='DeleteMessage'):
    user_id: int


class ChangeAddressPrivacy(CallbackData, prefix='ChangeAddressPrivacy'):
    privacy_value: int
    show_sensitive_info: bool = False


class SelectTopDifficulty(CallbackData, prefix='SelectTopDifficulty'):
    difficulty: int


class ShowTopDifficulties(CallbackData, prefix='ShowTopDifficulties'):
    ...
