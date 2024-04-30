from django.urls import path
from .views import Managecart, Checkout


urlpatterns = [
    path('cart/<int:product_id>/', Managecart.as_view(), name='cart_id'),
    path('cart/', Managecart.as_view(), name='cart'),
    path('checkout/<int:id>/', Checkout.as_view(), name='checkout_id'),
    path('checkout/', Checkout.as_view(), name='checkout'),
]
