from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class ShippingMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название (например, Европочта)")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена (BYN)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = 'Способ доставки'
        verbose_name_plural = 'Способы доставки'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.price} BYN)"


class Order(models.Model):
    # --- ВАРИАНТЫ ОПЛАТЫ ---
    PAYMENT_METHOD_CHOICES = (
        ('yookassa', 'ЮKassa (Карты РФ, SberPay)'),
        ('paritet', 'Паритет Банк (Карты РБ: Visa, MasterCard, BelKart)'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    
    shipping_method = models.CharField(max_length=100, verbose_name="Способ доставки")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Стоимость доставки")
    
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='yookassa', 
        verbose_name="Способ оплаты"
    )

    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False, verbose_name="Оплачено")
    payment_id = models.CharField(max_length=100, blank=True, verbose_name="ID платежа")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_total_cost(self):
        total_product_cost = sum(item.get_cost() for item in self.items.all())
        return total_product_cost + self.shipping_cost

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity