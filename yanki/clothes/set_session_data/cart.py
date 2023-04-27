from clothes.others import json_response, get_cart_for_local
from re import findall
from clothes.models import Product
from clothes.others import decode_json, get_int_count, sum_products
from clothes.set_session_data.currency import send_local_data, get_local_data_for_cart, get_all_sum_or_one
from clothes.utils import get_selected_products
from yanki.settings import CART_SESSION_ID, CURRENCY_SESSION_ID

name_id = "id"
name_sign = "sign"
add_product = "+"
sub_product = "-"
del_product = "delete"
key_products = "products"
change_cart = "change_cart"
set_cart = "new_cart"
command = "command"
global_count = "count"


non_cart = "<div class='cart__null null'> <div class='null__img'> <div class='null__icon icon-cart'></div>" \
           "</div><div class='null__data'><div class='null__text text-20'>В корзине нет товаров</div>" \
           "<div class='null__subinfo'><div class='null__subtext text-14'>Перейдите в каталог, " \
           "чтобы добавить товары в корзину</div><a href='/catalog/' " \
           "class='null__button'>Перейти</a></div></div></div>"


def get_list_cart(request):
    raw_cart = request.session.get(CART_SESSION_ID, [])
    cart = get_cart_for_local(raw_cart)
    filters = {"id__in": [*cart]}
    products = get_selected_products(filters, CART_SESSION_ID)

    for item in products:
        count = findall(r"\d+", str(cart.get(str(item.id))))[0]
        if type(cart.get(str(item.id))) != int:
            item.max = True
        item.cart = count
        item.f_price = get_all_sum_or_one(request, str(item.id))

    return products


def get_products_from_bd(id_products):
    get_from_bd = lambda id_products: Product.objects.filter(id__in=id_products).\
        select_related("parent").only("id", global_count, "parent__price")
    if type(id_products) != list:
        id_products = [id_products]
        products = get_from_bd(id_products)[0]
    else:
        products = get_from_bd(id_products)
    return products


def set_cart(data, request):
    old_cart = data.get(CART_SESSION_ID)

    if old_cart:
        cart = old_cart.get(key_products)
        products_id = list(cart.keys())
        bd_products = get_products_from_bd(products_id)
        for product in bd_products:
            product_id = str(product.id)
            old_count = cart[product_id]
            cart[product_id] = check_availability_product(product, old_count, False)
        request.session[CART_SESSION_ID] = cart

    return request


def check_availability_product(product, old_count, sign):
    def check_product(count_in_bd, count_old):
        def set_max_count(count):
            return str(count) + "M"
        new_count = count_old

        if new_count > count_in_bd:
            new_count = set_max_count(count_in_bd)

        if new_count == count_in_bd:
            new_count = set_max_count(count_in_bd)

        if count_in_bd == 0:
            new_count = 0

        return new_count
    old_count = get_int_count(old_count)
    value = 1 if sign == add_product else -1
    product_count_in_bd = product.count
    new_count_product = check_product(product_count_in_bd, old_count)

    if sign:
        new_count_product = check_product(product_count_in_bd, old_count + value)

    return {global_count: new_count_product, "price": float(product.parent.price)}


def set_local_cart(raw_cart):
    if raw_cart == "Null":
        cart = raw_cart
    else:
        cart = {key_products: get_cart_for_local(raw_cart), global_count: sum_products(raw_cart)}
    return cart


def change_product(data, request):
    finally_data = {}
    cart = request.session.get(CART_SESSION_ID, {})
    product_id, sign = data.get(name_id), data.get(name_sign)
    if sign != del_product:
        product = get_products_from_bd(product_id)
        old_count = cart.get(product_id, 0)
        if old_count != 0:
            old_count = old_count.get(global_count)
        cmd = check_availability_product(product, old_count, sign)
        cart[product_id] = cmd
        request.session[CART_SESSION_ID] = cart
        cmd = cmd.get(global_count)
    else:
        del cart[product_id]
        cmd = "delete"
        if len(cart) == 0:
            del request.session[CART_SESSION_ID]
            cart = "Null"
            finally_data["None_cart"] = non_cart
        else:
            request.session[CART_SESSION_ID] = cart

    if data.get("get_currency") == "1":
        finally_data[CURRENCY_SESSION_ID] = get_local_data_for_cart(request, product_id)
    finally_data[command] = cmd
    finally_data[change_cart] = set_local_cart(cart)
    return finally_data


class Cart:
    def post(self, request):
        data = decode_json(request.body)
        cart = {}
        if data.get(name_id):
            cart = change_product(data, request)
        return json_response(cart)


