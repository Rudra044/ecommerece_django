from django.urls import path
from .views import Managecart, Checkout


urlpatterns =     [
    path('cart/<int:product_id>', Managecart.as_view()),
    path('cart', Managecart.as_view()),
    path('checkout/<int:id>', Checkout.as_view()),
    path('checkout', Checkout.as_view()),
    ]