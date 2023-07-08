from re import findall

from clothes.set_session_data.currency import get_currency_for_page, get_valute, get_sign
from yanki.settings import LIKE_SESSION_ID


def sort_size(lst):
    list_size = {"XXS": 40, "XS": 44, "S": 46, "M": 48, "L": 50, "XL": 52, "XXL": 54, "3XL": 58}
    return sorted(lst, key=lambda elem: list_size[elem])


def calc_color(string):
    return sum([int(items, 16) for items in findall(r"\w{2}", string=string.upper())])


def sort_color(lst):
    return sorted(lst, key=lambda elem: calc_color(elem), reverse=True)


def get_finished_products(raw_list):
    lst_sort = sorted(raw_list, key=lambda elem: elem.id)
    lst_id = []
    list_product = []

    for item in lst_sort:
        if item.parent_id not in lst_id:
            item.color.hex = [item.color.hex, ]
            item.size.title = [item.size.title, ]
            lst_id.append(item.parent_id)
            for x in raw_list:
                if x.id != item.id and x.parent_id == item.parent_id:
                    if x.color.hex not in item.color.hex:
                        item.color.hex.append(x.color.hex)
                    if x.size.title not in item.size.title:
                        item.size.title.append(x.size.title)

            list_product.append(item)

    return list_product


def set_currency_and_like(list_products, request, search=False):
    list_like = request.session.get(LIKE_SESSION_ID, [])
    set_like = lambda x: str(x.parent.id) in list_like
    currency = get_currency_for_page(request)
    sign = get_sign(currency)
    old_vals, new_vals = get_valute(currency)

    def set_data(products_list):
        for item in products_list:
            if search:
                item.size = sort_size(item.size)
                item.color = sort_color(item.color)
            else:
                item.size.title = sort_size(item.size.title)
                item.color.hex = sort_color(item.color.hex)
            item.like = set_like(item)
            if sign != "грн":
                item.f_price = f"{round(float(item.parent.price) * old_vals / float(new_vals), 2)} {sign}"
            else:
                item.f_price = f"{int(item.parent.price)} {sign}"
        return products_list

    if type(list_products) != list:
        products = set_data([list_products])
        return products[0]

    products = set_data(list_products)

    return products
