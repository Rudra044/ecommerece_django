from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from product.models import Product
from.serializers import Cartserializer

class Managecart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, product_id):
        quantity = request.data.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error":"invalid product id."})
        user_id = request.user.id
        try:
            items = Cart.objects.get(user_id=user_id, product_id=product_id)
        except:
            items = Cart.objects.create(user_id=user_id, product_id=product_id)
        items.quantity = quantity
        items.total = quantity*product.price
        items.save()
        return Response({"message":"items are added to the cart"})
    
    def delete(self, request, product_id=None):
        user = request.user
        if product_id:
            try:
                items = Cart.objects.get(user_id=user.id, product_id=product_id)
            except Cart.DoesNotExist:
                return Response({"error":"Item you want to delete is not added by you."})
            items.delete()
            return Response({"message":"Item deleted"})
        else:
            items = Cart.objects.filter(user_id=user.id)
            items.delete()
            return Response({"message":"All cart items deleted"})
    
    
    def get(self, request, product_id=None):
        user = request.user
        if product_id:
            try:
                items = Cart.objects.get(user_id=user.id, product_id=product_id)
                serializer = Cartserializer(items)
                return Response(serializer.data)
            except Cart.DoesNotExist:
                return Response({"error":"Id provided by u does not exist."})
        else:
            items = Cart.objects.filter(user_id=user.id)
            serializer = Cartserializer(items, many=True)
            return Response(serializer.data)




