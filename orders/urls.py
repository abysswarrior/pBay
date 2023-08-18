from django.urls import path, include
from . import views

app_name = "orders"

payment_url = [
    path('<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
]

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name="order_create"),
    path('bill/<int:order_id>/', views.OrderBillView.as_view(), name="order_bill"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name="cart_add"),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name="cart_remove"),
    path('payment/', include(payment_url)),
    path('coupon/add/<int:order_id>', views.CouponAddView.as_view(), name="coupon_add")
]
