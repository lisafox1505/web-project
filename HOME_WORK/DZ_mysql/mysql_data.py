import mysql.connector
from mysql.connector.errors import IntegrityError

DB_CONFIG = {
"host": "localhost",
"user": "root",
"password": "--мій пароль--"
}

DB_NAME = "users_db"

def connect_to_db(config, db_name=None):
    try:
        if db_name:
            config["database"] = db_name
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_database_and_tables():
    try:
        conn = connect_to_db(DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"Create database if not exists {DB_NAME};")
        cursor.execute(f'use {DB_NAME};')
        cursor.execute("""
                Create table if not exists users(
                    id INT auto_increment primary key,
                    username varchar(255) unique,
                    password varchar(255) not null,
                    email varchar(255) unique
                );
            """)
        conn.commit()
        cursor.close()
        conn.close()
        print("База даних та таблиця створені.")
    except mysql.connector.Error as e:
        print(f"Помилка: {e}")

def create_tables_sites():
    try:
        conn = connect_to_db(DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(f"use {DB_NAME};")
        cursor.execute("""
                Create table if not exists sites(
                    id INT auto_increment primary key,
                    site_name varchar(255) not null,
                    site_login varchar(255) not null,
                    site_password varchar(255) not null,
                    login_type varchar(255) not null,
                    user_id integer,
                    foreign key (user_id) references users(id)      
                );
            """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Таблиця створена.")
    except mysql.connector.Error as e:
        print(f"Помилка: {e}")

class User:
    def __init__(self):
        self.mydb = connect_to_db(DB_CONFIG, DB_NAME)
        self.cursor = self.mydb.cursor()

    def register(self, username, password, email):
        try:
            self.cursor.execute(
                "insert into users (username, password, email) values(%s, %s, %s)",
                (username, password, email)
            )
            self.mydb.commit()
            print(f"Користувач {username} зареєстрован!")
        except IntegrityError as e:
            print(f"Помилка: {e}")

    def login(self, username, password):
        self.cursor.execute(
            "select * from users where username=%s and password=%s",
            (username, password)
        )
        user = self.cursor.fetchone()
        if user:
            return user[0]
        else:
            return False

    def close(self):
        if self.mydb and self.mydb.is_connected():
            self.cursor.close()
            self.mydb.close()
            print("Connection closed")

class SiteInfo:
    def __init__(self):
        self.mydb = connect_to_db(DB_CONFIG, DB_NAME)
        self.cursor = self.mydb.cursor()

    def add_sites(self, user_id, site_name, site_login, site_password, login_type):
        self.cursor.execute(
            "select * from sites where user_id=%s and site_name=%s and login_type=%s",
            (user_id, site_name, login_type)
        )
        found_value = self.cursor.fetchone()
        if found_value:
            print("Цей сайт вже збережен!")
            return

        self.cursor.execute(
            "insert into sites (user_id, site_name, site_login, site_password, login_type) values(%s, %s, %s, %s, %s)",
            (user_id, site_name, site_login, site_password, login_type)
        )
        self.mydb.commit()
        print("Інформація про сайт збережена!")

    def open_info_about_site(self, user_id):
        self.cursor.execute(
            "select site_name, site_login, login_type from sites where user_id=%s",
            (user_id, )
        )
        found_info = self.cursor.fetchall()
        if found_info:
            for site in found_info:
                print(f"Сайт: {site[0]}, Логін: {site[1]}, Тип входу: {site[2]}")
        else:
            print("Немає збережених сайтів!")

    def close(self):
        if self.mydb and self.mydb.is_connected():
            self.cursor.close()
            self.mydb.close()
            print("Connection closed")

if __name__ == "__main__":
    create_database_and_tables()
    create_tables_sites()

user_system = User()
user_menu = SiteInfo()
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
        user_id = user_system.login(username, password)
        if user_id:
            print(f"Вхід успішний! Ласкаво просимо {username}!")
            while True:
                print("Мої сайти")
                print("Додати сайт")
                print("Вийти")
                your_choice_menu = input("Виберіть дію:\n")
                your_choice_menu = your_choice_menu.strip().lower()
                if your_choice_menu == "мої сайти":
                    user_menu.open_info_about_site(user_id)
                elif your_choice_menu == "додати сайт":
                    site_name = input("Назва сайту:\n")
                    site_login = input("Логін:\n")
                    site_password = input("Пароль:\n")
                    login_type = input("Тип входу:\n")
                    user_menu.add_sites(user_id, site_name, site_login, site_password, login_type)
                elif your_choice_menu == "вийти":
                    print("Вихід з акаунта")
                    break
                else:
                    print("Невірний вибір")
        else:
            print("Невірний логін або пароль")
    elif your_choice == "вийти":
        print("Вихід з програми")
        user_system.close()
        user_menu.close()
        break
    else:
        print("Спробуйте ще раз!")

