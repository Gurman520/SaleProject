import router.request_class.ad as request_ad
from db.tables import Announcement
from db.db import create_session
import error


def get_ad_for_id(ad_id):
    """
    Функция получения объявления по ID из БД
    :param ad_id: ID объявления
    :return: Объявление
    """
    try:
        session = create_session()
        ad = session.query(Announcement).filter(Announcement.id == ad_id).all()[0]
        session.close()
    except:
        return error.ErrNotFoundAd
    return ad


def get_ad_list():
    """
    Функция получения списка объявлений из БД
    :return: Список объявления
    """
    # Добавить фильтрацию
    session = create_session()
    ad = session.query(Announcement).all()
    session.close()
    return ad


def create_ad(ad, user_id):
    """
    Функция создания объявления в БД
    :param ad: Объявление
    :param user_id: ID пользователя
    :return: Cjplfyyjt j,]zdktybt
    """
    session = create_session()
    new_ad = Announcement(
        title=ad.title,
        price=ad.price,
        description=ad.description,
        user_id=user_id,
        category_id=ad.category_id
    )
    session.add(new_ad)
    session.commit()

    return session.query(Announcement).filter(Announcement.id == new_ad.id).all()[0]


def delete_ad(ad_id):
    """
    Функция удаления объявления по ID из БД
    :param ad_id: ID объявления
    :return: Удаленное объявление
    """
    try:
        session = create_session()
        ad = session.query(Announcement).filter(Announcement.id == ad_id).one()
        session.delete(ad)
        session.commit()
    except:
        return None
    return ad


def update_ad(id: int, ad: request_ad.update_ad):
    """
    Функция обновления объявления по ID из БД
    :param id: ID объявления
    :param ad: Параметры объявления
    :return: Обновленное объявление
    """
    session = create_session()
    get_ad = session.query(Announcement).filter(Announcement.id == id).one()
    if ad.price is not None:
        get_ad.price = ad.price
    if ad.title is not None:
        get_ad.title = ad.title
    if ad.category_id is not None:
        get_ad.category_id = ad.category_id
    if ad.description is not None:
        get_ad.description = ad.description
    session.add(get_ad)
    session.commit()
    return session.query(Announcement).filter(Announcement.id == id).all()[0]
