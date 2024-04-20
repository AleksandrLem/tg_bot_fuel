from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

other_router = Router()

# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@other_router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.reply(text='Извините, эта команда мне неизвестна')