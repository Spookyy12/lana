from .cart import Cart
from .models import SiteSettings

def cart(request):
    return {'cart': Cart(request)}

def site_settings(request):
    settings = SiteSettings.objects.first()
    return {'contacts': settings}