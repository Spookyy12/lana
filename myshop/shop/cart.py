from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart(object):
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False, size=None):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart[product_id] = {'quantity': 0, 'price': str(product.price), 'size': ''}

        if size:
            self.cart[product_id]['size'] = size
            
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        # Список найденных ID, чтобы очистить мусор
        found_ids = []

        for product in products:
            found_ids.append(str(product.id))
            cart[str(product.id)]['product'] = product
            
        # ОЧИСТКА: Удаляем из сессии товары, которых нет в базе
        for product_id in list(self.cart.keys()):
            if product_id not in found_ids:
                del self.cart[product_id]
                self.save() # Сохраняем очищенную сессию
                if product_id in cart:
                    del cart[product_id]

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Считаем только существующие товары
        """
        product_ids = self.cart.keys()
        # Фильтруем только те, что есть в БД
        products = Product.objects.filter(id__in=product_ids)
        
        count = 0
        for product in products:
            count += self.cart[str(product.id)]['quantity']
        return count

    def get_total_price(self):
        """
        Считаем цену только для существующих товаров
        """
        product_ids = self.cart.keys()
        # Фильтруем только те, что есть в БД
        products = Product.objects.filter(id__in=product_ids)
        
        total = Decimal('0.00')
        for product in products:
            item = self.cart[str(product.id)]
            total += Decimal(item['price']) * item['quantity']
        return total
        
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()