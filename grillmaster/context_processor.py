def calculate_shipping(total):
    shipping = 0
    if total > 50000:
        return 0
    return shipping

def calculate_taxes(total):
    return round(total * 0.19)

def shopping_cart_total(request):
    total = 0
    amount = 0
    try:
        for key, value in request.session['shopping_cart'].items():
            amount = amount + int(value['amount'])
            total = total + int(value['price']) * value['amount']
    except:
        request.session['shopping_cart'] = {}
        total = 0

    shipping = calculate_shipping(total)
    taxes = calculate_taxes(total)

    return { 
        'taxes': taxes,
        'shopping_cart_total': (total + taxes + shipping), 
        'shopping_cart_amount': amount,
        'shipping': shipping,
    }

def get_page_number(request):
    page = 1
    try:
        page = int(request.GET.get('page'))
        if not page:
            page = 1
    except:
        page = 1
    return page
