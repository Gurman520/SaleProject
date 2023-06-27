import logging as log
from datetime import datetime, timedelta
from jose import JWTError, jwt
import error
from config import Config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import db.user as us
import router.response_class.user as response
import router.request_class.user as request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    is_admin: bool
    is_active: bool


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Функция создания токена доступа.
    :param data: Словарь с данными о пользователе
    :param expires_delta: Время жизни токена
    :return: Токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Функция проверки валидности токена доступа
    :param token: Токен
    :return: Пользователь
    """
    # Добавить проверку времени токена
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
        time = payload.get("exp")
        time = datetime.utcfromtimestamp(time)
        now_t = datetime.utcnow()
        if time < now_t:
            raise credentials_exception
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = us.get_user_for_email(username)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is baned",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_password_hash(password):
    """
    Функция хэширования пароля при регистрации
    :param password: Текст пароля
    :return: Хэшированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Функция проверки ввденного пароля и хэшированного из БД
    :param plain_password: Введенный пароль
    :param hashed_password: Хэшированный пароль
    :return:True | False
    """
    return pwd_context.verify(plain_password, hashed_password)


def create(user):
    """
    Функция создания пользователя в системе и получения Токена
    :param user: Информация о пользователе
    :return: Токен
    """
    get_user = us.get_user_for_email(user.email)
    if get_user is not None:
        return None

    h_pass = get_password_hash(user.password)
    create_user = us.create_user(user, h_pass)
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": create_user.email}, expires_delta=access_token_expires)
    return token


def login(form_data):
    """
    Функция получения токена пользователя по Login и Password
    :param form_data: Информация с формы заполнения
    :return: Токен
    """
    get_user = us.get_user_for_email(form_data.username)
    if get_user is None:
        return None
    if not verify_password(form_data.password, get_user.password):
        return 401
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": get_user.email}, expires_delta=access_token_expires)
    return token


def get_user_list(current_user: User):
    list_user = us.get_user_list()
    l_user = list()
    if current_user.is_admin:
        for user in list_user:
            u = response.User(
                id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_admin=user.is_admin,
                is_active=user.is_active,
            )
            l_user.append(u)
    else:
        for user in list_user:
            u = response.User(
                id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
            )
            l_user.append(u)
    return l_user


def get_user_for_id(id: str, current_user: User):
    user = us.get_user_for_id(int(id))
    if user is None:
        return error.ErrNotFoundUser
    return user


def update_user(id: str, update_user: request.update_user, current_user: User):
    user = us.get_user_for_id(int(id))
    if user is None:
        return error.ErrNotFoundUser
    if user.id != current_user.id and not current_user.is_admin:
        log.error("Update User - ErrAccessDeniedUser")
        return error.ErrAccessDeniedUser
    if current_user.is_admin:
        user = us.update_user_for_id_admin(int(id), update_user)
    user = us.update_user_for_id(int(id), update_user)
    log.info("Update User - finish")
    return user
