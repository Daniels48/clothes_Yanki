from django.views import View
from clothes.others import json_response
from clothes.set_session_data.cart import set_local_cart
from yanki.settings import CART_SESSION_ID, LIKE_SESSION_ID, CURRENCY_SESSION_ID


class Set_local_data(View):
    def post(self, request):
        obj = {}

        if request.session.get(CART_SESSION_ID):
            products = request.session.get(CART_SESSION_ID)
            obj[CART_SESSION_ID] = set_local_cart(products)

        if request.session.get(CURRENCY_SESSION_ID):
            obj[CURRENCY_SESSION_ID] = 5

        if request.session.get(LIKE_SESSION_ID):
            obj[LIKE_SESSION_ID] = 5

        finally_obj = {"data": obj}

        return json_response(finally_obj)