from rest_framework import serializers
from apps.cart.models import Cart, CartLine
from apps.catalog.serializers import ProductSerializer


class CartLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartLine
        fields = ["id", "product", "product_id", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    lines = CartLineSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "session_key", "lines", "created_at", "updated_at"]
        read_only_fields = ["user", "session_key", "created_at", "updated_at"]
