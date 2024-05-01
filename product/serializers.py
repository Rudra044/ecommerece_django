from rest_framework import serializers
from .models import Product


class Productserializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name","description","price","inventory"]