import math
from app import utils
from flask import request, render_template, redirect, jsonify, session
from datetime import datetime, timedelta
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import dao, app
from app import login
from flask_login import login_user
from flask_login import logout_user, current_user
import requests


@app.route("/")
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get('page')
    prods = dao.get_products(kw, cate_id, page)
    num = dao.count_product()
    page_size = app.config['PAGE_SIZE']
    return render_template('index.html', products=prods,
                           pages=math.ceil(num/page_size))


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user)

    return redirect('/admin')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json
    cart = session.get('cart')
    if cart is None:
        cart = {}

    id = str(data.get("id"))
    # if id in cart:
    #     # cart[id]['quantity'] += 1
    if id not in cart:
        cart[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "start": str(datetime.now().date()),
            "end": str(datetime.now().date() + timedelta(days=1)),
            "contain": int('2')
        }

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/cart')
def cart():
    # uname = request.args.get('uname')
    # session['us_name'] = str(uname)
    return render_template('cart.html')


@app.route('/single')
def single():
    page = request.args.get('page')
    s_room = dao.query_single_room(page)
    num = dao.count_single_room()
    page_size = app.config['PAGE_SIZE']
    return render_template('single.html', single_room=s_room,
                           pages=math.ceil(num/page_size))


@app.context_processor
def common_res():
    return{
        'categories' : dao.get_categories(),
        'cart_stats' : utils.count_cart(session.get('cart'))
    }


@app.route('/api/cart/<room_id>', methods=['put'])
def update_cart(room_id):
    cart = session.get('cart')
    if cart and room_id in cart:
        # start = request.json.get('start')
        end = request.json.get('end')
        # cart[room_id]['start'] = str(start)
        cart[room_id]['end'] = str(end)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/start/<room_id>', methods=['put'])
def update_cart_start(room_id):
    cart = session.get('cart')
    if cart and room_id in cart:
        start = request.json.get('start')
        cart[room_id]['start'] = str(start)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route('/api/cart/contain/<room_id>', methods=['put'])
def update_cart_contain(room_id):
    cart = session.get('cart')
    if cart and room_id in cart:
        contain = request.json.get('contain')
        cart[room_id]['contain'] = int(contain)

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))

@app.route('/api/cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart
    return jsonify(utils.count_cart(cart))


@app.route('/login', methods = ['post', 'get'])
def process_user_login():
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)

        next = request.args.get('next')
        return redirect("/" if next is None else next)
    return render_template('login.html')


@app.route("/api/pay", methods=['post'])
def pay():

    if dao.add_receipt(session.get('cart')):

        del session['cart']
        # del session['us_name']
        # del session['us_phone']
        # del session['us_id']
        return jsonify({'status': 200})
    else:
        return jsonify({'status':500})
    # return jsonify({'status': 500, 'err_msg': 'Something wrong!'})

@app.route('/endpoint', methods=['POST'])
def process_data():
    data = request.get_json()
    value = data['data']
    session['us_name'] = str(value)
    response = {
        'message': 'Đã nhận giá trị thành công',
        'value': value
    }
    return jsonify(response)

@app.route('/endpointt', methods=['POST'])
def processs_data():
    data = request.get_json()
    value = data['data']
    session['us_phone'] = int(value)
    response = {
        'message': 'Đã nhận giá trị thành công',
        'value': value
    }
    return jsonify(response)

@app.route('/endpointtt', methods=['POST'])
def processss_data():
    data = request.get_json()
    value = data['data']
    session['us_id'] = int(value)
    response = {
        'message': 'Đã nhận giá trị thành công',
        'value': value
    }
    return jsonify(response)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = None
    if request.method.__eq__("POST"):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_staff(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password)
            except Exception as e:
                err_msg = str(e)
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/rooms/<id>')
def details(id):
    page = request.args.get('page')
    num = dao.count_img_by_id(id)
    page_size = app.config['PAGE_SIZE_DETAILS']
    return render_template('details.html',
                           room=dao.get_room_by_id(id),
                           images=dao.get_img_by_id(id),
                           facilities=dao.get_facilities_by_id(id),
                           pages=math.ceil(num/page_size),
                           imgs = dao.get_imgs(id, page))




if __name__ == '__main__':
    from app import admin
    app.run(debug=True)

