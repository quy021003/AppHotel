import hashlib

from app import app, db
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, VARCHAR, DATETIME, Enum, DateTime
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
    name = Column(String(50), default='user_normal')
    phone = Column(VARCHAR(10))


# class Staff(BaseUser, UserMixin):
#     # attribute
#
#     work = Column(String(150))
#     salary = Column(Float, default=0)
#     start_day = Column(DateTime, default=datetime.now())
#     role = Column(Enum(UserRoleEnum), default=UserRoleEnum.STAFF)
#
#     # relationship
#     invoices = relationship('Invoice', lazy=True, backref='staff')
#     def __str__(self):
#         return self.user_name


class User(BaseUser, UserMixin):
    # attribute
    user_name = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    # relationship
    invoices = relationship('Invoice', lazy=True, backref='user')
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
    image = Column(String(900),
                   default='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
    active = Column(Boolean, default=True)

    # relationship
    facilities = relationship('Facility', backref='room', lazy=True)
    images = relationship('Images', backref='room', lazy=True)
    bookings = relationship('Booking', lazy=True, backref='room')

    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

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
    start = Column(DateTime, default=datetime.now())
    end = Column(DateTime, default=datetime.now())
    contains = Column(Integer, default=2)
    price = Column(Float, default=0)
    # foreign-key
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    room_id = Column(ForeignKey('room.id'), nullable=False)
    # relationship


class Invoice(db.Model):
    # attribute
    id = Column(Integer, autoincrement=True, primary_key=True)
    total = Column(Float, default=0)
    release = Column(DateTime, default=datetime.now())

    # foreign-key
    user_id = Column(ForeignKey('user.id'))
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    # relationship
    bookings = relationship('Booking', lazy=True, backref='invoice')

class Customer(BaseUser):
    cert = Column(VARCHAR(12), default='000000000000')
    invoices = relationship('Invoice', lazy=True, backref='customer')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        a = User(name='Nguyễn Thi Quý', user_name='thiquy1243', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                  role=UserRoleEnum.ADMIN)
        b = User(name='Nguyễn Thi Quý', user_name='staff', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 role=UserRoleEnum.STAFF)


        c1 = Category(name='Phòng đôi', capacity=2)
        c2 = Category(name='Phòng đơn', capacity=1)
        c3 = Category(name='Phòng gia đình', capacity=5)
        db.session.add(a)
        db.session.add(b)
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)

        p1 = Room(name='A01', price=300000,category_id=1,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p2 = Room(name='A02', price=350000,category_id=1,active=False, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p3 = Room(name='A03', price=300000,category_id=1,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p4 = Room(name='A04', price=300000,category_id=1,active=False, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p5 = Room(name='B01', price=300000,category_id=2,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p6 = Room(name='B02', price=300000,category_id=2,active=False, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p7 = Room(name='B03', price=300000,category_id=2,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p8 = Room(name='B04', price=300000,category_id=2,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p9 = Room(name='C01', price=300000,category_id=3,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p10 = Room(name='C02', price=300000,category_id=3,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p11 = Room(name='C03', price=300000,category_id=3,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        p12 = Room(name='C04', price=300000,category_id=3,active=True, image='https://th.bing.com/th/id/R.1d28a8a270a65d2f064490e3328cb67c?rik=TecRpNJsxZbrrw&riu=http%3a%2f%2fddcorporation.vn%2fupload%2fimages%2ftin-tuc%2fthiet-ke-thi-cong-noi-that-khach-san-dep-tai-ha-noi8.jpg&ehk=2YGZZBGQ8y5mPy8Jf1EfC4SAGqf7Otwa%2fh3WRiKOimo%3d&risl=&pid=ImgRaw&r=0')
        db.session.add(p1)
        db.session.add(p3)
        db.session.add(p5)
        db.session.add(p7)
        db.session.add(p9)
        db.session.add(p2)
        db.session.add(p4)
        db.session.add(p6)
        db.session.add(p8)
        db.session.add(p10)
        db.session.add(p11)
        db.session.add(p12)

        f1 = Facility(name='Quạt máy', quantity=2, active=True, room_id=1)
        f2 = Facility(name='Máy lạnh', quantity=1, active=True, room_id=1)
        f3 = Facility(name='TV', quantity=2, active=True, room_id=1)
        f4 = Facility(name='Bếp ăn', quantity=2, active=True, room_id=1)
        f5 = Facility(name='Quạt máy', quantity=2, active=True, room_id=2)
        f6 = Facility(name='Máy lạnh', quantity=2, active=True, room_id=2)
        f7 = Facility(name='Quạt máy', quantity=2, active=True, room_id=3)
        f8 = Facility(name='Tủ lạnh', quantity=2, active=True, room_id=3)
        f9 = Facility(name='Máy lạnh', quantity=2, active=True, room_id=3)
        f10 = Facility(name='Ban công', quantity=2, active=True, room_id=2)
        f11= Facility(name='Tủ lạnh', quantity=2, active=True, room_id=2)
        facts = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]
        db.session.add_all(facts)

        i1 = Images(link='https://th.bing.com/th/id/OIP.35Xr7_P7FEuhmUPoeLQvtwHaE7?w=1600&h=1066&rs=1&pid=ImgDetMain', room_id=1)
        i2 = Images(link='https://th.bing.com/th/id/OIP.yrUafSdDC4pPUwnqDX1OGwHaEl?w=855&h=530&rs=1&pid=ImgDetMain', room_id=1)
        i3 = Images(link='https://th.bing.com/th/id/OIP.UZ1snS1rLSc3mqdSszYVZwHaD4?w=1710&h=898&rs=1&pid=ImgDetMain', room_id=1)
        i4 = Images(link='https://th.bing.com/th/id/OIP.Yv1zB7JREyJRX73gIzUbKQHaEz?rs=1&pid=ImgDetMain', room_id=1)
        i5 = Images(link='https://th.bing.com/th/id/OIP.Gjmx4trnHBSwVsDRMG2xTQHaFz?w=850&h=666&rs=1&pid=ImgDetMain', room_id=1)

        imgs = [i1, i2, i3, i4, i5]
        db.session.add_all(imgs)
        db.session.commit()

