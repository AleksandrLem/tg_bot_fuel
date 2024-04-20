import sqlite3
from aiogram.fsm.state import State, StatesGroup

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}

# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    mileage = State()        # Состояние ожидания ввода пробега
    price_one_liter = State()  # Состояние ожидания ввода цены за литр топлива
    spent_money = State()      # Состояние ожидания ввода суммы покупки топлива
    distance = State()   # Состояние ожидания ввода дистанции
    time_dist = State()  # Состояние ожидания ввода времени на дистанции




class Database:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

# метод будет проверять наличие пользователя в БД
    def users_exsists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
            "SELECT * FROM 'users_fuel' WHERE 'user_id' = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

# метод добавляет пользователя в БД
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'users_fuel' ('user_id') VALUES (?)", (user_id,)
            )
