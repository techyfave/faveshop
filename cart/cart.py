from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        # Use a default value if CART_SESSION_ID is not in settings
        cart_session_id = getattr(settings, 'CART_SESSION_ID', 'cart')
        cart = self.session.get(cart_session_id)
        if not cart:
            cart = self.session[cart_session_id] = {}
        self.cart = cart
        self.cart_session_id = cart_session_id  # Store for later use
    
    def add(self, product, quantity=1):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        self.cart[product_id]['quantity'] += quantity
        self.save()
    
    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # del self.session[settings.CART_SESSION_ID]
        del self.session[self.cart_session_id]
        self.save()
    
    def save(self):
        self.session.modified = True
    
    def get_items(self):
        """Get cart items with product objects"""
        items = []
        for product_id, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                item = {
                    'product': product,
                    'quantity': item_data['quantity'],
                    'price': Decimal(item_data['price']),
                    'total_price': Decimal(item_data['price']) * item_data['quantity']
                }
                items.append(item)
            except Product.DoesNotExist:
                continue
        return items