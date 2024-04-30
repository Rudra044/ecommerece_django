from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Order
from product.models import Product
from .serializers import Orderserializer

from user.decorators import is_seller


class Createorder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        quantity = request.data.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)
        if product.inventory < quantity:
            return Response({"message": f"You can maximum order {product.inventory}"}, status=status.HTTP_200_OK)
        if user.address is None:
            return Response({"message": "Please add your address before order"})
        order = Order.objects.create(user=user, product=product)
        order.quantity = quantity
        order.save()
        product.inventory = product.inventory-quantity
        product.save()
        amount = product.price*quantity
        return Response(
            {"message":
             f"Your order has been created items-{order.quantity}, status-{order.status}, inventory_left-{product.inventory}, amount-{amount}"}, 
             status=status.HTTP_201_CREATED)

   
class Manageorder(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user = request.user
        try:
            items = Order.objects.get(user_id=user.id, id=id)
        except Order.DoesNotExist:
            return Response({"error": "Order you want to delete is not added by you."}, 
                            status=status.HTTP_400_BAD_REQUEST)
        product = items.product
        product.inventory = product.inventory+items.quantity
        product.save()
        items.delete()
        return Response({"message": "Order deleted"}, status=status.HTTP_200_OK)
    
    @is_seller
    def patch(self, request, id):
        useri = request.user
        status = request.data.get("status")
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"})
        product = order.product
        user = product.user
        if useri.id == user.id:
            order.status = status
            order.save()
            return Response({"message": f"the status has been updated to {order.status}"})
        else:
            return Response({"error": "Order you want to update is not taken from you."})   

    def get(self, request, id=None):
        user = request.user
        if id:
            try:
                order = Order.objects.get(user=user, id=id)
                serializer = Orderserializer(order)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"error": "Id provided by you does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            order = Order.objects.filter(user=user)
            serializer = Orderserializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class Orderseller(APIView):
    @is_seller
    def get(self, request, id=None):
        user = request.user
        if id:
            try:
                order = Order.objects.get(user=user, id=id)
                product = order.product
                user1 = product.user
                if user1 == user:
                    serializer = Orderserializer(order)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"error": "Id provided by ypu does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            order = Order.objects.filter(product__user=user)
            serializer = Orderserializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)



        





    




