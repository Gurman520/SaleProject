from db.tables import Category
from db.db import create_session


def get_category_for_id(id):
    try:
        session = create_session()
        category = session.query(Category).filter(Category.id == id).all()[0]
        session.close()
    except:
        return None
    return category


def get_categories_list():
    session = create_session()
    categories = session.query(Category).all()
    session.close()
    return categories


def create_category(new_category):
    session = create_session()
    new_cat = Category(
        name=new_category.name,
        description=new_category.description,
    )
    session.add(new_cat)
    session.commit()

    return session.query(Category).filter(Category.name == new_category.name).all()[0]


def delete_category(id):
    try:
        session = create_session()
        category = session.query(Category).filter(Category.id == id).one()
        session.delete(category)
        session.commit()
    except:
        return None
    return category