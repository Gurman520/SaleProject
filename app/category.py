import db.category as db
import error
from app.user import User
import router.response_class.category as response
import router.request_class.category as request


def get_category_list():
    list_cat = db.get_categories_list()
    l_categoris = list()
    for category in list_cat:
        c = response.category(
            id=category.id,
            name=category.name,
            description=category.description,
        )
        l_categoris.append(c)
    return l_categoris


def create_category(new_category: request.new_category, current_user: User):
    if not current_user.is_admin:
        return error.ErrAccessDeniedCategory
    new_cat = db.create_category(new_category)
    return new_cat


def delete_category(id: str, current_user: User):
    if not current_user.is_admin:
        return error.ErrAccessDeniedCategory
    del_cat = db.delete_category(int(id))
    if del_cat is None:
        return error.ErrNotFoundCategory
    return del_cat
