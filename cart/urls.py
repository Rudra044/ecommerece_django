from django.urls import path
from .views import Managecart


urlpatterns =     [
    path('cart/<int:product_id>', Managecart.as_view()),
    path('cart', Managecart.as_view()),
    ]