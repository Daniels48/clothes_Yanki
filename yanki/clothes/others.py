from json import loads
from re import findall
from django.http import JsonResponse


def get_cart_for_local(cart):
    return {product: cart[product]["count"] for product in cart}


def decode_json(data):
    processed_data = data.decode("utf-8") if type(data) == bytes else data
    return loads(processed_data)


def get_int_count(count):
    if type(count) == str:
        count = int(findall(r"\d+", count)[0])
    return count


def sum_products(cart):
    raw_cart = get_cart_for_local(cart)
    return sum([get_int_count(raw_cart[product]) for product in raw_cart])


def json_response(obj):
    return JsonResponse(obj)
