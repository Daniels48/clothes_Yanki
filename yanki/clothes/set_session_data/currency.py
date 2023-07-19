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


def get_currency_for_page(data):
    currency = data.session.get(CURRENCY_SESSION_ID, base_nominal)
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
            "Value": 82.6417,
            "Previous": 82.093
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 89.0057,
            "Previous": 88.0379
        },
        "UAH": {
            "ID": "R01720",
            "NumCode": "980",
            "CharCode": "UAH",
            "Nominal": 10,
            "Name": "Украинских гривен",
            "Value": 22.3769,
            "Previous": 22.2267
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
        request.session[CURRENCY_SESSION_ID] = currency
    return request


def set_currency_for_page(list_products, request):
    def set_data(products_list):
        for item in products_list:
            if sign != "грн":
                item.f_price = f"{round(float(item.parent.price) * old_vals / float(new_vals), 2)} {sign}"
            else:
                item.f_price = f"{int(item.parent.price)} {sign}"
        return products_list

    currency = get_currency_for_page(request)
    sign = get_sign(currency)
    old_vals, new_vals = get_valute(currency)

    if type(list_products) != list:
        products = set_data([list_products])
        return products[0]

    products = set_data(list_products)

    return products


class Currency(View):
    def post(self, request):
        response = send_local_data(request)
        return json_response(response)


def get_valute(value):
    get_value = lambda val, sign: val.get(sign).get("Value") / val.get(sign).get("Nominal")
    valutes = cache["Valute"]
    new_value = get_value(valutes, value)
    old_value = get_value(valutes, base_nominal)
    return float(old_value), float(new_value)


def send_local_data(request):
    currency = get_currency_for_page(request)
    old_value, new_value = get_valute(currency)
    sign = get_sign(currency)
    value_sign = old_value / new_value if sign != "грн" else 1
    query = BaseProduct.objects.aggregate(Max('price'))
    raw_value = int(query["price__max"]) * value_sign
    return {"local": currency,
           "data": {"new": new_value, "old": old_value, "sign": currency_list[currency], "max_price": ceil(raw_value)}}


def get_number(number):
    return re.findall(r"\d+\.?\d*", str(number).replace(",", "."))[0]


def get_raw_list_product_sum_price(request):
    cart = request.session.get(CART_SESSION_ID)
    currency = get_currency_for_page(request)
    get_value = lambda product, value: get_number(cart[product].get(value))
    return {id_pr: float(get_value(id_pr, "count")) * float(get_value(id_pr, "price")) for id_pr in cart}, currency


def get_sum_products(list_sum, currency, id_product=0):
    count_round = 2
    old_value, new_value = get_valute(currency)
    get_value = lambda p_id: round(list_sum.get(p_id) * old_value / new_value, count_round)
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



