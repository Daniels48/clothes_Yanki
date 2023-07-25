from clothes.others import json_response, get_cart_for_local
from re import findall
from clothes.models import Product
from clothes.others import decode_json, get_int_count, sum_products
from clothes.set_session_data.currency import get_sum_all_objects_cart_with_currency_price_or_one, \
    get_dict_response_for_cart
from clothes.utils import get_select_related_and_selected_fields_products
from users.models import CartProduct
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


def get_products_from_bd(id_products):
    get_from_bd = lambda id_products: Product.objects.filter(id__in=id_products).select_related("parent").\
        only("id", global_count, "parent__price")
    if type(id_products) != list:
        id_products = [id_products]
        return get_from_bd(id_products)[0]
    else:
        return get_from_bd(id_products)


def set_local_cart(cart_session):
    if cart_session == "Null":
        return cart_session
    return {key_products: get_cart_for_local(cart_session), global_count: sum_products(cart_session)}


def set_cart(data, request):
    local_cart = data.get(CART_SESSION_ID)

    if local_cart:
        products_cart = local_cart.get(key_products)
        products_id = list(products_cart.keys())
        bd_products = get_products_from_bd(products_id)

        for product in bd_products:
            product_id = str(product.id)
            old_count = products_cart[product_id]
            products_cart[product_id] = check_availability_product(product, old_count, False)

        request.session[CART_SESSION_ID] = products_cart

    return request


def check_availability_product(product, old_count, sign):
    def check_product(count_in_bd, count_old):
        set_max_count = lambda count : f"{count}M"

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


def get_cart_in_bd(request):
    session_cart = request.session.get(CART_SESSION_ID, {})
    if not session_cart:
        if request.user.is_authenticated:
            price = "product__parent__price"
            query_cart = CartProduct.objects.filter(user=request.user).select_related("product__parent").\
                values("product", "count", price)
            if len(query_cart):
                get_cart_item = lambda item: {str(item.get("product")): {"count": item.get("count"), "price": float(item.get(price))}}
                session_cart = {get_cart_item(item) for item in query_cart}
                request.session[CART_SESSION_ID] = session_cart
    return session_cart


class Cart:
    def get_queryset(self):
        return self.get_list_cart(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_sum"] = get_sum_all_objects_cart_with_currency_price_or_one(self.request)
        context["title"] = "Корзина"
        return context

    def post(self, request):
        data = decode_json(request.body)
        cart = self.change_product_in_cart(data)
        return json_response(cart)

    @staticmethod
    def get_list_cart(request):
        raw_cart = get_cart_in_bd(request)
        cart = get_cart_for_local(raw_cart)
        filters = {"id__in": [*cart]}
        products = get_select_related_and_selected_fields_products(filters, CART_SESSION_ID)

        for item in products:
            id_product = str(item.id)
            raw_count_product = cart.get(id_product)
            count_product = findall(r"\d+", str(raw_count_product))[0]

            if type(raw_count_product) != int:
                item.max = True
            item.cart = count_product
            item.f_price = get_sum_all_objects_cart_with_currency_price_or_one(request, id_product)

        return products

    def change_product_in_cart(self, data):
        dict_response = {}
        if data.get(name_id):
            cart = get_cart_in_bd(self.request)
            product_id, sign = data.get(name_id), data.get(name_sign)

            if sign != del_product:
                cart, quantity_product = self.plus_or_minus_product(cart, product_id, sign)
            else:
                cart, quantity_product, dict_response = self.remove_product(cart, product_id, dict_response)

            if data.get("get_currency") == "1":
                dict_response[CURRENCY_SESSION_ID] = get_dict_response_for_cart(self.request, product_id)

            dict_response[command] = quantity_product
            dict_response[change_cart] = set_local_cart(cart)
        return dict_response

    def plus_or_minus_product(self, cart, product_id, sign):
        product = get_products_from_bd(product_id)
        old_count = cart.get(product_id, 0)

        if old_count != 0:
            old_count = old_count.get(global_count)

        object_cart_session = check_availability_product(product, old_count, sign)

        cart[product_id] = object_cart_session
        self.request.session[CART_SESSION_ID] = cart

        quantity_product = object_cart_session.get(global_count)

        self.change_quantity_product_in_bd(quantity_product, product)

        return cart, quantity_product

    def remove_product(self, cart, product_id, dict_response):
        del cart[product_id]
        self.get_cart_product(product_id).delete()
        quantity_product = "delete"

        if len(cart):
            self.request.session[CART_SESSION_ID] = cart
        else:
            del self.request.session[CART_SESSION_ID]
            cart = "Null"
            dict_response["None_cart"] = non_cart

        return cart, quantity_product, dict_response

    def get_cart_product(self, product):
        return CartProduct.objects.get(user=self.request.user, product=product)

    def change_quantity_product_in_bd(self, quantity_product, product):
        user = self.request.user
        if user.is_authenticated:
            int_quantity_product = get_int_count(quantity_product)
            try:
                cart_product = self.get_cart_product(product)
                cart_product.count = int_quantity_product
                cart_product.save()
            except CartProduct.DoesNotExist:
                cart_product = CartProduct.objects.create(user=user, product=product, count=int_quantity_product)
                cart_product.save()

