from re import findall


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

    for item in list_product:
        item.size.title = sort_size(item.size.title)
        item.color.hex = sort_color(item.color.hex)

    return list_product
