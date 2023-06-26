import db.comments as db
import error
from app.user import User
import router.response_class.comments as response
import router.request_class.comments as request


def get_comments_list(ad: request.Get_comments_list):
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
    return comments_list


def add_comments(new_comment: request.Add_comment, current_user: User):
    new_comm = db.create_comments(new_comment, current_user.id)
    return new_comm


def del_comments(id: str, current_user: User):
    if not current_user.is_admin:
        return error.ErrAccessDeniedComments
    del_comm = db.delete_comments(id)
    return del_comm
