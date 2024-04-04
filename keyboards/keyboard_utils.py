from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Создаем объекты кнопок
button_fuel = KeyboardButton(text='Результат расчетов по топливу')
button_speed = KeyboardButton(text='Средняя скорость')
button_admin = KeyboardButton(text='Панель Администратора')
button_id = KeyboardButton(text='ID пользователей')
button_newsletter = KeyboardButton(text='Сделать рассылку')
button_newsletter_all = KeyboardButton(text='Отправить всем')
button_newsletter_only_selected = KeyboardButton(text='Отправить выбранным')
button_history_id = KeyboardButton(text='История сообщений по ID')
button_select_id = KeyboardButton(text='Выбрать по ID')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard_fuel = ReplyKeyboardMarkup(keyboard=[[button_fuel]], resize_keyboard=True)
keyboard_speed = ReplyKeyboardMarkup(keyboard=[[button_speed]], resize_keyboard=True)
keyboard_admin = ReplyKeyboardMarkup(keyboard=[[button_admin]], resize_keyboard=True)
keyboard_admin_in = ReplyKeyboardMarkup(keyboard=[[button_id],
                                                  [button_newsletter],
                                                  [button_history_id]],
                                                  resize_keyboard=True)
keyboard_newsletter = ReplyKeyboardMarkup(keyboard=[[button_newsletter_all],
                                                    [button_newsletter_only_selected]],
                                                    resize_keyboard=True)
keyboard_newsletter_only_selected = ReplyKeyboardMarkup(keyboard=[[button_select_id]],
                                                        resize_keyboard=True)