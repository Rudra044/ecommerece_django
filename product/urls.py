from .views import Createproduct, Manageproduct, Readproduct
from django.urls import path

urlpatterns = [
    path('create_product/', Createproduct.as_view(), name='create_product'),
    path('manage_product/<int:id>/', Manageproduct.as_view(), name='manage_product_id'),
    path('read_product/<int:id>/', Readproduct.as_view(), name='read_product_id'),
    path('read_product/', Readproduct.as_view(), name='read_product'),
]