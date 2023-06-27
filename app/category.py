import logging as log
import db.category as db
import error
from app.user import User
import router.response_class.category as response
import router.request_class.category as request


def get_category_list():
    """
    Получение списка категорий
    :return: Список из категорий (Класс - категория)
    """
    log.info("Get List Category - init")
    list_cat = db.get_categories_list()
    l_categoris = list()
    for category in list_cat:
        c = response.Category(
            id=category.id,
            name=category.name,
            description=category.description,
        )
        l_categoris.append(c)
    log.info(f"Get List Category - count Category: %s - finish", len(l_categoris))
    return l_categoris


def create_category(new_category: request.new_category, current_user: User):
    """
    Функция по добавлению категории. Доступна только админестратору
    :param new_category: новая категория
    :param current_user: Пользователь
    :return: Новая категория
    """
    log.info("Create Category - init")
    if not current_user.is_admin:
        log.error("Create Category - ErrAccessDeniedCategory")
        return error.ErrAccessDeniedCategory
    new_cat = db.create_category(new_category)
    log.info("Create Category - finish")
    return new_cat


def delete_category(id: str, current_user: User):
    """
    Функция удаления категории по ID. Доступна только админестратору.
    :param id: ID категории
    :param current_user: Пользователь
    :return: Удаленная категория
    """
    log.info("Delete category - init")
    if not current_user.is_admin:
        log.error("Delete category - ErrAccessDeniedCategory")
        return error.ErrAccessDeniedCategory
    del_cat = db.delete_category(int(id))
    if del_cat is None:
        log.error("Delete category - ErrNotFoundCategory")
        return error.ErrNotFoundCategory
    log.info("Delete category - finish")
    return del_cat
