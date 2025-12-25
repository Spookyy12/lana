import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order, ShippingMethod
from .forms import OrderCreateForm
from shop.cart import Cart
from yookassa import Configuration, Payment

Configuration.account_id = '1191034'
Configuration.secret_key = 'test_EXwu3slLHiyWSmeBKX2IKx7K5cO_TiC8Rm_McYO9nWY'

def order_create(request):
    cart = Cart(request)
    if cart.get_total_price() == 0:
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            shipping_obj = form.cleaned_data['shipping_method_obj']
            order.shipping_method = shipping_obj.name
            order.shipping_cost = shipping_obj.price
            
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])

            final_price = cart.get_total_price() + shipping_obj.price 
            if order.payment_method == 'yookassa':
                idempotence_key = str(uuid.uuid4())
                payment = Payment.create({
                    "amount": {
                        "value": str(final_price),
                        "currency": "RUB" # Юкасса принимает RUB
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": request.build_absolute_uri(f'/orders/success/{order.id}/')
                    },
                    "capture": True,
                    "description": f"Заказ №{order.id}"
                }, idempotence_key)

                order.payment_id = payment.id
                order.save()
                return redirect(payment.confirmation.confirmation_url)

            # ВАРИАНТ 2: ПАРИТЕТ БАНК (Заглушка)
            elif order.payment_method == 'paritet':
                return redirect('orders:paritet_pay', order_id=order.id)
                
    else:
        form = OrderCreateForm()
        form.fields['payment_method'].initial = 'yookassa'
    
    shipping_methods = ShippingMethod.objects.all()
    return render(request, 'orders/create.html', {
        'cart': cart, 'form': form, 'shipping_methods': shipping_methods
    })

# --- ФУНКЦИИ ДЛЯ ИМИТАЦИИ БАНКА ---

def paritet_pay(request, order_id):
    """Отображает фейковую форму ввода карты"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/paritet_pay.html', {'order': order})

def paritet_process(request, order_id):
    """Обрабатывает нажатие кнопки 'Оплатить' в фейковом банке"""
    order = get_object_or_404(Order, id=order_id)

    order.paid = True 
    order.save()

    cart = Cart(request)
    cart.clear()

    return render(request, 'orders/success.html')

def success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart = Cart(request)
    cart.clear()
    try:
        payment = Payment.find_one(order.payment_id)
        if payment.status == 'succeeded':
            order.paid = True
            order.save()
    except Exception:
        pass
    return render(request, 'orders/success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/my_orders.html', {'orders': orders})