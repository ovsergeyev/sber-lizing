import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from core.handlers.common import delete_post
from settings import settings


async def startup(bot: Bot):
    await bot.send_message(settings.bot.chat_id, "Bot started")


async def shutdown(bot: Bot):
    await bot.send_message(settings.bot.chat_id, "Bot stopped")


async def run_bot():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )

    bot = Bot(settings.bot.token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # dp.startup.register(startup)
    # dp.shutdown.register(shutdown)

    dp.callback_query.register(delete_post)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(run_bot())
