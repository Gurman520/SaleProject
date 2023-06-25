from db.tables import Comments
from db.db import create_session


def get_comments_list(ad_id):
    session = create_session()
    comm = session.query(Comments).filter(Comments.ad_id == ad_id).all()
    session.close()
    return comm
