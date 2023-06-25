import db.announcement as db
from app.user import User
import router.request_class.ad as request_ad
import router.response_class.ad as response_ad


def create_ad(ad: request_ad.add_new_ad, current_user: User):
    new_ad = db.create_ad(ad, current_user.id, 1)
    print(new_ad)
    return new_ad


def get_list_ad(current_user: User):
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
    ad = db.get_ad_for_id(int(ad_id))
    return ad


def delete_ad(current_user: User, ad_id: str):
    ad = db.get_ad_for_id(int(ad_id))
    if ad.user_id != current_user.id:
        return None
    return db.delete_ad(int(ad_id))


def update_ad():
    pass
