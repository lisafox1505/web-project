import sqlite3

class User:
    def __init__(self):
        self.connection = sqlite3.connect("users_data_sql3.db")
        self.cursor = self.connection.cursor()
        self.query_create_table = """
            create table if not exists users (
            id integer primary key autoincrement,
            username text not null unique,
            password text not null,
            email text not null unique
        );
        """
        self.cursor.execute(self.query_create_table)
        self.connection.commit()

    def register(self, username, password, email):
        self.cursor.execute("select * from users where username=?", (username,))
        user_verify_username = self.cursor.fetchone()
        self.cursor.execute("select * from users where email=?", (email,))
        user_verify_email = self.cursor.fetchone()
        if user_verify_username and user_verify_email:
            print("Такі логін та email існують! Виберіть 'Увійти'!")
            return
        if user_verify_username:
            print("Таке ім'я вже існує! Виберіть 'Увійти'!")
            return
        if user_verify_email:
            print("Такий email вже існує! Виберіть 'Увійти'!")
            return

        self.cursor.execute("insert into users (username, password, email) values(?, ?, ?)",
                                (username, password, email))
        self.connection.commit()
        print(f"Користувач {username} зареєстрован!")

    def login(self, username, password):
        self.cursor.execute("select * from users where username=? and password=?", (username, password))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False
    def close(self):
        self.connection.close()

user_system = User()
while True:
    print("Зареєструватися")
    print("Увійти")
    print("Вийти")

    your_choice = input("Виберіть дію:\n")
    your_choice = your_choice.strip().lower()

    if your_choice == "зареєструватися":
        username = input("Введіть ім'я:\n")
        password = input("Введіть пароль:\n")
        email = input("Введіть email:\n")
        user_system.register(username, password, email)

    elif your_choice == "увійти":
        username = input("Введіть ім'я:\n")
        password = input("Введіть пароль:\n")
        if user_system.login(username, password):
            print(f"Вхід успішний! Ласкаво просимо {username}!")
        else:
            print("Невірний логін або пароль")
    elif your_choice == "вийти":
        print("Вихід з програми")
        user_system.close()
        break
    else:
        print("Спробуйте ще раз!")
