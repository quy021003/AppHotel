from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '%432%123sfdsxcsdvfdg'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:Thiquy0779179473@localhost/hoteldb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
app.config["PAGE_SIZE_DETAILS"] = 2
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
