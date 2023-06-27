import router.request_class.auth_class as request
from db.tables import User
from db.init_db import create_session


def get_user_for_email(email):
    """
    Функция получения пользователя по email
    :param email: email пользователя
    :return: Пользователь
    """
    try:
        session = create_session()
        user = session.query(User).filter(User.email == email).all()[0]
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


def update_user_for_id(id, up_user):
    session = create_session()
    get_user = session.query(User).filter(User.id == id).one()
    if up_user.name is not None:
        get_user.name = up_user.name
    if up_user.surname is not None:
        get_user.surname = up_user.surname
    if up_user.email is not None:
        get_user.email = up_user.email
    session.add(get_user)
    session.commit()
    return session.query(User).filter(User.id == id).all()[0]


def update_user_for_id_admin(id, up_user):
    session = create_session()
    get_user = session.query(User).filter(User.id == id).one()
    if up_user.is_admin is not None:
        get_user.is_admin = up_user.is_admin
    if up_user.is_active is not None:
        get_user.is_active = up_user.is_active
    session.add(get_user)
    session.commit()
    return session.query(User).filter(User.id == id).all()[0]


def get_user_list():
    session = create_session()
    user = session.query(User).all()[0]
    session.close()
    return user


def get_user_for_id(id):
    try:
        session = create_session()
        user = session.query(User).filter(User.id == id).all()[0]
        session.close()
    except:
        return None
    return user
