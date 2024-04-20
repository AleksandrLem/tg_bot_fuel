from datetime import datetime
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from services.services import average_speed
from database.database import user_dict, FSMFillForm
from keyboards.keyboard_utils import keyboard_speed

speed_router = Router()


# Этот хэндлер будет срабатывать на кнопку speed_up
# и переводить бота в состояние ожидания ввода времени на дистанции
@speed_router.callback_query(F.data == 'speed_up', StateFilter(default_state))
async def process_help_button(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Пожалуйста, введите Ваше время\n'
                         'на дистанции в минутах\n'
                         'Ожидается целое число от 1 до 6000')
    # Устанавливаем состояние ожидания ввода дистанции
    await state.set_state(FSMFillForm.time_dist)


# Этот хэндлер будет срабатывать, если введено корректоное время
# и переводить в состояние ожидания ввода дистанции
@speed_router.message(StateFilter(FSMFillForm.time_dist),
            lambda x: x.text.isdigit() and 1 <= int(x.text) <= 6000)
async def process_distance_sent(message: Message, state: FSMContext):
    # Cохраняем введенное время в хранилище по ключу "time_dist_min"
    await state.update_data(time_dist_min=message.text)
    await message.answer(text='Спасибо!\n\nТеперь введите дистанцию в км\n'
                         'Ожидается целое число или число с ТОЧКОЙ от 1 до 3000')
    # Устанавливаем состояние ожидания ввода дистанции
    await state.set_state(FSMFillForm.distance)

# Этот хэндлер будет срабатывать, если во время ввода времени
# будет введено что-то некорректное
@speed_router.message(StateFilter(FSMFillForm.time_dist))
async def warning_not_time(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на время в минутах\n\n'
             'Пожалуйста, введите время в минутах (целое число от 1 до 6000)\n\n'
             'Если вы хотите прервать заполнение данных - '
             'отправьте команду /cancel'
    )

# Этот хэндлер будет срабатывать, если корректно введена дистанция
@speed_router.message(StateFilter(FSMFillForm.distance),
            lambda x: x.text[0]!='.' and (all(map(lambda el: el in '0123456789', x.text.replace('.', '')))) and 1 <= float(x.text) <= 3000)
async def process_dist_ok_sent(message: Message, state: FSMContext):
    # Cохраняем введенную дистанцию в хранилище по ключу "dist_km"
    await state.update_data(dist_km=message.text)
    # Сохраняем в базу данных все введнные данные
    user_dict[message.from_user.id] = await state.get_data()
    # достаем из БД дистанцию и вермя на дистанции
    dist_time = user_dict[message.from_user.id]["dist_km"]
    time_dist = user_dict[message.from_user.id]["time_dist_min"]
    # Сохраняем среднюю скорость
    await state.update_data(speed_total=average_speed(time_dist, dist_time))
    # Сохраняем дату и время расчетов
    await state.update_data(date_time_sp=datetime.now().strftime('%d.%m.%Y || %H:%M:%S'))
    # Ещё раз сохраняем в базу данных все данные с расчетами ср.скорости
    user_dict[message.from_user.id] = await state.get_data()
    # Завершаем машину состояний
    await state.clear()
    await message.answer(text='Спасибо!\n\n Данные внесены\n'
                         'Чтобы посмотреть результат нажмите на кнопку',
                         reply_markup=keyboard_speed)


# Этот хэндлер будет срабатывать, если во время ввода дистанции
# будет введено что-то некорректное
@speed_router.message(StateFilter(FSMFillForm.distance))
async def warning_not_spent_money(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на дистанцию в км\n\n'
             'Пожалуйста, введите ещё раз дистанцию в км\n'
             'Ожидается целое число или число с ТОЧКОЙ от 100 до 20 000)\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel')


# Этот хэндлер будет срабатывать на отправку команды /result_speed
# и отправлять в чат данные расчета, либо сообщение об отсутствии данных
@speed_router.message(F.text == 'Средняя скорость', StateFilter(default_state))
async def process_result_speed_command(message: Message):
    # Отправляем пользователю расчет, если он есть в "базе данных"
    if message.from_user.id in user_dict:
        await message.answer(text=
            f'Дата, время: {user_dict[message.from_user.id]["date_time_sp"]}\n'
            f'Средняя скорость: {user_dict[message.from_user.id]["speed_total"]} км/ч\n',
            reply_markup=ReplyKeyboardRemove()
                           )
    else:
        # Если анкеты пользователя в базе нет - предлагаем заполнить
        await message.answer(
            text='Вы еще не заполняли данные. Чтобы приступить - '
            'отправьте команду /menu',
            reply_markup=ReplyKeyboardRemove()
        )