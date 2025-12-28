from django.db import models
from django.urls import reverse

class InfoPage(models.Model):
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL-имя (например, about)")
    title = models.CharField(max_length=200, verbose_name="Заголовок страницы")
    content = models.TextField(verbose_name="Текст страницы (можно HTML)")

    seo_title = models.CharField(max_length=250, blank=True, verbose_name="SEO Title (для браузера)")
    seo_description = models.CharField(max_length=500, blank=True, verbose_name="SEO Description")

    class Meta:
        verbose_name = 'Инфо-страница'
        verbose_name_plural = 'Инфо-страницы'

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name="Размер")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sizes = models.ManyToManyField(Size, blank=True, related_name='products', verbose_name="Доступные размеры")
    
    # НОВЫЕ SEO ПОЛЯ
    seo_title = models.CharField(max_length=250, blank=True, verbose_name="SEO Title")
    seo_description = models.CharField(max_length=500, blank=True, verbose_name="SEO Description")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    text = models.CharField(max_length=200, blank=True, verbose_name="Текст")
    image = models.ImageField(upload_to='banners/', verbose_name="Изображение")
    link = models.CharField(max_length=200, blank=True, verbose_name="Ссылка (например /category/notebooks)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    TYPE_CHOICES = (
        ('main', 'Главный (Большой)'),
        ('small_top', 'Маленький (Боковой верхний)'),
        ('small_bottom', 'Маленький (Боковой нижний)'),
    )
    banner_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='main')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

class SiteSettings(models.Model):
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", default="+375 29 123 45 67")
    email = models.EmailField(verbose_name="Email", default="info@lana.by")
    address = models.CharField(max_length=200, verbose_name="Адрес", default="г. Минск, пр. Независимости 100")
    
    telegram = models.URLField(blank=True, verbose_name="Ссылка на Telegram")
    vk = models.URLField(blank=True, verbose_name="Ссылка на VK")
    instagram = models.URLField(blank=True, verbose_name="Ссылка на Instagram")
    odnoklassniki = models.URLField(blank=True, verbose_name="Ссылка на Одноклассники")
    facebook = models.URLField(blank=True, verbose_name="Ссылка на Facebook")
    tiktok = models.URLField(blank=True, verbose_name="Ссылка на TikTok")
    youtube = models.URLField(blank=True, verbose_name="Ссылка на YouTube")

    def __str__(self):
        return "Настройки контактов (редактировать тут)"

    @property
    def phone_link(self):
        if self.phone:
            return self.phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        return "#"

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'