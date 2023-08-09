from re import findall
from django.db.models import Q, F, ExpressionWrapper
from clothes.models import *
from clothes.others import sum_products
from clothes.set_session_data.currency import get_currency_for_page, get_list_currency, get_sign, get_valute_value, \
    get_max_price
from yanki.settings import CURRENCY_SESSION_ID, CART_SESSION_ID, LIKE_SESSION_ID


class GeneralDataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = get_currency_for_page(self.request)
        context[CURRENCY_SESSION_ID] = currency
        context["sign"] = get_sign(currency)
        list_language = ["RU", "EN"]
        context["currency_other"] = get_list_currency(currency)
        language = self.request.session.get("language", "RU")
        context["language"] = language
        context["other_language"] = [x for x in list_language if x != language][0]
        cart = self.request.session.get(CART_SESSION_ID, [])
        context["cart_count"] = sum_products(cart)
        return context


class GeneralMixin(GeneralDataMixin):
    """General mixin for provide authenticate and currency"""


class FilterMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["size"] = Size.objects.all()
        context["color"] = Color.objects.all()
        context["max"] = get_max_price(self.request)
        return context


def get_select_related_products():
    return Product.objects.select_related("parent", "parent__type", "size", "color")


def get_list_category():
    return Tag.objects.all().only("title", "slug", "title_en", "title_ru").\
        union(Catalog.objects.all().only("title", "slug", "title_en", "title_ru"), all=True)


def get_select_related_and_selected_fields_products(filters=False, types=False):
    select_related_products = get_select_related_products()
    general_fields = ["parent__title", "parent__price", "parent__slug", "id", "parent__type__slug", "parent__title_en",
                      "parent__title_ru",
                      "size__title", "color__hex"]
    list_fields = {"cart": ["image_1", "count"], "catalog": ["image", "parent__tags__title"]}
    general_fields.extend(list_fields.get(types))

    if not filters:
        filters = {}

    if types != "cart":
        select_related_products = select_related_products.prefetch_related("parent__tags")

    return select_related_products.filter(**filters).only(*general_fields)


def get_catalog_products(request, category):
    filter_parent = {}
    dict_params = request.GET

    if dict_params or category:
        currency = get_currency_for_page(request)
        valute_value = get_valute_value(currency)

        sub_query_filters = {}
        size, color, min_price, max_price = [dict_params.get("size"), dict_params.get("color"),
                                             dict_params.get("min"), dict_params.get("max")]

        category_filters = [Q(parent__tags__slug=category) | Q(parent__type__slug=category)] if category else []
        sub_query_filters.update([("size__title__in", size.split(","))]) if size else ""
        sub_query_filters.update([("color__id__in", color.split(","))]) if color else ""
        sub_query_filters.update([("newprice__gte", int(min_price))]) if min_price else ""
        sub_query_filters.update([("newprice__lte", int(max_price))]) if max_price else ""

        new_price = ExpressionWrapper(F("parent__price") * valute_value, output_field=models.DecimalField())

        list_id_subquery = get_select_related_products().annotate(newprice=new_price). \
            filter(*category_filters, **sub_query_filters).values("parent_id")

        filter_parent["parent_id__in"] = list_id_subquery

    list_query = get_select_related_and_selected_fields_products(filter_parent, "catalog")
    return Set_data_products(list_query, request).products


def get_product(name, request):
    list_query = get_select_related_products().filter(parent__slug=name)
    return Set_data_products(list_query, request, False, True).product


def get_list_for_product(request):
    list_query = get_select_related_and_selected_fields_products(types="catalog")
    return Set_data_products(list_query, request).products


def decorator(func):
    from datetime import datetime

    def wrapper(*args, **kwargs):
        time_init = datetime.now()
        result = func(*args, **kwargs)
        time_finish = datetime.now()
        print(f'Время работы функции: = {time_finish-time_init}')
        return result
    return wrapper


