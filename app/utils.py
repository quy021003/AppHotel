from datetime import datetime
def count_cart(cart):
    total_quantity, total_amount, contain = 0, 0, 0

    if cart:
        for c in cart.values():
            # Mặc định là 2 người, nếu cứ thêm 1 người thì phụ thu thêm 25%
            regulation = 2
            charge = c['price'] * 0.25
            person_excess = c['contain'] - regulation


            total_quantity += 1
            start = datetime.strptime(c['start'], '%Y-%m-%d')
            end = datetime.strptime(c['end'], '%Y-%m-%d')
            result = int((end - start).days)

            total_amount += result * (c['price'] + charge*person_excess)
            contain += c['contain']
    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity,
        'contain': contain
    }
