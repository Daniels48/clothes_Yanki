from django.contrib import admin
from django.db.models import Count
from django.http import JsonResponse
from .models import *
from django import forms
from .others import decode_json


class BaseProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class ProductAdminForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=BaseProduct.objects.all(), empty_label="Выберете базовый продукт")
    size = forms.ModelChoiceField(queryset=Size.objects.none(), required=False, empty_label="Выберете сначала базовый продукт")
    color = forms.ModelChoiceField(queryset=Color.objects.none(), required=False, empty_label="Выберете сначала цвет")

    class Meta:
        model = Product
        fields = "__all__"


class ProductAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST" and request.body:
            obj = self.change_value(request)
            return JsonResponse(obj)
        return self.changeform_view(request, None, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if request.method == "POST" and request.body:
            obj = self.change_value(request)
            return JsonResponse(obj)
        return self.changeform_view(request, object_id, form_url, extra_context)

    def change_value(self, request):
        data = decode_json(request.body)
        size = data.get("size")
        parent = data.get("parent")
        response_obj = {}

        if size:
            list_color_id = [x.get("color", "") for x in
                             list(Product.objects.all().
                                  filter(parent__title=parent, size__title=size).
                                  values("color"))]
            list_title_color = list(Color.objects.all().exclude(id__in=list_color_id).values("title"))

            list_response = self.get_obj_response(list_title_color)
            response_obj["color"] = list_response
        else:
            Count_color = Color.objects.aggregate(Count('id')).get("id__count")
            list_size_id = [x.get("size", "") for x in
                            Product.objects.all().values("size", "parent").
                            annotate(count_size=Count("color")).filter(count_size=Count_color, parent__title=parent)]

            list_title_size = list((Size.objects.all().exclude(id__in=list_size_id).values("title")))
            list_response = self.get_obj_response(list_title_size)
            response_obj["size"] = list_response

        return response_obj

    @staticmethod
    def get_obj_response(list_data):
        pk = 0
        list_values = []
        for x in list_data:
            pk += 1
            obj = {"id": pk, "name": x.get("title")}
            list_values.append(obj)
        return list_values

    # z = ProductAdmin.change_value()
    # form = ProductAdminForm


class CatalogAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')


class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", 'title')
    list_display_links = ('id', 'title')


admin.site.register(BaseProduct, BaseProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)