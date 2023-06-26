import router.request_class.auth_class as request
from db.tables import User
from db.db import create_session


def get_user_for_email(email):
    """
    Функция получения пользователя по email
    :param email: email пользователя
    :return: Пользователь
    """
    try:
        session = create_session()
        user = session.query(User).filter(User.email == email).all()[0]
        print(user)
        session.close()
    except:
        return None
    return user


def create_user(us: request.UserCreate, h_pass: str):
    """
    Функция создания пользователя в БД
    :param us: Параметры нового пользователя
    :param h_pass: Хэшированный пароль
    :return: Пользователь
    """
    session = create_session()
    u = User(
        name=us.name,
        surname=us.surname,
        email=us.email,
        password=h_pass,
    )
    session.add(u)
    session.commit()

    return session.query(User).filter(User.email == us.email).all()[0]


def update_user_for_id(user_id):
    pass


def get_user_list():
    pass
