from .views import Createproduct, Manageproduct, Readproduct
from django.urls import path

urlpatterns = [
    path('create_product', Createproduct.as_view()),
    path('manage_product/<int:id>', Manageproduct.as_view()),
    path('read_product/<int:id>', Readproduct.as_view()),
    path('read_product', Readproduct.as_view()),

]