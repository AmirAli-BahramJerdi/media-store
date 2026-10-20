from decimal import Decimal
from apps.shop.models import Product

CART_SESSION_ID = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override=False):
        pid = str(product.id)
        if pid not in self.cart:
            self.cart[pid] = {"quantity": 0, "price": str(product.price), "name": product.name}
        if override:
            self.cart[pid]["quantity"] = quantity
        else:
            self.cart[pid]["quantity"] += quantity
        self.save()

    def remove(self, product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):
        pids = list(self.cart.keys())
        products = {str(p.id): p for p in Product.objects.filter(id__in=pids)}
        for pid in pids:
            if pid not in products:
                del self.cart[pid]
                continue
            item = self.cart[pid]
            item["product"] = products[pid]
            item["total_price"] = Decimal(item["price"]) * item["quantity"]
        self.save()
        for item in self.cart.values():
            yield item

    def get_total_price(self):
        return sum(Decimal(i["price"]) * i["quantity"] for i in self.cart.values())

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()
