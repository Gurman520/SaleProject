import logging as log
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
    log.info("Create AD - init")
    category = db_cat.get_category_for_id(ad.category_id)
    if category is None:
        log.error("Create AD - ErrNotFoundCategory")
        return error.ErrNotFoundCategory
    new_ad = db.create_ad(ad, current_user.id)
    log.info("Create AD - finish")
    return new_ad


def get_list_ad():
    """
    Функция получения списка всех объявлений
    :return: список из классов объявление
    """
    log.info("Get List AD - init")
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
    log.info(f"Get List AD - count AD: %s - finish", len(l))
    return l


def get_ad(ad_id: str):
    """
    Функция получения одного объявления по ID
    :param ad_id: ID объявления
    :return: объявление
    """
    log.info("Get AD for ID - init")
    ad = db.get_ad_for_id(int(ad_id))
    if ad == error.ErrNotFoundAd:
        log.error("Get AD for ID - ErrNotFoundAd")
    else:
        log.info("Get AD for ID - finish")
    return ad


def delete_ad(current_user: User, ad_id: str):
    """
    Функция удаления объявления. Доступна только пользователю, который создал объявление и администратору.
    :param current_user: Пользователь
    :param ad_id: ID объявления
    :return: удаленное объявление
    """
    log.info("Delete AD - init")
    ad = db.get_ad_for_id(int(ad_id))
    if ad == error.ErrNotFoundAd:
        log.error("Delete AD - ErrNotFoundAd")
        return ad
    if ad.user_id != current_user.id and not current_user.is_admin:
        log.error("Delete AD - ErrAccessDeniedAd")
        return error.ErrAccessDeniedAd
    log.info("Delete AD - finish")
    return db.delete_ad(int(ad_id))


def update_ad(id: str, ad: request_ad.update_ad, current_user: User):
    """
    Функция обновления объявления. Доступно только пользователю и администратору
    :param id: ID объявления
    :param ad: параметры, которые необходимо обновить
    :param current_user: Пользователь
    :return: обновленное объявление
    """
    log.info("Update AD - init")
    if ad.category_id is not None:
        category = db_cat.get_category_for_id(ad.category_id)
        if category is None:
            log.error("Update AD - ErrNotFoundCategory")
            return error.ErrNotFoundCategory
    get_ad = db.get_ad_for_id(int(id))
    if get_ad.user_id != current_user.id and not current_user.is_admin:
        log.error("Update AD - ErrAccessDeniedAd")
        return error.ErrAccessDeniedAd
    up_ad = db.update_ad(int(id), ad)
    log.info("Update AD - finish")
    return up_ad
