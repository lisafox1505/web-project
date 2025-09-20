from sqlalchemy import Column, Integer, Text, create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///users_data.sqlite")
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True)
    password = Column(Text)
    email = Column(Text, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def register(self):
        try:
            session.add(self)
            session.commit()
            print(f"Користувач {self.username} зареєстрован!")
        except Exception as error:
            print("Помилка:", error)

    def login(self, username, password):
        user = session.query(User).filter_by(username=username, password=password).first()
        if user:
            return True
        else:
            return False

Base.metadata.create_all(engine)

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
        user_verify = session.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first()

        if user_verify:
            print("Ви вже зареєстровані! Виберіть 'Увійти'!")
        else:
            new_user = User(username, password, email)
            new_user.register()

    elif your_choice == "увійти":
        username = input("Введіть ім'я:\n")
        password = input("Введіть пароль:\n")
        user_data = User("", "", "")
        if user_data.login(username, password):
            print(f"Вхід успішний! Ласкаво просимо {username}!")
        else:
            print("Невірний логін або пароль")
    elif your_choice == "вийти":
        print("Вихід з програми")
        break
    else:
        print("Спробуйте ще раз!")

print(session.query(User).all())