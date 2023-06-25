from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import Config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
import db.user as us

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
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        username: str = payload.get("sub")
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
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create(user):
    get_user = us.get_user_for_email(user.email)
    if get_user is not None:
        return None

    h_pass = get_password_hash(user.password)
    create_user = us.create_user(user, h_pass)
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": create_user.email}, expires_delta=access_token_expires)
    return token


def login(form_data):
    get_user = us.get_user_for_email(form_data.username)
    if get_user is None:
        return None
    if not verify_password(form_data.password, get_user.password):
        return 401
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": get_user.email}, expires_delta=access_token_expires)
    return token
