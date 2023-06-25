import db.comments as db
from app.user import User
import router.response_class.comments as response
import router.request_class.comments as request


def get_comments_list(id: str):
    comments = db.get_comments_list(int(id))
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
    pass


def del_comments(id: str, current_user: User):
    pass
