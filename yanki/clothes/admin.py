from django.contrib import admin
from .models import *


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("id", 'title', "price")
#     list_display_links = ('id', 'title')
#     search_fields = ('title', 'price')
#     prepopulated_fields = {'slug': ('title',)}
class SSS(admin.ModelAdmin):
    list_display = ("id", 'parent', "color", "size", "count")
    list_display_links = ('id', "parent")


admin.site.register(Product, SSS)


class ASD(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(BaseProduct, ASD)


class CatalogAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Catalog, CatalogAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Tag, TagAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')
admin.site.register(Size, SizeAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')
admin.site.register(Color, ColorAdmin)
