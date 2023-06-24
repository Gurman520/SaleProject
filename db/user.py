import router.request_class.auth_class as request
from db.tables import User
from db.db import create_session


def get_user_for_email(email):
    session = create_session()
    user = session.query(User).filter(User.email == email).all()[0]
    session.close()
    return user


def create_user(us: request.UserCreate, h_pass: str):
    session = create_session()
    print(session)
    u = User(
        name=us.name,
        surname=us.surname,
        email=us.email,
        password=h_pass,
    )
    session.add(u)
    session.commit()

    return session.query(User).filter(User.email == us.email).all()[0]
