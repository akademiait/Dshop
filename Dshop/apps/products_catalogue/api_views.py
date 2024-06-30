from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from dj_shop_cart.cart import get_cart_class
from .models import Order, Product
from .serializers import (CartReadSerializer, ProductSerializer, 
                          CartWriteSerializer, OrderSerializer)
from .filters import ProductFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True, parent_product=None)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = (AllowAny, )

class CartAPIView(APIView):
    permission_classes = (AllowAny ,)
    serializer_class = CartReadSerializer
    
    def post(self, request):
        write_serializer = CartWriteSerializer(data=request.data, context={'request': request})
        if write_serializer.is_valid():
            cart = write_serializer.save()
            return Response(self.serializer_class(cart).data, status=status.HTTP_201_CREATED)
        else:
            return Response(write_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        cart = get_cart_class().new(request)
        serializer = self.serializer_class(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes((AllowAny, ))
def empty_cart(request):
    get_cart_class().new(request).empty()
    return Response({"message": "cart empty"})


class OrderAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            return Response(self.serializer_class(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    