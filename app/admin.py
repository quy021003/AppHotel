from app.models import Category, Room, UserRoleEnum
from app import app, db, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, request, render_template


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
        return self.render('admin/stats.html', stats = dao.get_revenue_on_room(kw=kw)\
                           , customers = dao.count_customer_by_room()\
                           , rooms_booking = dao.stats_room_booking())


class MyInvoiceView(AuthenticatedUser):
    @expose("/")
    def index(self):
        kw = request.args.get('kw_invoice')
        c_id = request.args.get('c_id')
        return self.render('admin/invoice.html', invoices=dao.get_invoices(kw=kw, c_id=c_id))

class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

@app.route('/admin/myinvoiceview/<id>')
def bookings(id):
    return render_template('/admin/booking.html', books=dao.get_bookings(id))

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyRoomView(Room, db.session))
admin.add_view(MyStatsView(name='Thống kê'))
admin.add_view(MyInvoiceView(name='Hoá đơn'))
admin.add_view(LogoutView(name='Đăng xuất'))

