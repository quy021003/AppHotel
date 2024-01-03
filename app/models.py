import hashlib

from app import app, db
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, VARCHAR, DATETIME, Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
import enum


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    STAFF = 3


class BaseUser(db.Model):
    __abstract__ = True
    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    adddress = Column(String(150))
    phone = Column(VARCHAR(10))


class Staff(BaseUser, UserMixin):
    # attribute
    work = Column(String(150))
    salary = Column(Float, default=0)
    start_day = Column(DATETIME, default=datetime.now())


    # relationship
    invoices = relationship('Invoice', lazy=True, backref='staff')
    def __str__(self):
        return self.user_name


class User(BaseUser, UserMixin):
    # attribute
    certificate = Column(VARCHAR(10))
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    #relationship
    invoices = relationship('Invoice', lazy=True, backref='customer')
    def __str__(self):
        return self.user_name


class Category(db.Model):
    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    capacity = Column(Integer, default=2)

    # relationship
    rooms = relationship('Room', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Room(db.Model):
    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    image = Column(String(500),
                   default='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
    active = Column(Boolean, default=True)

    # relationship
    facilities = relationship('Facility', backref='room', lazy=True)
    images = relationship('Images', backref='room', lazy=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    bookings = relationship('Booking', lazy=True, backref='room')
    def __str__(self):
        return self.name


class Facility(db.Model):
    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer, default=1)
    active = Column(Boolean, default=True)

    # foreign-key
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


class Images(db.Model):
    # attribute
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(150), unique=True,
                  default="https://th.bing.com/th/id/OIP.ez4CSm0lvNT4oqojhoiE9AHaH_?rs=1&pid=ImgDetMain")

    # foreign-key
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)






class Booking(db.Model):
    # attribute
    id = Column(Integer, autoincrement=True, primary_key=True)
    start = Column(DATETIME())
    end = Column(DATETIME())
    contains = Column(Integer, nullable=False)

    # foreign-key
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    room_id = Column(ForeignKey('room.id'), nullable=False)
    # relationship



class Invoice(db.Model):
    # attribute
    id = Column(Integer, autoincrement=True, primary_key=True)
    total = Column(Float, default=0)
    release = Column(DATETIME())

    # foreign-key
    user_id = Column(ForeignKey('user.id'), nullable=False)
    staff_id = Column(ForeignKey('staff.id'), nullable=False)

    # relationship
    bookings = relationship('Booking', lazy=True, backref='invoice')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # a = User(user_name='Admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), staff_id='4', role=UserRoleEnum.ADMIN)
        # db.session.add(a)
        # db.session.commit()
        # c1 = Category(name='Phòng đôi')
        # c2 = Category(name='Phòng đơn')
        # c3 = Category(name='Phòng gia đình')

        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)

        # p5 = Room(name='P105', price=290000, category_id='2')
        # p6 = Room(name='P106', price=450000, category_id='1')
        # p7 = Room(name='P107', price=550000, category_id='3')
        # p8 = Room(name='P108', price=600000, category_id='3')
        #
        #
        # db.session.add(p5)
        # db.session.add(p6)
        # db.session.add(p7)
        # db.session.add(p8)
        # db.session.commit()
