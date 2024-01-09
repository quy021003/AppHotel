from app.models import Category, Room, UserRoleEnum
from app import app, db, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request

class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_rooms_by_cate())

admin = Admin(app=app, name='QUẢN TRỊ KHÁCH SẠN', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyRoomView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'price', 'active']
    column_searchable_list = ['name']
    form_excluded_columns = ['facilities', 'customers', 'images']


class MyCategoryView(AuthenticatedAdmin):
    column_list = ['name', 'rooms']


class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        kw = request.args.get('kw')
        return self.render('admin/stats.html', stats = dao.get_revenue_on_room(kw=kw), customers = dao.count_customer_by_room())


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyRoomView(Room, db.session))
admin.add_view(MyStatsView(name='Statistic'))
admin.add_view(LogoutView(name='Log out'))
