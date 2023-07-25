from django.views import View
from clothes.others import json_response
from clothes.set_session_data.cart import set_local_cart

from yanki.settings import CART_SESSION_ID, LIKE_SESSION_ID, CURRENCY_SESSION_ID


class get_local_data(View):
    def post(self, request):
        dict_response = {}
        cart = request.session.get(CART_SESSION_ID)
        currency = request.session.get(CURRENCY_SESSION_ID)
        like = request.session.get(LIKE_SESSION_ID)

        if cart:
            dict_response[CART_SESSION_ID] = set_local_cart(cart)

        if currency:
            dict_response[CURRENCY_SESSION_ID] = currency

        if like:
            dict_response[LIKE_SESSION_ID] = like

        return json_response({"data": dict_response})
