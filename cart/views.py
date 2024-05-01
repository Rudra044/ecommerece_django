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
            return Response({"error": "invalid product id."}, status=status.HTTP_404_NOT_FOUND)
        user_id = request.user.id
        try:
            items = Cart.objects.get(user_id=user_id, product_id=product_id)
        except Cart.DoesNotExist:
            items = Cart.objects.create(user_id=user_id, product_id=product_id)
        if product.inventory < quantity:
            return Response({"message": f"You can only add elements upto {product.inventory}"}, status=status.HTTP_200_OK)
        items.quantity = quantity
        items.total = quantity*product.price
        items.save()
        return Response({"message": "items are added to the cart"}, status=status.HTTP_200_OK)

    def delete(self, request, product_id=None):
        user = request.user
        if product_id:
            try:
                items = Cart.objects.get(user_id=user.id, product_id=product_id)
            except Cart.DoesNotExist:
                return Response({"error": "Cart does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            items.delete()
            return Response({"message": "Item deleted"})
        else:
            items = Cart.objects.filter(user_id=user.id)
            items.delete()
            return Response({"message": "All cart items deleted"}, status=status.HTTP_200_OK)

    def get(self, request, product_id=None):
        user = request.user
        if product_id:
            try:
                items = Cart.objects.get(user_id=user.id, product_id=product_id)
                serializer = Cartserializer(items)
                return Response(serializer.data)
            except Cart.DoesNotExist:
                return Response({"error": "Id provided by you does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            items = Cart.objects.filter(user_id=user.id)
            serializer = Cartserializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id=None):
        user = request.user
        if id:
            try:
                cart = Cart.objects.get(user=user, id=id)
            except Cart.DoesNotExist:
                return Response({"error": "Item you want to order are not added in cart."}, status=status.HTTP_400_BAD_REQUEST)
            if cart.product.inventory < cart.quantity:
                return Response({"message": f"You can only add elements upto {cart.product.inventory}"}, status=status.HTTP_400_BAD_REQUEST)
            if user.address is None:
                return Response({"message": "Please add your address before order"})
            order = Order.objects.create(user=user, product=cart.product, quantity=cart.quantity)
            total = cart.total
            cart.product.inventory = cart.product.inventory-cart.quantity
            cart.product.save()
            order.save()
            cart.delete()
            return Response({"message": f"Your order has been created total-{total}, inventory-{cart.product.inventory}"}, 
                            status=status.HTTP_201_CREATED)
        else:
            cart_items = Cart.objects.filter(user=user)
            total_amount = 0
            for cart in cart_items:
                if cart.product.inventory < cart.quantity:
                    return Response({"message": f"You can only add elements upto {cart.product.inventory}"}, status=status.HTTP_400_BAD_REQUEST)
                if user.address is None:
                    return Response({"message": "Please add your address before order"})
                order = Order.objects.create(user=user, product=cart.product, quantity=cart.quantity)
                total = cart.total
                total_amount = total_amount + total
                cart.product.inventory = cart.product.inventory-cart.quantity
                cart.product.save()
                order.save() 
                cart.delete()
            return Response({"message": f"Your order has been created total-{total_amount}, inventory-{cart.product.inventory}"}, status=status.HTTP_201_CREATED)





