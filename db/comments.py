from db.tables import Comments
from db.db import create_session


def get_comments_list(ad_id):
    session = create_session()
    comm = session.query(Comments).filter(Comments.ad_id == ad_id).all()
    session.close()
    return comm


def create_comments(new_comments, user_id):
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
    session = create_session()
    comm = session.query(Comments).filter(Comments.id == comm_id).one()
    session.delete(comm)
    session.commit()
