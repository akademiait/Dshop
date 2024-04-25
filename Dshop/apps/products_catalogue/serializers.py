import json
from django.db import transaction
from django.shortcuts import get_object_or_404
from dj_shop_cart.cart import get_cart_class
from rest_framework import serializers
from .models import Product, Order, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

        
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price', 'short_description', 'full_description', 'parent_product', 'images']
        read_only_fields = ['id']


class CartItemSerializer(serializers.Serializer):
    product_pk = serializers.IntegerField(min_value=1, required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)
    product_name = serializers.CharField(read_only=True, max_length=200)
    price = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    subtotal = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    item_id = serializers.IntegerField(read_only=True, min_value=1)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_name = Product.objects.get(pk=instance.product_pk).name
        representation['product_name'] = product_name
        return representation


class CartReadSerializer(serializers.Serializer):
    total = serializers.DecimalField(
        read_only=True, min_value=0, max_digits=10, decimal_places=2
    )
    items = serializers.SerializerMethodField()
    count = serializers.IntegerField(read_only=True, min_value=1)

    def get_items(self, obj):
        return CartItemSerializer(list(obj), many=True).data


class CartWriteSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True, required=False)

    def create(self, validated_data):
        request = self.context['request']
        cart = get_cart_class().new(request)
        cart.empty()
        with transaction.atomic():
            for item in validated_data.get("items", []):
                product = get_object_or_404(Product, pk=item['product_pk'])
                cart.add(product, quantity=item['quantity'])
        return cart
    

    def validate_items(self, items):
        product_pks = set()
        for item in items:
            product_pk = item.get("product_pk")
            if product_pk in product_pks:
                raise serializers.ValidationError(
                    "product_pk must be unique within items."
                )
            product_pks.add(product_pk)
        return items
    

def cart_and_delivery_to_order_data(cart, delivery, data):
    cart_data = CartReadSerializer(cart).data
    data["cart_details"] = json.dumps(cart_data)
    data["delivery_name"] = delivery.name
    data["delivery_price"] = delivery.price
    data["cart_total"] = cart.total
    data["total_sum"] = cart.total + delivery.price
    return data


class OrderSerializer(serializers.ModelSerializer):

    cart = CartWriteSerializer(write_only=True, required=True)

    def validate_cart(self, cart_data):
        if len(cart_data["items"]) < 1:
            raise serializers.ValidationError("No items")
        return cart_data

    def create(self, validated_data):
        cart_data = validated_data.pop('cart')
        delivery = validated_data.pop('delivery')
        cart_serializer = CartWriteSerializer(data=cart_data, context=self.context)
        cart_serializer.is_valid(raise_exception=True)
        cart = cart_serializer.save()
        order_details = cart_and_delivery_to_order_data(cart, delivery, {})
        return Order.objects.create(delivery=delivery, **validated_data, **order_details)
    

    class Meta:
        model = Order
        fields = ['delivery', "cart",
                  'created_at','cart_details',
                  'cart_total','delivery_name',
                  'delivery_price','total_sum']
       
        read_only_fields = ["created_at", "cart_details"
                            "cart_total", "delivery_name",
                            "delivery_price", "total_sum"]


