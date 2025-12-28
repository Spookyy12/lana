from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Banner, InfoPage
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products_list = Product.objects.filter(available=True)
    
    # --- НОВЫЙ КОД: Получаем SEO для главной ---
    # Ищем страницу с slug='home'. first() вернет None, если страницы нет (чтобы сайт не упал)
    seo_page = InfoPage.objects.filter(slug='home').first() 
    # -------------------------------------------

    # Поиск
    query = request.GET.get('q') 
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=category)
    
    # Пагинация
    paginator = Paginator(products_list, 9) # 9 товаров на странице
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    main_banner = Banner.objects.filter(is_active=True, banner_type='main').first()
    
    # Забираем конкретные баннеры для верхней и нижней позиции справа
    small_top_banner = Banner.objects.filter(is_active=True, banner_type='small_top').first()
    small_bottom_banner = Banner.objects.filter(is_active=True, banner_type='small_bottom').first()

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'main_banner': main_banner,
        'small_top_banner': small_top_banner,
        'small_bottom_banner': small_bottom_banner,
        'query': query,
        'seo_page': seo_page
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    size = request.POST.get('size', None) 

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'],
                 size=size) # Передаем размер
    
    next_page = request.META.get('HTTP_REFERER')
    if next_page:
        return redirect(next_page)
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'shop/cart/detail.html', {'cart': cart})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'shop/registration/register.html', {'form': form})

def about(request):
    page = get_object_or_404(InfoPage, slug='about')
    return render(request, 'shop/pages/info_page.html', {'page': page})

def privacy(request):
    page = get_object_or_404(InfoPage, slug='privacy')
    return render(request, 'shop/pages/info_page.html', {'page': page})

def delivery_info(request):
    page = get_object_or_404(InfoPage, slug='delivery')
    return render(request, 'shop/pages/info_page.html', {'page': page})