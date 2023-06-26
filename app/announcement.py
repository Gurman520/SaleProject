import db.announcement as db
import db.category as db_cat
from app.user import User
import router.request_class.ad as request_ad
import router.response_class.ad as response_ad
import error


def create_ad(ad: request_ad.add_new_ad, current_user: User):
    """
    Функция создания объявления
    :param ad: Класс содержащий информацию о новос объявлении
    :param current_user: Пользователь
    :return: Новое объявлние
    """
    category = db_cat.get_category_for_id(ad.category_id)
    if category is None:
        return error.ErrNotFoundCategory
    new_ad = db.create_ad(ad, current_user.id)
    print(new_ad)
    return new_ad


def get_list_ad():
    """
    Функция получения списка всех объявлений
    :return: список из классов объявление
    """
    l_ad = db.get_ad_list()
    l = list()
    for ad in l_ad:
        a = response_ad.announcement(
            id=ad.id,
            category_id=ad.category_id,
            title=ad.title,
            price=ad.price,
            description=ad.description
        )
        l.append(a)
    return l


def get_ad(ad_id: str):
    """
    Функция получения одного объявления по ID
    :param ad_id: ID объявления
    :return: объявление
    """
    ad = db.get_ad_for_id(int(ad_id))
    return ad


def delete_ad(current_user: User, ad_id: str):
    """
    Функция удаления объявления. Доступна только пользователю, который создал объявление и администратору.
    :param current_user: Пользователь
    :param ad_id: ID объявления
    :return: удаленное объявление
    """
    ad = db.get_ad_for_id(int(ad_id))
    if ad == error.ErrNotFoundAd:
        return ad
    if ad.user_id != current_user.id and not current_user.is_admin:
        return error.ErrAccessDeniedAd
    return db.delete_ad(int(ad_id))


def update_ad(id: str, ad: request_ad.update_ad, current_user: User):
    """
    Функция обновления объявления. Доступно только пользователю и администратору
    :param id: ID объявления
    :param ad: параметры, которые необходимо обновить
    :param current_user: Пользователь
    :return: обновленное объявление
    """
    category = db_cat.get_category_for_id(ad.category_id)
    if category is None:
        return error.ErrNotFoundCategory
    get_ad = db.get_ad_for_id(int(id))
    if get_ad.user_id != current_user.id and not current_user.is_admin:
        return None
    up_ad = db.update_ad(id, ad)
    return up_ad
