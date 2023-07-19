from django.db.models import Window, IntegerField, F, Count
from django.db.models.functions import RowNumber
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django_cte import With

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
    model = Product
    template_name = "clothes/person.html"

    # text_query_id = f"SELECT parent_id FROM clothes_product AS {name_pr}" \
    #                 f" JOIN clothes_baseproduct AS {name_bpr} on {name_bpr}.id = {name_pr}.parent_id" \
    #                 f" JOIN clothes_catalog AS {name_cc} on {name_bpr}.type_id = {name_cc}.id" \
    #                 f" JOIN clothes_size AS sz on sz.id = {name_pr}.size_id" \
    #                 f" JOIN clothes_color AS clr on clr.id = {name_pr}.color_id WHERE {filters}"
    #
    #
    #
    # text_query_product = f'SELECT {name_pr}.id as pid, ' \
    #                      f'{name_pr}.image as image, ' \
    #                      f'{name_bpr}.title as title, ' \
    #                      f'{name_bpr}.price as price,' \
    #                      f'{name_bpr}.id as id, ' \
    #                      f'{name_bpr}.slug as slug, ' \
    #                      f'{name_bpr}.price as price, ' \
    #                      f'sz.title as csize , ' \
    #                      f'clr.hex as chex, ' \
    #                      f'{name_bpr}.type_id as cid,' \
    #                      f'{name_cc}.slug as ccslug, ' \
    #                      f'{name_cc}.title as cctitle, ' \
    #                      f'count({name_bpr}.id) OVER(partition by {name_bpr}.id, {name_cc}.id) as cnt_all, ' \
    #                      f'count({name_cc}.title) OVER(partition by {name_cc}.title, {name_bpr}.id) as cnt ' \
    #                      f'FROM clothes_product AS {name_pr}' \
    #                      f' JOIN clothes_baseproduct AS {name_bpr} on {name_bpr}.id = {name_pr}.parent_id' \
    #                      f' JOIN clothes_catalog AS {name_cc} on {name_bpr}.type_id = {name_cc}.id' \
    #                      f' JOIN clothes_size AS sz on sz.id = {name_pr}.size_id' \
    #                      f' JOIN clothes_color AS clr on clr.id = {name_pr}.color_id' \
    #                      f' WHERE {name_pr}.parent_id IN ({text_query_id})'
    #
    # text_query_product2 = f"with base_select AS ({text_query_product}), calc_v as (SELECT " \
    #                       f"bs.id as id, " \
    #                       f"bs.cid as cid, " \
    #                       f"count(*) over() as cnt_all, " \
    #                       f"count(*) over(partition by cid) cnt " \
    #                       f"FROM base_select as bs group by 1, 2)" \
    #                       f" select bs.*, cv.cnt_all, cv.cnt from base_select as bs join calc_v as cv using(id);"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        person = User.objects.get(id=self.request.user.id)
        context["form"] = Change_person_data(instance=person)

        # # only("image", "parent__price", "parent__title", "size__title", "color__hex",
        # #      "parent__type__id", "parent__type__title", "parent__type__slug").
        #
        #
        # sub_query = BaseProduct.objects.filter(id=1).prefetch_related("tags").values("id")
        # query = Product.objects.select_related("parent", "parent__type", "size", "color"). \
        #     prefetch_related("parent__tags").filter(parent__in=sub_query).\
        #     only("id", "parent", "image", "parent__title", "parent__price", "parent__type__title",
        #          "size__title", "color__hex").annotate(ctitle=F("parent__type__title"), bid=F("parent"))
        #
        #
        # cnt_all = Window(
        #     expression=Count("*")
        # )
        # cnt = Window(
        #     expression=Count("*"),
        #     partition_by=F('ctitle')
        # )
        # # text_query_product2 = f"with base_select AS ({text_query_product}), calc_v as (SELECT " \
        # #                       f"bs.id as id, " \
        # #                       f"bs.cid as cid, " \
        # #                       f"count(*) over() as cnt_all, " \
        # #                       f"count(*) over(partition by cid) cnt " \
        # #                       f"FROM base_select as bs group by 1, 2)" \
        # #                       f" select bs.*, cv.cnt_all, cv.cnt from base_select as bs join calc_v as cv using(id);"
        # cte1 = With(query, name="cte1")
        # cte3 = With(cte1.queryset().values("parent", "ctitle").annotate(c=Count("parent"),cnt_all=cnt_all, cnt=cnt), name="cte2")
        # # cte2 = With(query).join(With(cte1.annotate(cnt_all=cnt_all, cnt=cnt)).queryset())
        # #
        # # result1 = cte3.queryset().join(cte1.queryset())
        #
        # res = cte1.join(cte3.queryset(), parent=cte1.col.parent_id).\
        #     with_cte(cte1).\
        #     with_cte(cte3)
        # #
        # # result = Product.objects.with_cte(cte1)
        #
        #
        # for x in res:
        #     print(x, 2222222222)



        return context

    def post(self, request):
        data = decode_json(request.body)
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
