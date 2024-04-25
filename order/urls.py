from django.urls import path
from .views import Createorder, Manageorder, Orderseller


urlpatterns =[
    path('create_order/<int:product_id>', Createorder.as_view()),
    path('manage_order/<int:id>', Manageorder.as_view()),
    path('manage_order', Manageorder.as_view()),
    path('get_order', Orderseller.as_view()),
    path('get_order/<int:id>', Orderseller.as_view()),
]