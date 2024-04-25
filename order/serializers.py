from rest_framework import serializers
from .models import Order


class Orderserializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "quantity", "status"]