class Set_data_products:
    def __init__(self, list_products, request, search=False, one=False):
        self.one = one
        self.list_products = list_products
        self.request = request
        self.search = search
        self.list_like = None
        self.sign = None
        self.valute_value = None
        self.list_cateogry_obj = {}

        if self.one:
            self.product = None
            self.list_size = {}
            self.list_color = []
            self.id_color = []
            self.product = self.get_full_products()
        else:
            self.products = self.get_full_products()

    def set_currency(self, element):
        if self.sign is None or self.valute_value is None:
            currency = get_currency_for_page(self.request)
            self.sign = get_sign(currency)
            self.valute_value = get_valute_value(currency)

        price = element.parent.price
        if self.sign != "грн":
            element.f_price = f"{round(float(price) * self.valute_value, 2)} {self.sign}"
        else:
            element.f_price = f"{int(price)} {self.sign}"

    def set_like(self, element):
        if self.list_like is None:
            self.list_like = self.request.session.get(LIKE_SESSION_ID, [])

        id_element = element.parent_id if not self.search else element.id
        value_like = str(id_element) in self.list_like or id_element in self.list_like
        element.like = value_like

    def sort_color(self, lst):
        return sorted(lst, key=lambda elem: self.calc_color_weight(elem), reverse=True)

    @staticmethod
    def sort_size(lst):
        list_size = {"XXS": 40, "XS": 44, "S": 46, "M": 48, "L": 50, "XL": 52, "XXL": 54, "3XL": 58}
        return sorted(lst, key=lambda elem: list_size[elem])

    @staticmethod
    def calc_color_weight(string):
        return sum([int(items, 16) for items in findall(r"\w{2}", string=string.upper())])

    def sort_size_and_color(self, element):
        if self.search:
            element.size = self.sort_size(element.size)
            element.color = self.sort_color(element.color)
        else:
            element.size.title = self.sort_size(element.size.title)
            element.color.hex = self.sort_color(element.color.hex)

    def sort_size_one_product(self):
        for key, value in self.list_size.items():
            self.list_size[key] = sorted(value, key=lambda item: item.size.id, reverse=True)
        return self.list_size

    def sort_color_one_product(self):
        return sorted(self.list_color, key=lambda obj: self.calc_color_weight(obj.color.hex), reverse=True)

    def set_size_product(self, element):
        clr = element.color.hex

        if not self.product:
            self.product = element

        if clr not in self.list_size:
            self.list_size[clr] = [element]
        else:
            self.list_size[clr].append(element)

    def set_color_product(self, element):
        id_color = element.color.id

        if not self.product:
            self.product = element

        if id_color not in self.id_color:
            self.id_color.append(id_color)
            self.list_color.append(element)

    def set_re_context_one_product(self, key):
        data = {"care": {"pattern": r"-[\s\w]+", "string": self.product.parent.care},
                "composition": {"pattern": r"\w+:(?:\s\d+%\s\w+,?)+", "string": self.product.parent.composition}}
        pattern = data[key]["pattern"]
        string = data[key]["string"]
        return "<br>".join(findall(pattern, string))

    def set_parent_products(self, item):

        if item.parent_id not in self.list_cateogry_obj:
            item.color.hex = [item.color.hex, ]
            item.size.title = [item.size.title, ]
            self.list_cateogry_obj[item.parent_id] = item
            return item

        else:
            old_item = self.list_cateogry_obj[item.parent_id]
            old_item.color.hex = {*old_item.color.hex, item.color.hex}
            old_item.size.title = {*old_item.size.title, item.size.title}
            self.list_cateogry_obj[item.parent_id] = old_item
            return old_item

    def set_full_data(self, element):
        if self.one:
            self.set_color_product(element)
            self.set_size_product(element)
        else:
            self.set_like(element)
            self.set_currency(element)
            new_element = element
            if not self.search:
                new_element = self.set_parent_products(element)
            self.sort_size_and_color(new_element)

    def get_full_products(self):
        [self.set_full_data(item) for item in self.list_products]

        if self.one:
            self.product.care = self.set_re_context_one_product("care")
            self.product.composition = self.set_re_context_one_product("composition")
            self.product.sizes = self.sort_size_one_product()
            self.product.colors = self.sort_color_one_product()
            self.set_like(self.product)
            self.set_currency(self.product)
            return self.product

        if self.search:
            return self.list_products

        return list(self.list_cateogry_obj.values())


