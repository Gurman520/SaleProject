import router.request_class.auth_class as request
from db.tables import Announcement
from db.db import create_session


def get_ad_for_id(ad_id):
    try:
        session = create_session()
        ad = session.query(Announcement).filter(Announcement.id == ad_id).all()[0]
        session.close()
    except:
        return None
    return ad


def get_ad_list():
    # Добавить фильтрацию
    session = create_session()
    ad = session.query(Announcement).all()
    session.close()
    return ad


def create_ad(ad, user_id, category_id):
    session = create_session()
    new_ad = Announcement(
        title=ad.title,
        price=ad.price,
        description=ad.description,
        user_id=user_id,
        category_id=category_id
    )
    session.add(new_ad)
    session.commit()

    return session.query(Announcement).filter(Announcement.id == new_ad.id).all()[0]


def delete_ad(ad_id):
    try:
        session = create_session()
        ad = session.query(Announcement).filter(Announcement.id == ad_id).one()
        session.delete(ad)
        session.commit()
    except:
        return None
    return ad


# Дописать структуру для обновления
def update_ad(ad_id):
    pass
