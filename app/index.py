import math
import utils
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
            "end": str(datetime.now().date() + timedelta(days=1))
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/cart')
def cart():
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
    # if dao.add_receipt(session.get('cart')):
    if dao.add_receipt(session.get('cart')):
        del session['cart']
        return jsonify({'status': 200})
    else:
        return jsonify({'status':500})
    # return jsonify({'status': 500, 'err_msg': 'Something wrong!'})





if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
