import math
import utils
from flask import request, render_template, redirect, jsonify, session

from app import dao, app
from app import login
from flask_login import login_user

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
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.context_processor
def common_res():
    return{
        'categories' : dao.get_categories(),
        'cart_stats' : utils.count_cart(session.get('cart'))
    }


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
