from django.views import View
from clothes.others import decode_json, json_response
from clothes.utils import get_selected_products, Set_data_products
from yanki.settings import LIKE_SESSION_ID


def set_like(data, request):
    like = data.get(LIKE_SESSION_ID)
    if like:
        request.session[LIKE_SESSION_ID] = change_like(like, request)
        if not request.session[LIKE_SESSION_ID]:
            del request.session[LIKE_SESSION_ID]
    return request


def get_like_in_bd(request):
    if request.user.is_authenticated:
        like_list = list(request.user.like_list.values_list("id", flat=True))
        request.session[LIKE_SESSION_ID] = like_list
        return like_list
    else:
        return []


def change_like(data, request):
    list_like = request.session.get(LIKE_SESSION_ID, [])

    is_authenticated = request.user.is_authenticated

    if not list_like:
        list_like = get_like_in_bd(request)

    product_id = data.get("id")
    sign = data.get("sign")

    if sign == "+":
        if product_id not in list_like:
            list_like.append(product_id)
            if is_authenticated:
                request.user.like_list.add(product_id)

    if sign == "delete":
        if product_id in list_like:
            list_like.remove(product_id)
            if is_authenticated:
                request.user.like_list.remove(product_id)

    return list_like


class Like(View):
    def post(self, request):
        data = decode_json(request.body)
        like = data.get(LIKE_SESSION_ID)
        sign = like.get("sign")
        id_product = like.get("id")
        where_add = like.get("where_add")
        list_like = request.session.get(LIKE_SESSION_ID, [])
        val = "true"
        if sign == "+":
            if id_product not in list_like:
                val = "false"
        if sign == "delete":
            if id_product in list_like:
                val = "false"

        obj = {LIKE_SESSION_ID: {"command": val, "sign": sign, "id": id_product,
                                 "list_like": list_like, "where_add": where_add}}

        return json_response(obj)


def get_list_favorite(request):
    list_id = request.session.get(LIKE_SESSION_ID, [])
    if not list_id:
        list_id = get_like_in_bd(request)
    filters = {"parent__id__in": [*list_id]}
    list_products = get_selected_products(filters, "catalog")
    return Set_data_products(list_products, request).products


def set_like_cls_for_product(list_product, request):
    list_like = request.session.get(LIKE_SESSION_ID, [])
    set_like = lambda x: str(x.parent.id) in list_like

    if type(list_product) != list:
        list_product.like = set_like(list_product)
        return list_product

    for x in list_product:
        x.like = set_like(x)
    return list_product
