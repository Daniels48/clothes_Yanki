from clothes.others import decode_json
from clothes.set_session_data.cart import set_cart
from clothes.set_session_data.currency import set_currency
from clothes.set_session_data.like import set_like
local_name = "local"


def set_items(data, request):
    set_cart(data, request)
    set_currency(data, request)
    set_like(data, request)
    return request


def set_local_data(get_response):
    def middleware(request):

        if request.method == "POST":
            data = decode_json(request.body)

            if data.get(local_name):
                request = set_items(data, request)

        response = get_response(request)
        return response

    return middleware


