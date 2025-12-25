from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('success/<int:order_id>/', views.success, name='success'),
    path('my-orders/', views.my_orders, name='my_orders'),

    path('paritet/pay/<int:order_id>/', views.paritet_pay, name='paritet_pay'),
    path('paritet/process/<int:order_id>/', views.paritet_process, name='paritet_process'),
]