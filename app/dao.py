from app.models import Category, Room, User
import hashlib
from app import app
def get_categories():
    return Category.query.all()


def get_products(kw, cate_id, page=None):
    products = Room.query

    if kw:
        products = products.filter(Room.name.contains(kw))

    if cate_id:
        products = products.filter(Room.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page-1)*page_size

        return products.slice(start, start+page_size)

    return products.all()


def count_product():
    return Room.query.count()

def get_user_by_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.user_name.__eq__(username), User.password.__eq__(password)).first()
