from django.contrib import admin
from .models import Category, Product, Banner, InfoPage, Size
from .models import SiteSettings

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'content')}),
        ('SEO настройки', {'fields': ('seo_title', 'seo_description')}),
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created']
    list_filter = ['available', 'created', 'updated', 'sizes']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('sizes',)

    fieldsets = (
        # Добавлено поле 'sizes' в список fields ниже
        ('Товар', {'fields': ('category', 'name', 'slug', 'image', 'description', 'price', 'sizes', 'available')}),
        ('SEO настройки', {'fields': ('seo_title', 'seo_description')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'is_active']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()