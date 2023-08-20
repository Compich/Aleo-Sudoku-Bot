import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_default import BotCommandScopeDefault

import config
import handlers
import middlewares as mdlw


async def on_startup(bot: Bot):
    default_commands = [
        BotCommand(
            command='profile',
            description='Open profile'
        ),
        BotCommand(
            command='newgame',
            description='Start new game'
        ),
        BotCommand(
            command='top',
            description='Show top players'
        )
    ]

    await bot.set_my_commands(
        commands=default_commands,
        scope=BotCommandScopeDefault()
    )


async def main():
    dispatcher = Dispatcher()
    bot = Bot(config.BOT_TOKEN, parse_mode='MarkdownV2')

    dispatcher.include_routers(
        handlers.user_router
    )

    dispatcher.startup.register(on_startup)

    dispatcher.message.middleware(mdlw.UpdateUserMiddleware())
    dispatcher.callback_query.middleware(mdlw.UpdateUserMiddleware())

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.warning('Aleo Sudoku Bot')

    asyncio.run(main())
