from django.urls import path
from .views import Createorder, Manageorder, Orderseller


urlpatterns = [
    path('create_order/<int:product_id>/', Createorder.as_view(), name='create_order'),
    path('manage_order/<int:id>/', Manageorder.as_view(), name='manage_order_id'),
    path('manage_order/', Manageorder.as_view(), name='manage_order'),
    path('get_order/', Orderseller.as_view(), name='get_order'),
    path('get_order/<int:id>/', Orderseller.as_view(), name='get_order_id'),
]