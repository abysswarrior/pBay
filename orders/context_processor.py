from .cart import Cart


def cart_item_counter(request):
    return {'item_counter': Cart(request)}
