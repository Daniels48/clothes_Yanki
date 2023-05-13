from django.http import HttpResponseNotFound
from django.views.generic import DetailView, ListView
from yanki.settings import SITE_NAME
from .set_session_data.cart import get_list_cart, Cart
from .set_session_data.currency import set_currency_for_page, get_all_sum_or_one
from .set_session_data.like import get_list_favorite, set_like_cls_for_product
from .utils import *


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
        products = get_catalog_products(category, filters)
        raw_products = set_currency_for_page(products, self.request)
        return set_like_cls_for_product(raw_products, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get("category")
        context["catalog"] = get_list_category()
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
        raw_product = get_product(name)
        products_currency = set_currency_for_page(raw_product, self.request)
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
        return {**context}


class ClothesCart(Cart, GeneralMixin, ListView):
    model = Product
    template_name = "clothes/cart.html"

    def get_queryset(self):
        return get_list_cart(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_sum"] = get_all_sum_or_one(self.request)
        return context


class ClothesFavorite(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/favorite.html"

    def get_queryset(self):
        return get_list_favorite(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранное"
        return {**context}


class ClothesAbout(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/o_nas.html"


def pageNotFound(request, exception):
    return HttpResponseNotFound('dappes')
