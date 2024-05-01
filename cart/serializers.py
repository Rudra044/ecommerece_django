from rest_framework import serializers
from .models import Cart


class Cartserializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["quantity", "total"]