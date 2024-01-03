from datetime import datetime
def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += 1
            start = datetime.strptime(c['start'], '%Y-%m-%d')
            end = datetime.strptime(c['end'], '%Y-%m-%d')
            result = int((end - start).days)
            total_amount += result
            # total_amount += c['price'] *c['price']

    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity
    }
