from django.http import HttpResponseNotFound, JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView
from clothes.models import *
from users.models import *
from .forms import Change_person_data
from .others import decode_json, json_response
from .set_session_data.cart import Cart
from .set_session_data.like import get_favorite_products
from .utils import GeneralMixin, get_catalog_products, get_list_category, get_product, get_list_for_product, FilterMixin


class ClothesHome(GeneralMixin, ListView):
    model = Catalog
    template_name = "clothes/index.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["head_title"] = True
        context["title"] = "Главная страница"
        return context


class ClothesCatalog(FilterMixin, GeneralMixin, ListView):
    model = BaseProduct
    template_name = "clothes/catalog.html"

    def get_queryset(self):
        category = self.kwargs.get("category")
        return get_catalog_products(self.request, category)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get("category")
        context["catalog"] = get_list_category()
        context["title"] = "Каталог"

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
    extra_context = {'title': f"Yanki | История заказов"}


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


class ClothesFavorite(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/favorite.html"

    def get_queryset(self):
        return get_favorite_products(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Избранное"
        return context


class ClothesAbout(GeneralMixin, ListView):
    model = Product
    template_name = "clothes/o_nas.html"


class ClothesLanguages(View):
    def post(self, request):
        data = decode_json(request.body)
        language = data.get("language")
        request.session["language"] = language
        dict_response = "Ok"
        return json_response({"response": dict_response})


class ClothesMail(View):
    def post(self, request):
        data = decode_json(request.body)
        email = data.get("email")
        text = self.add_mail_mailing(email)
        return json_response({"text": text})

    @staticmethod
    def add_mail_mailing(email):
        span = f"<span class='news__span'>{email}</span>"
        get_text = lambda text: f"Email «{span}»{text} добавлен в рассылку новостей!</div>"
        if Mailing_news.objects.filter(email=email).exists():
            return get_text(" уже")
        else:
            new_email = Mailing_news.objects.create(email=email)
            new_email.save()
            return get_text("")


def pageNotFound(request, exception):
    return HttpResponseNotFound('dappes')
