from django.contrib.auth import views as auth_views
from shop import views as shop_views 

urlpatterns = [
    
    path('login/', auth_views.LoginView.as_view(template_name='shop/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', shop_views.register, name='register'),
    
]