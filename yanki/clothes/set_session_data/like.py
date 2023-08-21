from django.views import View
from clothes.others import decode_json, json_response
from clothes.utils import Set_data_products, get_select_related_and_selected_fields_products
from yanki.settings import LIKE_SESSION_ID


def get_like_in_bd(request):
    list_like = request.session.get(LIKE_SESSION_ID, [])
    if not list_like:
        if request.user.is_authenticated:
            list_like = list(request.user.like_list.values_list("id", flat=True))
    return list_like


def set_like(data, request):
    like_local = [int(x) for x in data.get(LIKE_SESSION_ID, [])]
    if like_local:
        like_bd = [int(x) for x in get_like_in_bd(request)]
        new_like_list = list(set([*like_bd, *like_local]))
        request.session[LIKE_SESSION_ID] = new_like_list
    return request


class Like(View):
    def post(self, request):
        data = decode_json(request.body)
        product_change_request = data.get(LIKE_SESSION_ID)
        dict_response = self.change_like(product_change_request)
        return json_response(dict_response)

    def change_like(self, data):
        list_like = get_like_in_bd(self.request)

        valid_change = "true"
        product_id = int(data.get("id"))
        sign = data.get("sign")
        where_add = data.get("where_add")

        dict_func = {"+": self.add_product, "delete": self.remove_product}

        func = dict_func[sign]

        list_like, valid_change = func(list_like, product_id, valid_change)

        dict_response = {LIKE_SESSION_ID:
                             {"command": valid_change, "sign": sign, "id": product_id, "list_like": list_like,
                              "where_add": where_add
                              }
                         }

        self.request.session[LIKE_SESSION_ID] = list_like
        return dict_response

    def add_product(self, list_like, product_id, valid_change):
        if product_id not in list_like:
            list_like.append(product_id)

            if product_id not in list_like:
                valid_change = "false"

            if self.request.user.is_authenticated:
                self.request.user.like_list.add(product_id)

        return list_like, valid_change

    def remove_product(self, list_like, product_id, valid_change):
        if product_id in list_like:
            list_like.remove(product_id)

            if product_id in list_like:
                valid_change = "false"

            if self.request.user.is_authenticated:
                self.request.user.like_list.remove(product_id)

        return list_like, valid_change


def get_favorite_products(request):
    list_id = request.session.get(LIKE_SESSION_ID, [])
    if not list_id:
        list_id = get_like_in_bd(request)
    filters = {"parent__id__in": [*list_id]}
    list_products = get_select_related_and_selected_fields_products(filters, "catalog")
    return Set_data_products(list_products, request).products




