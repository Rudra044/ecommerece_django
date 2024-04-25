from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from product.models import Product
from .serializers import Cartserializer
from order.models import Order

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
        if product.inventory < quantity:
            return Response({"message":f"You can only add elements upto {product.inventory}"})
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


class Checkout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id=None):
        user = request.user
        if id:
            try:
                cart = Cart.objects.get(user=user, id=id)
            except Cart.DoesNotExist:
                return Response({"error":"Item you want to order is not added by you."})
            if cart.product.inventory < cart.quantity:
                return Response({"message":f"You can only add elements upto {cart.product.inventory}"})
            order = Order.objects.create(user=user, product=cart.product, quantity=cart.quantity)
            total = cart.total
            cart.product.inventory = cart.product.inventory-cart.quantity
            cart.product.save()
            order.save()
            cart.delete()
            return Response({"message":f"Your order has been created total-{total}, inventory-{cart.product.inventory}"})
        else:
            cart_items = Cart.objects.filter(user=user)
            for cart in cart_items:
                if cart.product.inventory < cart.quantity:
                    return Response({"message":f"You can only add elements upto {cart.product.inventory}"})
                order = Order.objects.create(user=user, product=cart.product, quantity=cart.quantity)
                total = cart.total
                cart.product.inventory = cart.product.inventory-cart.quantity
                cart.product.save()
                order.save()
                cart.delete()
                return Response({"message":f"Your order has been created total-{total}, inventory-{cart.product.inventory}"})





