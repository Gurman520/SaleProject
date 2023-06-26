from db.tables import Comments
from db.db import create_session


def get_comments_list(ad_id):
    """
    Функция получения списка комментариев
    :param ad_id: ID объявления
    :return: Список комментариев
    """
    session = create_session()
    comm = session.query(Comments).filter(Comments.ad_id == ad_id).all()
    session.close()
    return comm


def create_comments(new_comments, user_id):
    """
    Функция создания комментария
    :param new_comments: Параметры комментария
    :param user_id: ID пользователя
    :return: Комментариев
    """
    session = create_session()
    new_comm = Comments(
        text=new_comments.text,
        user_id=user_id,
        ad_id=new_comments.ad_id,
    )
    session.add(new_comm)
    session.commit()

    return session.query(Comments).filter(Comments.id == user_id).all()[0]


def delete_comments(comm_id):
    """
    Функция удаления комментария из БД
    :param comm_id: ID комментария
    :return: Удаленный комментарий
    """
    session = create_session()
    comm = session.query(Comments).filter(Comments.id == comm_id).one()
    session.delete(comm)
    session.commit()
