from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)
from keyboards.keyboard_utils import keyboard_admin
from config_data.config import Config, load_config


config: Config = load_config()
ID_ADMIN: int = config.tg_bot.admin_ids[0]
command_router = Router()

# Этот хэндлер будет срабатывать на команду "/help"
@command_router.callback_query(F.data == 'help', StateFilter(default_state))
async def process_help_button(callback: CallbackQuery):
    await callback.message.delete()
    # Создаем объекты инлайн-кнопок
    fuel_button = InlineKeyboardButton(
        text='Расчеты по топливу',
        callback_data='fuel_up'
    )

    speed_button = InlineKeyboardButton(
        text='Расчет средней скорости',
        callback_data='speed_up'
    )

    # Добавляем кнопки в клавиатуру (в одном ряду одна кнопка)
    keyboard: list[list[InlineKeyboardButton]] = [
        [fuel_button],
        [speed_button]
    ]

    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Отправляем пользователю сообщение с клавиатурой
    await callback.message.answer(text=
        'Этот бот делает расчет расхода топлива или средней скорости\n\n'
        'На ввод принимаются ЦЕЛЫЕ числа либо числа с ТОЧКОЙ\n'
        'Для расчетов по топливу будут нужны следующие данные:\n\n'
        ' - Пробег;\n'
        ' - Цена за 1 литр топлива;\n'
        ' - Сумма заправки;\n\n'
        'Итоги расчетов по топливу будут предоставлены примерно в таком виде:\n\n'
        'Пробег: 321 км\n'
        'Цена за 1 литр топлива: 53.3 руб.\n'
        'Сумма заправки: 1050.5 руб.\n'
        'Всего литров заправлено: 19.71\n'
        'Расход топлива: 6.14 л/100км\n\n'
        'Данные вводятся пошагово, а в итоге\n'
        'выводятся результаты расчетов\n\n'
        'Пожалуйста, при вводе данных следуйте указаниям инструкции на'
        ' каждом шаге!\n'
        'Для расчета средней скорости будут нужны следующие данные\n\n'
        ' - Дистанция в километрах (целое число или число с ТОЧКОЙ)\n'
        ' - Время на дистанции в минутах (целое число)\n\n'
        'Выберите действие',
        reply_markup=markup
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на команду /start вне состояний
# и предлагать перейти к заполнению анкеты, отправив команду /calculation
@command_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    # Создаем объекты инлайн-кнопок
    fuel_button = InlineKeyboardButton(
        text='Расчеты по топливу',
        callback_data='fuel_up'
    )

    speed_button = InlineKeyboardButton(
        text='Расчет средней скорости',
        callback_data='speed_up'
    )

    help_button = InlineKeyboardButton(
        text='Справка',
        callback_data='help'
    )

    # Добавляем кнопки в клавиатуру (в одном ряду одна кнопка)
    keyboard: list[list[InlineKeyboardButton]] = [
        [fuel_button],
        [speed_button],
        [help_button]
    ]

    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    await message.answer(
        text='Этот бот может сделать расчет расхода топлива или средней скорости\n\n'
    )
    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Выберите действие',
        reply_markup=markup
    )

# Этот хэндлер будет срабатывать на команду /menu вне состояний
@command_router.message(Command(commands='menu'), StateFilter(default_state))
async def process_start_command(message: Message):
    # Создаем объекты инлайн-кнопок
    fuel_button = InlineKeyboardButton(
        text='Расчеты по топливу',
        callback_data='fuel_up'
    )

    speed_button = InlineKeyboardButton(
        text='Расчет средней скорости',
        callback_data='speed_up'
    )

    help_button = InlineKeyboardButton(
        text='Справка',
        callback_data='help'
    )

    # Добавляем кнопки в клавиатуру (в одном ряду одна кнопка)
    keyboard: list[list[InlineKeyboardButton]] = [
        [fuel_button],
        [speed_button],
        [help_button]
    ]

    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # Отправляем пользователю сообщение с клавиатурой
    await message.answer(
        text='Выберите действие',
        reply_markup=markup
    )
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Вы администратор',
                         reply_markup=keyboard_admin)


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@command_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Сейчас расчет не ведется\n\n'
            'Чтобы перейти к расчетам - \n'
            'перейдите в главное меню /menu'
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
# знак тильда ~ означает - всё кроме данного выражения, т.е.
# ~StateFilter(default_state) означает срабатывать всегда, кроме
# тех случаев, когда StateFilter отключен
@command_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы прервали проведение расчетов\n\n'
            'Чтобы возобновить расчеты - \n'
            'перейдите в главное меню /menu'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()