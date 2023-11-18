from django import template

#decorater
register = template.Library()

@register.filter(name = "is_in_cart")
def is_in_cart(item, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == item.id:
            return True
    return False

@register.filter(name = "get_quantity")
def get_quantity(item, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == item.id:
            return cart.get(id)
    return 0

@register.filter(name = "get_item_total")
def get_item_total(item, cart):
    return item.item_price * get_quantity(item,cart)

@register.filter(name = "get_cart_total")
def get_cart_total(item, cart):
    sum = 0
    for item in item:
        sum += get_item_total(item, cart)
    return sum

@register.filter(name = "get_total_quanity")
def get_total_quantity(cart):
    quantity = 0
    keys = cart.keys()
    for id in keys:
        quantity+= cart.get(id)
    return quantity