import sqlite3

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
