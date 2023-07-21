import re
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


def get_currency_for_page(request):

    currency = request.session.get(CURRENCY_SESSION_ID, base_nominal)
    if currency == base_nominal:
        if request.user.is_authenticated:
            currency = request.user.currency
            if not currency:
                currency = base_nominal
            request.session[CURRENCY_SESSION_ID] = currency
    return currency


def get_sign(value):
    return currency_list.get(value)


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


class Currency(View):
    def post(self, request):
        response = send_local_data(request)
        return json_response(response)


def get_valute_value(value):
    get_value = lambda val, sign: val.get(sign).get("Value") / val.get(sign).get("Nominal")
    valutes = cache["Valute"]
    new_value = get_value(valutes, value)
    old_value = get_value(valutes, base_nominal)
    return float(old_value) / float(new_value)


def send_local_data(request):
    currency = get_currency_for_page(request)
    valute_value = get_valute_value(currency)
    query = BaseProduct.objects.aggregate(Max('price'))
    raw_value = int(query["price__max"]) * valute_value
    return {"local": currency,
           "data": {"valute_value": valute_value, "sign": currency_list[currency], "max_price": ceil(raw_value)}}


def get_number(number):
    return re.findall(r"\d+\.?\d*", str(number).replace(",", "."))[0]


def get_raw_list_product_sum_price(request):
    cart = request.session.get(CART_SESSION_ID)
    currency = get_currency_for_page(request)
    get_value = lambda product, value: get_number(cart[product].get(value))
    return {id_pr: float(get_value(id_pr, "count")) * float(get_value(id_pr, "price")) for id_pr in cart}, currency


def get_sum_products(list_sum, currency, id_product=0):
    count_round = 2
    valute_value = get_valute_value(currency)
    get_value = lambda p_id: round(list_sum.get(p_id) * valute_value, count_round)
    list_product = {id_product: list_sum.get(id_product)} if id_product else list_sum
    row_value = sum([get_value(id_p) for id_p in list_product])
    if currency == base_nominal:
        return int(row_value)
    else:
        fvalue = round(row_value, count_round)
        if str(fvalue).split(".")[1] == "0":
            return int(fvalue)
        return fvalue


def get_all_sum_or_one(request, id_product=0):
    if request.session.get(CART_SESSION_ID):
        cart, currency = get_raw_list_product_sum_price(request)
        return get_sum_products(cart, currency, id_product)
    else:
        return 0


def get_local_data_for_cart(request, id_product):
    currency = get_currency_for_page(request)
    sign = decode_json(request.body).get("sign")
    cart = request.session.get(CART_SESSION_ID)
    all_sum = get_all_sum_or_one(request) if cart else 0
    sum_product = 0 if sign == "delete" else get_all_sum_or_one(request, id_product)
    return {"sum_cart": all_sum, "product": {"id": id_product, "sum": sum_product, "sign": get_sign(currency)}}



