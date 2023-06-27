import logging as log
import db.comments as db
from db.announcement import get_ad_for_id
import error
from app.user import User
import router.response_class.comments as response
import router.request_class.comments as request


def get_comments_list(ad: request.Get_comments_list):
    """
    Функция получения списка комментариев по ID объявления
    :param ad: Класс содержащий информацию для получения списка
    :return: Список комментариев (Класс - комментарий)
    """
    log.info("Get List Comments - init")
    comments = db.get_comments_list(int(ad.announcement_id))
    comments_list = list()
    for comment in comments:
        comm = response.Comment(
            id=comment.id,
            text=comment.text,
            user_id=comment.user_id,
            ad_id=comment.ad_id,
        )
        comments_list.append(comm)
    log.info(f"Get List Comments - Get Comments: %s", len(comments_list))
    return comments_list


def add_comments(new_comment: request.Add_comment, current_user: User):
    """
    Функция добавления комментария
    :param new_comment: Новый комментарий
    :param current_user: Пользователь
    :return: Новый комментарий
    """
    log.info("Add Comments - init")
    ad = get_ad_for_id(new_comment.ad_id)
    if ad == error.ErrNotFoundAd:
        log.error("Add Comments - ErrNotFoundAd")
        return error.ErrNotFoundAd
    new_comm = db.create_comments(new_comment, current_user.id)
    log.info("Add Comments - finish")
    return new_comm


def del_comments(id: str, current_user: User):
    """
    Функция удаления комментария. Доступна только админестратору.
    :param id: ID комментария
    :param current_user: Пользователь
    :return: Удаленный комментарий
    """
    log.info("Delete Comments - init")
    if not current_user.is_admin:
        log.error("Delete Comments - ErrAccessDeniedComments")
        return error.ErrAccessDeniedComments
    del_comm = db.delete_comments(id)
    log.info("Delete Comments - finish")
    return del_comm
