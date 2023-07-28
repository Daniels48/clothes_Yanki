from clothes.others import decode_json
from clothes.set_session_data.cart import set_cart
from clothes.set_session_data.currency import set_currency
from clothes.set_session_data.like import set_like
from users.models import CartProduct
from yanki.settings import LIKE_SESSION_ID, CURRENCY_SESSION_ID, CART_SESSION_ID

local_name = "local"


def set_items(data, request):
    set_cart(data, request)
    set_currency(data, request)
    set_like(data, request)
    return request


def set_session_currency_from_bd(request):
    currency = request.session.get(CURRENCY_SESSION_ID)
    if not currency:
        new_currency = request.user.currency
        if new_currency:
            request.session[CURRENCY_SESSION_ID] = new_currency


def set_like_in_bd(request):
    like = request.session.get(LIKE_SESSION_ID)
    if type(like) != list:
        like_list = list(request.user.like_list.values_list("id", flat=True))
        request.session[LIKE_SESSION_ID] = like_list


def set_cart_in_bd(request):
    cart = request.session.get(CART_SESSION_ID)
    if type(cart) != dict:
        price = "product__parent__price"
        query_cart = list(CartProduct.objects.filter(user=request.user).select_related("product__parent"). \
                          values("product", "count", price))

        get_key_product = lambda item: str(item.get("product"))
        get_value_product = lambda item: {"count": item.get("count"), "price": float(item.get(price))}
        session_cart = {get_key_product(item): get_value_product(item) for item in query_cart}
        request.session[CART_SESSION_ID] = session_cart


def set_local_data(get_response):
    def middleware(request):
        if request.method == "POST" and request.META.get("PATH_INFO").count("admin") != 1:
            data = decode_json(request.body)

            if data.get(local_name):
                request = set_items(data, request)

        if request.user.is_authenticated:
            set_session_currency_from_bd(request)
            set_like_in_bd(request)
            set_cart_in_bd(request)

        response = get_response(request)
        return response

    return middleware
