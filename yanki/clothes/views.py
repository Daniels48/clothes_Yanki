from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from users.models import User
from yanki.settings import SITE_NAME
from clothes.models import *
from .forms import Change_person_data
from .others import decode_json
from .set_session_data.cart import get_list_cart, Cart
from .set_session_data.currency import set_currency_for_page, get_all_sum_or_one
from .set_session_data.like import get_list_favorite, set_like_cls_for_product
from .utils import GeneralMixin, get_catalog_products, get_list_category, get_product, get_list_for_product, \
    get_max_price, set_currency_and_like


class ClothesHome(GeneralMixin, ListView):
    model = Catalog
    template_name = "clothes/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = True
        context["title"] = "Главная страница"
        return context


class ClothesCatalog(GeneralMixin, ListView):
    model = BaseProduct
    template_name = "clothes/catalog.html"

    def get_queryset(self):
        category, filters = [self.kwargs.get("category"), self.request.GET]
        products = get_catalog_products(category, filters, self.request)
        query = set_currency_and_like(products, self.request)
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get("category")
        context["catalog"] = get_list_category()
        context["max"] = get_max_price(self.request)
        context["title"] = "Каталог"
        context["size"] = Size.objects.all()
        context["color"] = Color.objects.all()

        if category:
            cats = [catty for catty in context["catalog"] if category and category == catty.slug][0]
            context["title"] = cats.title
            context["category"] = cats
        return context


class ClothesProduct(GeneralMixin, DetailView):
    model = Product
    template_name = "clothes/product.html"

    def get_object(self, queryset=None):
        name = self.kwargs.get("name")
        raw_product = get_product(name, self.request)
        products_currency = set_currency_for_page(raw_product, self.request)
        # query = set_currency_and_like(raw_product, self.request)
        # # return query
        return set_like_cls_for_product(products_currency, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.parent.title
        context["list"] = set_currency_for_page(get_list_for_product(), self.request)
        return context


class ClothesHistory(GeneralMixin, ListView):
    model = Catalog
    template_name = "clothes/history.html"
    extra_context = {'title': f"{SITE_NAME} | История заказов"}


class ClothesInfo(GeneralMixin, ListView):
    model = Catalog
    template_name = "clothes/person.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        person = User.objects.get(id=self.request.user.id)
        context["form"] = Change_person_data(instance=person)
        return context

    def post(self, request):
        data = decode_json(request.body)
        print(data, 22222222)
        person = User.objects.get(id=self.request.user.id)
        form = Change_person_data(data, instance=person)
        response = "ok"
        if form.is_valid():
            form.save()
        else:
            response = "fail"
            valid = form.errors.as_data()
        return JsonResponse({"success": response})


class ClothesCart(Cart, GeneralMixin, ListView):
    model = Product
    template_name = "clothes/cart.html"

    def get_queryset(self):
        return get_list_cart(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_sum"] = get_all_sum_or_one(self.request)
        context["title"] = "Корзина"
        return context


class ClothesFavorite(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/favorite.html"

    def get_queryset(self):
        raw_query = get_list_favorite(self.request)
        query = set_currency_and_like(raw_query, self.request)
        # query = set_like_cls_for_product(raw_query, self.request)
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранное"
        return {**context}


class ClothesAbout(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/o_nas.html"

def pageNotFound(request, exception):
    return HttpResponseNotFound('dappes')
