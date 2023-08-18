from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponAddForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
from datetime import datetime


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "orders/cart.html", {'cart': cart})


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        messages.success(request, "Product Successfully Added to Card", "success")
        return redirect('home:product_detail', product.slug)


class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product.id)
        return redirect("orders:cart")


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        if not len(cart):
            messages.error(request, "No Item to buy! Cart is empty", 'danger')
            return redirect("orders:cart")
        for item in cart:
            order_item = OrderItem.objects.create(order=order, product=item['name'], price=item['price'],
                                                  quantity=item['quantity'])
        cart.clear()
        return redirect('orders:order_bill', order.id)


class OrderBillView(LoginRequiredMixin, View):
    form_class = CouponAddForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        # save order id in session to use it when verifying
        request.session['order_pay'] = {
            'order_id': order.id
        }
        return render(request, "orders/bill.html", {'order': order, 'form': self.form_class})


class CouponAddView(LoginRequiredMixin, View):
    form_class = CouponAddForm

    def post(self, request, order_id):
        now = datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            # check code validation
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'coupon dose not valid', 'danger')
                return redirect('orders:order_bill', order_id)
            # add discount to order
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            # remove coupon
            coupon.delete()
        return redirect('orders:order_bill', order_id)


class OrderPayView(LoginRequiredMixin, View):
    """
    in real payment gateway this method redirect
    user to payment page
    see like below for zarinpal payment example:
    https://github.com/rasooll/zarinpal-django-py3
    """

    def get(self, request, order_id):
        # TODO: use zarinpal sandbox instead
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/payment.html', {'order': order})


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = get_object_or_404(Order, id=int(order_id))
        order.paid = True
        order.save()
        messages.success(request, "Successful payment", "success")
        return redirect("home:home")
