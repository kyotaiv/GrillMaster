class ShoppingCart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        shopping_cart = self.session.get('shopping_cart')
        if not shopping_cart:
            shopping_cart = self.session['shopping_cart'] = {}
        self.shopping_cart = shopping_cart

    def add(self, productos):
        id = str(productos.id)
        if id not in self.shopping_cart.keys():
            self.shopping_cart[id]={
                'id': productos.id,
                'name': productos.name,
                'description': productos.description,
                'price': str(productos.price),
                'amount': 1,
                'total': productos.price,
                'url': productos.image.url,
            }
        else:
            self.shopping_cart[id]['amount'] = self.shopping_cart[id]['amount'] + 1
            self.shopping_cart[id]['price'] = productos.price
            self.shopping_cart[id]['total'] = self.shopping_cart[id]['total'] + productos.price
        self.save()
    
    def get_amount(self, productos):
        id = str(productos.id)
        try:
            return self.shopping_cart[id]['amount']
        except:
            return 0
        
    def save(self):
        self.session['shopping_cart'] = self.shopping_cart
        self.session.modified = True

    def delete(self, productos):
        id = str(productos.id)
        if id in self.shopping_cart:
            del self.shopping_cart[id]
            self.save()
    
    def substract(self, productos):
        for key, value in self.shopping_cart.items():
            if key == str(productos.id):
                value['amount'] = value['amount'] - 1
                value['total'] = value['total'] - productos.price
                if value['amount'] < 1:
                    self.delete(productos)
                break
        self.save()

    def clear(self):
        self.session['cart_open'] = False
        self.session['shopping_cart'] = {}
        self.session.modified = True