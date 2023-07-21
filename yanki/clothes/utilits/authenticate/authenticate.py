from django.contrib.auth import login
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from clothes.models import Product
from clothes.utilits.authenticate.send_data import data
from clothes.others import decode_json
from clothes.services.email import send_activate_email_message
from users.models import User, CartProduct
from yanki.settings import CART_SESSION_ID, LIKE_SESSION_ID, CURRENCY_SESSION_ID


def get_user(username):
    return User.objects.get(Q(username=username) | Q(email=username) | Q(phone=username))


class AuthenticateMixin(View):
    def post(self, request):
        info = decode_json(request.body)
        types = info.get("type", False)
        username = info.get("login", False)
        password = info.get("password", False)

        if types == "0":
            try:
                user = get_user(username)
                if user.check_password(password):
                    set_data_request(request, user)
                    login(request, user)
                    return JsonResponse({"success": 'yes'})
                else:
                    return JsonResponse({"data": data["error0"]})
            except User.DoesNotExist:
                return JsonResponse({"data": data["error0"]})

        if types == "11":
            try:
                get_user(username)
                request.session["recovery"] = username
                request.session["cod"] = send_activate_email_message(username)
                request.session.save()
            except User.DoesNotExist:
                return JsonResponse({"data": data["error1"]})

        if types == "12":
            cod = str(request.session["cod"])
            if username != cod:
                return JsonResponse({"data": data["error11"]})
            else:
                user = request.session["recovery"]
                username = get_user(user)
                username.set_password(password)
                username.save()

        if types == "21":
            try:
                get_user(username)
                return JsonResponse({"data": data["error2"]})
            except User.DoesNotExist:
                request.session["username"] = username
                request.session["password"] = password
                request.session["active"] = send_activate_email_message("dd45512@yandex.ru")

        if types == "22":
            cod = str(request.session["active"])
            if username != cod:
                return JsonResponse({"data": data["error11"]})
            else:
                username = request.session["username"]
                password = request.session["password"]
                user = User.objects.create_user(username, password)
                login(request, user)

        return JsonResponse({"data": data[types]})


def set_data_request(request, user):
    cart = request.session.get(CART_SESSION_ID)
    like = request.session.get(LIKE_SESSION_ID)
    currency = request.session.get(CURRENCY_SESSION_ID)
    if cart:
        CartProduct.objects.filter(user=user).delete()
        for key in cart:
            count = cart[key].get("count")
            product = Product.objects.get(pk=int(key))
            cart_product = CartProduct.objects.create(product=product, user=user, count=count)
            cart_product.save()
    if like:
        list_like_int = [int(x) for x in like]
        user.like_list.set(*list_like_int)
        user.save()
    if currency:
        user.currency = currency
        user.save()




