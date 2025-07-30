from aiogram.types import CallbackQuery


async def delete_post(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await callback.bot.delete_message(chat_id=chat_id, message_id=message_id)
