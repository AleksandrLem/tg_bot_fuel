# Вход в панель администратора
@dp.message(F.text == 'Панель Администратора', StateFilter(default_state))
async def process_admin_in(message: Message):
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Вы зашли в панель администратора',
                         reply_markup=keyboard_admin_in)
    else:
        await message.reply(text='Извините, Вы не администратор')

# Вход в панель рассылки
@dp.message(F.text == 'Сделать рассылку', StateFilter(default_state))
async def process_newsletter(message: Message):
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Меню администратора\n'
                             'Выбор рассылки сообщений',
                         reply_markup=keyboard_newsletter)
    else:
        await message.reply(text='Извините, Вы не администратор')

# Отправка рассылки по ID
@dp.message(F.text == 'Отправить выбранным', StateFilter(default_state))
async def process_newsletter(message: Message):
    if message.from_user.id == ID_ADMIN:
        await message.answer(text='Меню администратора\n'
                             'Выбор ID для рассылки',
                         reply_markup=keyboard_newsletter_only_selected)
    else:
        await message.reply(text='Извините, Вы не администратор')