from math import ceil
from re import findall
from django.db.models import Q, F, ExpressionWrapper, Max
from clothes.models import *
from clothes.others import sum_products
from clothes.set_session_data.currency import get_currency_for_page, get_list_currency, get_sign, get_valute
from users.models import CartProduct
from yanki.settings import CURRENCY_SESSION_ID, CART_SESSION_ID, LIKE_SESSION_ID


def get_cart_in_bd(request):
    if not request.session.get(CART_SESSION_ID):
        if request.user.is_authenticated:
            price = "product__parent__price"
            query_cart = CartProduct.objects.filter(user=request.user). \
                select_related("product__parent").values("product", "count", price)

            cart = {str(item.get("product")): {"count": item.get("count"), "price": float(item.get(price))}
                    for item in query_cart}
            request.session[CART_SESSION_ID] = cart
            return cart
        else:
            return []
    else:
        return request.session.get(CART_SESSION_ID, [])


class GeneralDataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = get_currency_for_page(self.request)
        context[CURRENCY_SESSION_ID] = currency
        context["sign"] = get_sign(currency)
        context["currency_other"] = get_list_currency(currency)
        count = get_cart_in_bd(self.request)
        context["cart_count"] = sum_products(count)
        return context


class GeneralMixin(GeneralDataMixin):
    """General mixin for provide authenticate and currency"""


def get_raw_union_products():
    return Product.objects.select_related("parent", "parent__type", "size", "color")


def get_selected_products(filters=False, types=False):
    general_fields = ["parent__title", "parent__price", "parent__slug",
                      "id", "parent__type__slug", "size__title", "color__hex"]
    list_fields = {"cart": ["image_1", "count"], "catalog": ["image", "parent__tags__title"]}
    general_fields.extend(list_fields.get(types))
    raw_list = get_raw_union_products()
    if not filters:
        filters = {}

    if types != "cart":
        raw_list = raw_list.prefetch_related("parent__tags")

    return raw_list.filter(**filters).only(*general_fields)


def get_catalog_products(category, filters, request):
    currency = get_currency_for_page(request)
    old_vals, new_vals = get_valute(currency)
    sign = get_sign(currency)
    value_sign = old_vals / float(new_vals) if sign != "грн" else 1

    def get_filters(data, names=False):
        elements, list_filters = {}, {}
        size, color, min_price, max_price = [data.get("size"), data.get("color"), data.get("min"), data.get("max")]
        cats = [Q(parent__tags__slug=names) | Q(parent__type__slug=names)] if names else []
        if data:
            elements.update([("size__title__in", size.split(","))]) if size else ""
            elements.update([("color__id__in", color.split(","))]) if color else ""
            elements.update([("newprice__gte", int(min_price))]) if min_price else ""
            elements.update([("newprice__lte", int(max_price))]) if max_price else ""
        pk = "parent_id__in"
        if data or names:
            list_filters[pk] = Product.objects. \
                select_related("parent", "size", "color").\
                annotate(newprice=ExpressionWrapper(F("parent__price") * value_sign,
                                                    output_field=models.DecimalField())).\
                filter(*cats, **elements).values("parent_id")

        return list_filters

    list_filters = get_filters(filters, category)
    list_query = get_selected_products(list_filters, "catalog")
    return Set_data_products(list_query, request).products


def get_list_category():
    return Tag.objects.all().only("title", "slug").union(Catalog.objects.all().only("title", "slug"), all=True)


def get_product(name, request):
    list_products = get_raw_union_products().filter(parent__slug=name)
    return Set_data_products(list_products, request, False, True).product


def get_list_for_product(request):
    list_query = get_selected_products(types="catalog")
    return Set_data_products(list_query, request).products


def get_max_price(request):
    currency = get_currency_for_page(request)
    old_vals, new_vals = get_valute(currency)
    sign = get_sign(currency)
    value_sign = old_vals / new_vals if sign != "грн" else 1
    query = BaseProduct.objects.aggregate(Max('price'))
    raw_value = int(query["price__max"]) * value_sign
    return ceil(raw_value)


def sort_size(lst):
    list_size = {"XXS": 40, "XS": 44, "S": 46, "M": 48, "L": 50, "XL": 52, "XXL": 54, "3XL": 58}
    return sorted(lst, key=lambda elem: list_size[elem])


def calc_color(string):
    return sum([int(items, 16) for items in findall(r"\w{2}", string=string.upper())])


def sort_color(lst):
    return sorted(lst, key=lambda elem: calc_color(elem), reverse=True)


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
        self.old_value = None
        self.new_value = None
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
        if self.sign is None or self.old_value is None or self.new_value is None:
            currency = get_currency_for_page(self.request)
            self.sign = get_sign(currency)
            self.old_value, self.new_value = get_valute(currency)

        id_element = element.parent_id
        if id_element not in self.list_cateogry_obj and not self.one:
            self.set_f_price(element)

        if self.one:
            self.set_f_price(element)

    def set_f_price(self, element):
        price = element.parent.price
        if self.sign != "грн":
            element.f_price = f"{round(float(price) * self.old_value / float(self.new_value), 2)} {self.sign}"
        else:
            element.f_price = f"{int(price)} {self.sign}"

    def set_like(self, element):
        if self.list_like is None:
            self.list_like = self.request.session.get(LIKE_SESSION_ID, [])

        id_element = element.parent_id
        if id_element not in self.list_cateogry_obj and not self.one:
            value_like = str(id_element) in self.list_like or id_element in self.list_like
            element.like = value_like

        if self.one:
            value_like = str(id_element) in self.list_like or id_element in self.list_like
            element.like = value_like

    def sort_size_and_color(self, element):
        if self.search:
            element.size = sort_size(element.size)
            element.color = sort_color(element.color)
        else:
            element.size.title = sort_size(element.size.title)
            element.color.hex = sort_color(element.color.hex)

    def sort_size_one_product(self):
        for key, value in self.list_size.items():
            self.list_size[key] = sorted(value, key=lambda item: item.size.id, reverse=True)
        return self.list_size

    def sort_color_one_product(self):
        return sorted(self.list_color, key=lambda obj: calc_color(obj.color.hex), reverse=True)

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

    def set_full_data(self, element):
        if self.one:
            self.set_color_product(element)
            self.set_size_product(element)
        else:
            self.set_like(element)
            self.set_currency(element)
            new_element = self.set_category(element)
            self.sort_size_and_color(new_element)

    def set_category(self, item):

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

        return list(self.list_cateogry_obj.values())


