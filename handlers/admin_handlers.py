from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message
from config_data.config import Config, load_config
from keyboards.keyboard_utils import (keyboard_admin_in,
                                      keyboard_newsletter,
                                      keyboard_newsletter_only_selected)

config: Config = load_config()
ID_ADMIN: int = config.tg_bot.admin_ids[0]
admin_routers = Router()



# Вход в панель администратора
@admin_routers.message(F.text == 'Панель Администратора', StateFilter(default_state))
async def process_admin_in(message: Message):
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Вы зашли в панель администратора',
                         reply_markup=keyboard_admin_in)
    else:
        await message.reply(text='Извините, Вы не администратор')

# Вход в панель рассылки
@admin_routers.message(F.text == 'Сделать рассылку', StateFilter(default_state))
async def process_newsletter(message: Message):
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Меню администратора\n'
                             'Выбор рассылки сообщений',
                         reply_markup=keyboard_newsletter)
    else:
        await message.reply(text='Извините, Вы не администратор')

# Отправка рассылки по ID
@admin_routers.message(F.text == 'Отправить выбранным', StateFilter(default_state))
async def process_newsletter(message: Message):
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Меню администратора\n'
                             'Выбор ID для рассылки',
                         reply_markup=keyboard_newsletter_only_selected)
    else:
        await message.reply(text='Извините, Вы не администратор')