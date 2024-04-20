from datetime import datetime
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from services.services import total_liters, fuel_consumption_f
from keyboards.keyboard_utils import keyboard_fuel
from database.database import user_dict, FSMFillForm

fuel_router = Router()

# Этот хэндлер будет срабатывать на нажатие кнопки fuel_up
# и переводить бота в состояние ожидания ввода пробега
@fuel_router.callback_query(F.data == 'fuel_up', StateFilter(default_state))
async def process_fuel_up_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Пожалуйста, введите ваш пробег (км)\n'
                         'Ожидается целое число от 1 до 1500')
    # Устанавливаем состояние ожидания ввода пробега
    await state.set_state(FSMFillForm.mileage)


# Этот хэндлер будет срабатывать, если введен корректный пробег
# и переводить в состояние ожидания ввода цены за литр топлива
@fuel_router.message(StateFilter(FSMFillForm.mileage),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= 1500)
async def process_mileage_sent(message: Message, state: FSMContext):
    # Cохраняем введенный пробег в хранилище по ключу "mileage_km"
    await state.update_data(mileage_km=message.text)
    await message.answer(text='Спасибо!\n\nТеперь введите цену за литр топлива\n'
                         'Ожидается целое число или число с ТОЧКОЙ от 30 до 500')
    # Устанавливаем состояние ожидания ввода цены за литр топлива
    await state.set_state(FSMFillForm.price_one_liter)


# Этот хэндлер будет срабатывать, если во время ввода пробега
# будет введено что-то некорректное
@fuel_router.message(StateFilter(FSMFillForm.mileage))
async def warning_not_mileage(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на пробег\n\n'
             'Пожалуйста, введите пробег (целое число от 1 до 1500)\n\n'
             'Если вы хотите прервать заполнение данных - '
             'отправьте команду /cancel'
    )

# Этот хэндлер будет срабатывать, если введена корректная цена
# и переводить в состояние ожидания ввода суммы заправки
@fuel_router.message(StateFilter(FSMFillForm.price_one_liter),
            lambda x: x.text[0]!='.' and (all(map(lambda el: el in '0123456789', x.text.replace('.', '')))) and 30 <= float(x.text) <= 500)
async def process_price_liter_sent(message: Message, state: FSMContext):
    # Cохраняем введенную цену за 1 л в хранилище по ключу "price_liter"
    await state.update_data(price_liter=message.text)
    await message.answer(text='Спасибо!\n\nТеперь введите сумму заправки (руб)\n'
                         'Ожидается целое число или число с ТОЧКОЙ от 100 до 20 000')
    # Устанавливаем состояние ожидания ввода суммы заправки
    await state.set_state(FSMFillForm.spent_money)


# Этот хэндлер будет срабатывать, если во время ввода цены за литр
# будет введено что-то некорректное
@fuel_router.message(StateFilter(FSMFillForm.price_one_liter))
async def warning_not_price_one_liter(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на цену за литр топлива\n\n'
             'Пожалуйста, введите цену за литр топлива\n'
             'Ожидается целое число или число с ТОЧКОЙ от 30 до 500)\n\n'
             'Если вы хотите прервать заполнение данных - '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать, если введена сумма заправки
@fuel_router.message(StateFilter(FSMFillForm.spent_money),
            lambda x: x.text[0]!='.' and (all(map(lambda el: el in '0123456789', x.text.replace('.', '')))) and 100 <= float(x.text) <= 20_000)
async def process_spent_money_sent(message: Message, state: FSMContext):
    # Cохраняем введенную сумму заправки в хранилище по ключу "price_liter"
    await state.update_data(spent_money_rub=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    sum_money = user_dict[message.from_user.id]["spent_money_rub"]
    price_litr = user_dict[message.from_user.id]["price_liter"]
    # Сохраняем количество всего заправленных литров
    await state.update_data(total_liters=total_liters(sum_money, price_litr))
    user_dict[message.from_user.id] = await state.get_data()
    total_litr = user_dict[message.from_user.id]["total_liters"]
    mileage_all = user_dict[message.from_user.id]["mileage_km"]
    # Сохраняем расход топлива
    await state.update_data(fuel_consumption=fuel_consumption_f(total_litr, mileage_all))
    # Сохраняем дату и время расчетов
    await state.update_data(date_time=datetime.now().strftime('%d.%m.%Y || %H:%M:%S'))
    # Добавляем в "базу данных" анкету пользователя
    # по ключу id пользователя
    user_dict[message.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text='Спасибо!\n\n Данные внесены\n'
                         'Чтобы посмотреть результат нажмите на кнопку\n'
                         '"Результат расчетов по топливу"',
                         reply_markup=keyboard_fuel)



# Этот хэндлер будет срабатывать, если во время ввода суммы заправки
# будет введено что-то некорректное
@fuel_router.message(StateFilter(FSMFillForm.spent_money))
async def warning_not_spent_money(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на сумму заправки\n\n'
             'Пожалуйста, введите сумму заправки\n'
             'Ожидается целое число или число с ТОЧКОЙ от 100 до 20 000)\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /result
# и отправлять в чат данные расчета, либо сообщение об отсутствии данных
@fuel_router.message(F.text == 'Результат расчетов по топливу', StateFilter(default_state))
async def process_showdata_command(message: Message):
    # Отправляем пользователю расчет, если он есть в "базе данных"
    if message.from_user.id in user_dict:
            #user_dict[message.from_user.id]["mileage_km"] not in None
        await message.answer(text=
            f'Дата, время: {user_dict[message.from_user.id]["date_time"]}\n'
            f'Пробег: {user_dict[message.from_user.id]["mileage_km"]} км\n'
            f'Цена за литр: {user_dict[message.from_user.id]["price_liter"]} руб.\n'
            f'Сумма заправки: {user_dict[message.from_user.id]["spent_money_rub"]} руб.\n'
            f'Всего литров заправлено: {user_dict[message.from_user.id]["total_liters"]}\n'
            f'Расход топлива: {user_dict[message.from_user.id]["fuel_consumption"]} л/100км',
            reply_markup=ReplyKeyboardRemove()              )
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли данные. Чтобы приступить - '
            'отправьте команду /menu',
            reply_markup=ReplyKeyboardRemove()
        )