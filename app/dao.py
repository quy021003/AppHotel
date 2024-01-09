from sqlalchemy.sql.operators import is_

from app.models import Category, Room, User, Invoice, Booking, Facility, Customer, Images
import hashlib, requests
from app import app, db
from flask import request, render_template, redirect, jsonify, session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, VARCHAR, DATETIME, Enum, DateTime
from flask_login import current_user
from sqlalchemy import func
def get_categories():
    return Category.query.all()

def get_id_invoice_last():
    return Invoice.query.get(Invoice.id).last()

def query_single_room(page=None):
    s_room = Room.query.filter(Room.category_id == 1)
    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size

        return s_room.slice(start, start + page_size)

    return s_room.all()


def get_products(kw, cate_id, page=None):
    products = Room.query

    if kw:
        products = products.filter(Room.name.contains(kw))

    if cate_id:
        products = products.filter(Room.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size

        return products.slice(start, start + page_size)

    return products.all()


def count_single_room():
    return Room.query.filter(Room.category_id == 1).count()


def count_product():
    return Room.query.count()


def get_user_by_id(user_id):
    return User.query.get(user_id)



def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    return User.query.filter(User.user_name.__eq__(username), User.password.__eq__(password)).first()


def add_receipt(cart):

     un = session.get('us_name')
     up = session.get('us_phone')
     ui = session.get('us_id')
     if cart:

        a = Customer(cert=ui, phone=up, name=un)
        db.session.add(a)
        i = Invoice(user=current_user, customer=a)
        db.session.add(i)

        for c in cart.values():
            d = Booking(start=c['start'], end=c['end'], price=c['price'], invoice=i, room_id=c['id'])
            db.session.add(d)

        db.session.commit()
        return True


     return False

def count_rooms_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Room.id))\
        .join(Room, Room.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.name).all()

def get_revenue_on_room(kw=None):
    query = db.session.query(Room.id, Room.name, func.sum(Booking.price))\
        .join(Booking, Booking.room_id.__eq__(Room.id))

    if kw:
        query = query.filter(Room.name.contains(kw))

    return query.group_by(Room.id).all()


def count_customer_by_room():
    return db.session.query(Room.id, Room.name,func.sum(Booking.room_id))\
                    .join(Booking, Booking.room_id.__eq__(Room.id), isouter=True)\
                    .group_by(Room.id).all()


def get_revenue_by_month(year=2024):
    return db.session.query(func.extract('month', Invoice.release), func.sum(Booking.price))\
        .join(Booking, Booking.invoice_id.__eq__(Invoice.id))\
        .filter(func.extract('year', Invoice.release).__eq__(year))\
        .group_by(func.extract('month', Invoice.release)).all()
# func.extract('month', A): Trả về các giá trị tháng trong trường A


def add_staff(name, username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())

    u = User(name=name, user_name=username, password=password)
    db.session.add(u)
    db.session.commit()


def get_room_by_id(id):
    return Room.query.get(id)


def get_img_by_id(id):
    return db.session.query(Images).join(Room).filter(Room.id.__eq__(id))



def get_facilities_by_id(id):
    return db.session.query(Facility).join(Room).filter(Room.id.__eq__(id))


def count_img_by_id(id):
    return db.session.query(Images).join(Room).filter(Room.id.__eq__(id)).count()


def get_imgs(id, page=None):
    imgs = get_img_by_id(id)

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE_DETAILS"]
        start = (page - 1) * page_size

        return imgs.slice(start, start + page_size)

    return imgs.all()

if __name__ == '__main__':
    with app.app_context():
        print(count_customer_by_room())
