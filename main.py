from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu
from handlers.other_handlers import other_router
from handlers.admin_handlers import admin_routers
from handlers.command_handlers import command_router
from handlers.fuel_handlers import fuel_router
from handlers.speed_handlers import speed_router


config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ID_ADMIN: int = config.tg_bot.admin_ids[0]

# Инициализируем Redis
redis = Redis(host='localhost')

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = RedisStorage(redis=redis)

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Подключаем роутеры
dp.include_routers(command_router, fuel_router, speed_router,
                   admin_routers, other_router
                   )


# Регистрируем асинхронную функцию в диспетчере,
# которая будет выполняться на старте бота
dp.startup.register(set_main_menu)


# Хендлеры с командами

# Хендлеры с вводом данных по топливу и вывод итога расчета

# Хендлеры с вводом данных по средней скорости и вывод итога расчета

# Хендлеры панели администратора

# Хендлер, который срабатывает на неизвестные команды other handler



# Запускаем поллинг
if __name__ == '__main__':
    dp.run_polling(bot)