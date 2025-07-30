import asyncio

from aiogram import Bot
from aiogram.types import URLInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from fake_useragent import UserAgent

from core.schemas.avto_schema import AutoSchema as Auto
from settings import settings


class TgBot:
    def __init__(self):
        self.bot = Bot(token=settings.bot.token)
        self.chat_id = settings.bot.chat_id
        self.ua = UserAgent(browsers=["chrome"])

    async def send_message(self, auto: Auto):
        headers = {"user-agent": self.ua.random}

        image_from_url = URLInputFile(auto.image_url, headers=headers)
        price_formatted = f"{auto.price:,}".replace(",", " ")

        caption_lines = [
            f"<b>{auto.title}</b>\n\r",
        ]

        if getattr(auto, "brand", None):
            caption_lines.append(f"<b>Марка:</b> <code>{auto.brand}</code>")

        if getattr(auto, "model", None):
            caption_lines.append(f"<b>Модель:</b> <code>{auto.model}</code>")

        if getattr(auto, "year_of_release", None):
            caption_lines.append(
                f"<b>Год выпуска:</b> <code>{auto.year_of_release}</code>"
            )

        if getattr(auto, "mileage", None):
            mileage_formatted = f"{auto.mileage:,}".replace(",", " ")
            caption_lines.append(f"<b>Пробег:</b> <code>{mileage_formatted} км.</code>")

        caption_lines.append(f"<b>Адрес:</b> <code>{auto.location}</code>")

        if getattr(auto, "old_price", None):
            old_price_formatted = f"{auto.old_price:,}".replace(",", " ")
            caption_lines.append(f"<b>Старая цена:</b> <s>{old_price_formatted} ₽</s>")

        caption_lines.append(f"<b>Цена:</b> <code>{price_formatted} ₽</code> \n\r")
        caption_lines.append(f"<a href='{auto.link}'>Ссылка</a>")

        caption = "\n\r".join(caption_lines)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Удалить", callback_data="delete"),
                ],
            ],
        )

        await self.bot.send_photo(
            chat_id=self.chat_id,
            photo=image_from_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=keyboard,
        )

        await asyncio.sleep(2)
