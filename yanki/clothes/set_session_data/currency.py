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
    "Date": "2023-06-10T11:30:00+03:00",
    "PreviousDate": "2023-06-09T11:30:00+03:00",
    "PreviousURL": "\/\/www.cbr-xml-daily.ru\/archive\/2023\/06\/09\/daily_json.js",
    "Timestamp": "2023-06-12T20:00:00+03:00",
    "Valute": {
        "AUD": {
            "ID": "R01010",
            "NumCode": "036",
            "CharCode": "AUD",
            "Nominal": 1,
            "Name": "Австралийский доллар",
            "Value": 55.4361,
            "Previous": 54.6904
        },
        "AZN": {
            "ID": "R01020A",
            "NumCode": "944",
            "CharCode": "AZN",
            "Nominal": 1,
            "Name": "Азербайджанский манат",
            "Value": 48.6128,
            "Previous": 48.29
        },
        "GBP": {
            "ID": "R01035",
            "NumCode": "826",
            "CharCode": "GBP",
            "Nominal": 1,
            "Name": "Фунт стерлингов Соединенного королевства",
            "Value": 103.5914,
            "Previous": 102.3043
        },
        "AMD": {
            "ID": "R01060",
            "NumCode": "051",
            "CharCode": "AMD",
            "Nominal": 100,
            "Name": "Армянских драмов",
            "Value": 21.3998,
            "Previous": 21.2105
        },
        "BYN": {
            "ID": "R01090B",
            "NumCode": "933",
            "CharCode": "BYN",
            "Nominal": 1,
            "Name": "Белорусский рубль",
            "Value": 28.0607,
            "Previous": 27.9685
        },
        "BGN": {
            "ID": "R01100",
            "NumCode": "975",
            "CharCode": "BGN",
            "Nominal": 1,
            "Name": "Болгарский лев",
            "Value": 45.3676,
            "Previous": 44.9825
        },
        "BRL": {
            "ID": "R01115",
            "NumCode": "986",
            "CharCode": "BRL",
            "Nominal": 1,
            "Name": "Бразильский реал",
            "Value": 16.8258,
            "Previous": 16.7141
        },
        "HUF": {
            "ID": "R01135",
            "NumCode": "348",
            "CharCode": "HUF",
            "Nominal": 100,
            "Name": "Венгерских форинтов",
            "Value": 24.0889,
            "Previous": 23.8358
        },
        "VND": {
            "ID": "R01150",
            "NumCode": "704",
            "CharCode": "VND",
            "Nominal": 10000,
            "Name": "Вьетнамских донгов",
            "Value": 34.8449,
            "Previous": 34.6179
        },
        "HKD": {
            "ID": "R01200",
            "NumCode": "344",
            "CharCode": "HKD",
            "Nominal": 1,
            "Name": "Гонконгский доллар",
            "Value": 10.5626,
            "Previous": 10.4951
        },
        "GEL": {
            "ID": "R01210",
            "NumCode": "981",
            "CharCode": "GEL",
            "Nominal": 1,
            "Name": "Грузинский лари",
            "Value": 31.6611,
            "Previous": 31.4087
        },
        "DKK": {
            "ID": "R01215",
            "NumCode": "208",
            "CharCode": "DKK",
            "Nominal": 1,
            "Name": "Датская крона",
            "Value": 11.9108,
            "Previous": 11.8102
        },
        "AED": {
            "ID": "R01230",
            "NumCode": "784",
            "CharCode": "AED",
            "Nominal": 1,
            "Name": "Дирхам ОАЭ",
            "Value": 22.4998,
            "Previous": 22.3504
        },
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
        "EGP": {
            "ID": "R01240",
            "NumCode": "818",
            "CharCode": "EGP",
            "Nominal": 10,
            "Name": "Египетских фунтов",
            "Value": 26.746,
            "Previous": 26.5684
        },
        "INR": {
            "ID": "R01270",
            "NumCode": "356",
            "CharCode": "INR",
            "Nominal": 10,
            "Name": "Индийских рупий",
            "Value": 10.0394,
            "Previous": 99.5595
        },
        "IDR": {
            "ID": "R01280",
            "NumCode": "360",
            "CharCode": "IDR",
            "Nominal": 10000,
            "Name": "Индонезийских рупий",
            "Value": 55.4531,
            "Previous": 55.1886
        },
        "KZT": {
            "ID": "R01335",
            "NumCode": "398",
            "CharCode": "KZT",
            "Nominal": 100,
            "Name": "Казахстанских тенге",
            "Value": 18.5774,
            "Previous": 18.3797
        },
        "CAD": {
            "ID": "R01350",
            "NumCode": "124",
            "CharCode": "CAD",
            "Nominal": 1,
            "Name": "Канадский доллар",
            "Value": 61.8668,
            "Previous": 61.3734
        },
        "QAR": {
            "ID": "R01355",
            "NumCode": "634",
            "CharCode": "QAR",
            "Nominal": 1,
            "Name": "Катарский риал",
            "Value": 22.7038,
            "Previous": 22.553
        },
        "KGS": {
            "ID": "R01370",
            "NumCode": "417",
            "CharCode": "KGS",
            "Nominal": 100,
            "Name": "Киргизских сомов",
            "Value": 94.3618,
            "Previous": 93.8099
        },
        "CNY": {
            "ID": "R01375",
            "NumCode": "156",
            "CharCode": "CNY",
            "Nominal": 1,
            "Name": "Китайский юань",
            "Value": 11.5716,
            "Previous": 11.4896
        },
        "MDL": {
            "ID": "R01500",
            "NumCode": "498",
            "CharCode": "MDL",
            "Nominal": 10,
            "Name": "Молдавских леев",
            "Value": 46.3028,
            "Previous": 46.0457
        },
        "NZD": {
            "ID": "R01530",
            "NumCode": "554",
            "CharCode": "NZD",
            "Nominal": 1,
            "Name": "Новозеландский доллар",
            "Value": 50.3288,
            "Previous": 49.6334
        },
        "NOK": {
            "ID": "R01535",
            "NumCode": "578",
            "CharCode": "NOK",
            "Nominal": 10,
            "Name": "Норвежских крон",
            "Value": 76.7254,
            "Previous": 74.9701
        },
        "PLN": {
            "ID": "R01565",
            "NumCode": "985",
            "CharCode": "PLN",
            "Nominal": 1,
            "Name": "Польский злотый",
            "Value": 19.9714,
            "Previous": 19.6809
        },
        "RON": {
            "ID": "R01585F",
            "NumCode": "946",
            "CharCode": "RON",
            "Nominal": 1,
            "Name": "Румынский лей",
            "Value": 17.9472,
            "Previous": 17.7764
        },
        "XDR": {
            "ID": "R01589",
            "NumCode": "960",
            "CharCode": "XDR",
            "Nominal": 1,
            "Name": "СДР (специальные права заимствования)",
            "Value": 109.9209,
            "Previous": 109.2026
        },
        "SGD": {
            "ID": "R01625",
            "NumCode": "702",
            "CharCode": "SGD",
            "Nominal": 1,
            "Name": "Сингапурский доллар",
            "Value": 61.5122,
            "Previous": 60.8863
        },
        "TJS": {
            "ID": "R01670",
            "NumCode": "972",
            "CharCode": "TJS",
            "Nominal": 10,
            "Name": "Таджикских сомони",
            "Value": 75.7312,
            "Previous": 75.2263
        },
        "THB": {
            "ID": "R01675",
            "NumCode": "764",
            "CharCode": "THB",
            "Nominal": 10,
            "Name": "Таиландских батов",
            "Value": 23.8852,
            "Previous": 23.5602
        },
        "TRY": {
            "ID": "R01700J",
            "NumCode": "949",
            "CharCode": "TRY",
            "Nominal": 10,
            "Name": "Турецких лир",
            "Value": 35.4044,
            "Previous": 35.6279
        },
        "TMT": {
            "ID": "R01710A",
            "NumCode": "934",
            "CharCode": "TMT",
            "Nominal": 1,
            "Name": "Новый туркменский манат",
            "Value": 23.6119,
            "Previous": 23.4551
        },
        "UZS": {
            "ID": "R01717",
            "NumCode": "860",
            "CharCode": "UZS",
            "Nominal": 10000,
            "Name": "Узбекских сумов",
            "Value": 72.271,
            "Previous": 71.6781
        },
        "UAH": {
            "ID": "R01720",
            "NumCode": "980",
            "CharCode": "UAH",
            "Nominal": 10,
            "Name": "Украинских гривен",
            "Value": 22.3769,
            "Previous": 22.2267
        },
        "CZK": {
            "ID": "R01760",
            "NumCode": "203",
            "CharCode": "CZK",
            "Nominal": 10,
            "Name": "Чешских крон",
            "Value": 37.5559,
            "Previous": 37.2135
        },
        "SEK": {
            "ID": "R01770",
            "NumCode": "752",
            "CharCode": "SEK",
            "Nominal": 10,
            "Name": "Шведских крон",
            "Value": 76.4133,
            "Previous": 75.4642
        },
        "CHF": {
            "ID": "R01775",
            "NumCode": "756",
            "CharCode": "CHF",
            "Nominal": 1,
            "Name": "Швейцарский франк",
            "Value": 91.7629,
            "Previous": 90.3411
        },
        "RSD": {
            "ID": "R01805F",
            "NumCode": "941",
            "CharCode": "RSD",
            "Nominal": 100,
            "Name": "Сербских динаров",
            "Value": 75.9657,
            "Previous": 75.0009
        },
        "ZAR": {
            "ID": "R01810",
            "NumCode": "710",
            "CharCode": "ZAR",
            "Nominal": 10,
            "Name": "Южноафриканских рэндов",
            "Value": 43.9035,
            "Previous": 43.2911
        },
        "KRW": {
            "ID": "R01815",
            "NumCode": "410",
            "CharCode": "KRW",
            "Nominal": 1000,
            "Name": "Вон Республики Корея",
            "Value": 63.9889,
            "Previous": 62.9692
        },
        "JPY": {
            "ID": "R01820",
            "NumCode": "392",
            "CharCode": "JPY",
            "Nominal": 100,
            "Name": "Японских иен",
            "Value": 59.4288,
            "Previous": 58.6924
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
        return round(row_value, count_round)


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



