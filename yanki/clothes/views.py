from django.http import HttpResponseNotFound, JsonResponse
from django.views.generic import DetailView, ListView
from yanki.settings import SITE_NAME, CART_SESSION_ID, LIKE_SESSION_ID, CURRENCY_SESSION_ID
from clothes.models import *
from .forms import Change_person_data
from .others import decode_json
from .set_session_data.cart import get_list_cart, Cart
from .set_session_data.currency import get_all_sum_or_one
from .set_session_data.like import get_favorite_products
from .utils import GeneralMixin, get_catalog_products, get_list_category, get_product, get_list_for_product, \
    get_max_price


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
        return get_catalog_products(category, filters, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get("category")
        context["catalog"] = get_list_category()
        context["max"] = get_max_price(self.request)
        context["title"] = "Каталог"
        context["size"] = Size.objects.all()
        context["color"] = Color.objects.all()

        if category:
            tilte_category = [name for name in context["catalog"] if category and category == name.slug][0]
            context["title"] = tilte_category.title
            context["category"] = tilte_category
        return context


class ClothesProduct(GeneralMixin, DetailView):
    model = Product
    template_name = "clothes/product.html"

    def get_object(self, queryset=None):
        name = self.kwargs.get("name")
        return get_product(name, self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.parent.title
        context["list"] = get_list_for_product(self.request)
        return context


class ClothesHistory(GeneralMixin, ListView):
    model = Catalog
    template_name = "clothes/history.html"
    extra_context = {'title': f"{SITE_NAME} | История заказов"}


class ClothesInfo(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/person.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        person = self.request.user
        context["form"] = Change_person_data(instance=person)
        return context

    def post(self, request):
        data = decode_json(request.body)
        person = self.request.user
        form = Change_person_data(data, instance=person)
        response = "ok"
        if form.is_valid():
            form.save()
        else:
            response = "fail"
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
        return get_favorite_products(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранное"
        return {**context}


class ClothesAbout(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/o_nas.html"


def pageNotFound(request, exception):
    return HttpResponseNotFound('dappes')
