from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views 
from shop import views as shop_views 

urlpatterns = [
    path('admin/', admin.site.urls),
     path('robots.txt', TemplateView.as_view(
        template_name="shop/robots.txt", 
        content_type="text/plain"
    )),

    path('login/', auth_views.LoginView.as_view(template_name='shop/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', shop_views.register, name='register'),

    path('', include('shop.urls', namespace='shop')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)