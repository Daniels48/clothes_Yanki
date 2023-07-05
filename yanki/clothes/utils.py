from re import findall
from django.db.models import Q
from clothes.models import *
from clothes.others import sum_products
from clothes.set_session_data.currency import get_currency_for_page, get_list_currency, get_sign
from clothes.utilits.Products import calc_color, get_finished_products
from yanki.settings import CURRENCY_SESSION_ID, CART_SESSION_ID


class GeneralDataMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        currency = get_currency_for_page(self.request)
        context[CURRENCY_SESSION_ID] = currency
        context["sign"] = get_sign(currency)
        context["currency_other"] = get_list_currency(currency)
        context["cart_count"] = sum_products(self.request.session.get(CART_SESSION_ID, {}))
        return context


class GeneralMixin(GeneralDataMixin):
    """General mixin for provide authenticate and currency"""


def get_raw_union_products():
    return Product.objects.distinct().select_related("parent", "parent__type", "size", "color")


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


def get_catalog_products(category, filters):
    def get_filters(data, names=False):
        elements, list_filters = {}, {}
        size, color, min_price, max_price = [data.get("size"), data.get("color"), data.get("min"), data.get("max")]
        cats = [Q(parent__tags__slug=names) | Q(parent__type__slug=names)] if names else []
        if data:
            elements.update([("size__title__in", size.split(","))]) if size else ""
            elements.update([("color__hex__in", color.split(","))]) if color else ""
            elements.update([("parent__price__gte", int(min_price))]) if min_price else ""
            elements.update([("parent__price__lte", int(max_price))]) if max_price else ""
        pk = "parent_id__in"
        if data or names:
            list_filters[pk] = Product.objects.distinct(). \
                select_related("parent", "size", "color").filter(*cats, **elements).values("parent_id")

        return list_filters

    list_filters = get_filters(filters, category)
    raw_list = get_selected_products(list_filters, "catalog")
    return get_finished_products(raw_list)


def get_list_category():
    return Tag.objects.all().only("title", "slug").union(Catalog.objects.all().only("title", "slug"), all=True)


def get_product(name):
    def re_context(key, obj):
        data = {"care": {"pattern": r"-[\s\w]+", "string": obj.parent.care},
                "composition": {"pattern": r"\w+:(?:\s\d+%\s\w+,?)+", "string": obj.parent.composition}}
        pattern = data[key]["pattern"]
        string = data[key]["string"]
        return "<br>".join(findall(pattern, string))

    def get_sizes_product(lst_objs):
        list_objects = {}
        for obj in lst_objs:
            clr = obj.color.hex
            if clr not in list_objects:
                list_objects[clr] = [obj]
            else:
                list_objects[clr].append(obj)

        for key, value in list_objects.items():
            list_objects[key] = sorted(value, key=lambda item: item.size.id, reverse=True)

        return list_objects

    def get_colors_product(lst_objs):
        lst_raw, lst = [], []
        [(lst.append(obj), lst_raw.append(obj.color.id)) for obj in lst_objs if obj.color.id not in lst_raw]
        return sorted(lst, key=lambda obj: calc_color(obj.color.hex), reverse=True)

    list_products = get_raw_union_products().filter(parent__slug=name)
    list_products[0].colors = get_colors_product(list_products)
    list_products[0].sizes = get_sizes_product(list_products)
    list_products[0].care = re_context("care", list_products[0])
    list_products[0].composition = re_context("composition", list_products[0])
    return list_products[0]


def get_list_for_product():
    raw_list = get_selected_products(types="catalog")
    return get_finished_products(raw_list)

