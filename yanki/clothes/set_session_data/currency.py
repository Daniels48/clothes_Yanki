from re import findall
from math import ceil
import requests
from django.db.models import Max
from django.views import View
from clothes.models import BaseProduct
from clothes.others import json_response, decode_json
from yanki.settings import CURRENCY_SESSION_ID, CART_SESSION_ID

cache = {}
global_new = "new"
global_old = "old"
base_nominal = "UAH"

currency_list = {base_nominal: "грн", "USD": "$", "EUR": "€"}


def get_list_currency(value):
    return [x for x in currency_list if x != value]


def get_sign(value):
    return currency_list.get(value)


def get_currency_for_page(request):
    currency = request.session.get(CURRENCY_SESSION_ID, base_nominal)
    if currency == base_nominal:
        if request.user.is_authenticated:
            currency = request.user.currency
            if not currency:
                currency = base_nominal
            request.session[CURRENCY_SESSION_ID] = currency
    return currency


def get_valute_value(value):
    get_value = lambda val, sign: float(val.get(sign).get("Value") / val.get(sign).get("Nominal"))
    valutes = cache["Valute"]
    new_value = get_value(valutes, value)
    old_value = get_value(valutes, base_nominal)
    return old_value / new_value


def get_currency_from_server():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    old = {
    "Valute": {
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 90.3846,
            "Previous": 90.8545
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 100.6562,
            "Previous": 101.833
        },
        "UAH": {
            "ID": "R01720",
            "NumCode": "980",
            "CharCode": "UAH",
            "Nominal": 10,
            "Name": "Украинских гривен",
            "Value": 24.5935,
            "Previous": 24.6002
        }
    }
}
    # return requests.get(url, "").json()
    return old


if not len(cache):
    cache = get_currency_from_server()


def set_currency(data, request):
    currency = data.get(CURRENCY_SESSION_ID)
    if currency:
        if request.user.is_authenticated:
            request.user.currency = currency
            request.user.save()
        request.session[CURRENCY_SESSION_ID] = currency
    return request


def get_max_price(request):
    currency = get_currency_for_page(request)
    valute_value = get_valute_value(currency)
    query = BaseProduct.objects.aggregate(Max('price'))
    max_price = ceil(int(query["price__max"]) * valute_value)
    return max_price


class Currency(View):
    def post(self, request):
        response = self.send_local_data(request)
        return json_response(response)

    def send_local_data(self, request):
        currency = get_currency_for_page(request)
        valute_value = get_valute_value(currency)
        max_price = self.get_max_price(request)
        data_dict = {"valute_value": valute_value, "sign": get_sign(currency), "max_price": max_price}
        dict_respone = {"local": currency, "data": data_dict}
        return dict_respone


def get_objects_cart_with_base_price_products(request):
    cart = request.session.get(CART_SESSION_ID)
    get_number = lambda number: float(findall(r"\d+\.?\d*", str(number).replace(",", "."))[0])
    currency = get_currency_for_page(request)
    get_value = lambda product_id, value: get_number(cart[product_id].get(value))
    return {id_pr: get_value(id_pr, "count") * get_value(id_pr, "price") for id_pr in cart}, currency


def get_sum_all_objects_cart_with_currency_price_or_one(request, id_product=0):
    if request.session.get(CART_SESSION_ID):
        cart, currency = get_objects_cart_with_base_price_products(request)
        count_round = 2
        valute_value = get_valute_value(currency)

        get_base_price = lambda product_id: cart.get(product_id)
        get_price_on_currency = lambda product_id: round(get_base_price(product_id) * valute_value, count_round)

        list_product = {id_product: get_base_price(id_product)} if id_product else cart

        price_cart = sum([get_price_on_currency(id_product) for id_product in list_product])

        if currency == base_nominal:
            return int(price_cart)

        round_price_cart = round(price_cart, count_round)
        is_end_zero = str(round_price_cart).split(".")[1] == "0"

        if is_end_zero:
            return int(round_price_cart)

        return round_price_cart
    return 0


def get_dict_response_for_cart(request, id_product):
    currency = get_currency_for_page(request)
    sign = decode_json(request.body).get("sign")
    all_sum = get_sum_all_objects_cart_with_currency_price_or_one(request)
    sum_product = 0 if sign == "delete" else get_sum_all_objects_cart_with_currency_price_or_one(request, id_product)
    return {"sum_cart": all_sum, "product": {"id": id_product, "sum": sum_product, "sign": get_sign(currency)}}



