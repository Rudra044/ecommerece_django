from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import Productserializer
from user.decorators import is_seller


class Createproduct(APIView):
    permission_classes = [IsAuthenticated]
    @is_seller
    def post(self,request):
        user_id = request.user.id
        serializer = Productserializer(data=request.data)
        if serializer.is_valid():
            try:
                Product.objects.get(user_id=user_id, name=serializer.validated_data.get("name"))
                return Response({
                    "message": 
                    "you have added the product you can update its detail but not add similar product again."}, 
                    status=status.HTTP_202_ACCEPTED)
            except Product.DoesNotExist:
                serializer.save(user_id=user_id)
        return Response({"message":"The product is added"}, status=status.HTTP_201_CREATED)
    

class Manageproduct(APIView):
    permission_classes = [IsAuthenticated]
    @is_seller
    def patch(self,request,id):
        user = request.user
        try:
            product = Product.objects.get(user_id=request.user.id, id=id)
        except Product.DoesNotExist:
            return Response({"error":"The product you are giving input is not added by you. You cannot update its detail."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = Productserializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response({"message":"The details are updated."}, status=status.HTTP_202_ACCEPTED)
    
    @is_seller       
    def delete(self,request,id):
        user = request.user
        try:
            product = Product.objects.get(user=user, id=id)
        except Product.DoesNotExist:
            return Response({"error":"The prroduct you are giving input is not added by you. You cannot delete it."},
                            status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response({"message":"The product is deleted."}, status=status.HTTP_200_OK)
    

class Readproduct(APIView):
    def get(self, request, id=None):
        if id:
            try:
                product = Product.objects.get(id=id)
                serializer = Productserializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response({"error":"Id provided by u does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            product = Product.objects.all()
            serializer = Productserializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
                

        

    

