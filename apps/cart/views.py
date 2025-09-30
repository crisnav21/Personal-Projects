from django.db import transaction
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartLine
from .serializers import CartSerializer, CartLineSerializer
from apps.catalog.models import Product


def _get_or_create_cart(request):
    # ensure session exists
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(
        session_key=session_key,
        defaults={"user": request.user if request.user.is_authenticated else None},
    )
    return cart


class CartView(APIView):
    def get(self, request):
        cart = _get_or_create_cart(request)
        return Response(CartSerializer(cart).data)


class CartAddView(APIView):
    @transaction.atomic
    def post(self, request):
        cart = _get_or_create_cart(request)
        serializer = CartLineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        qty = serializer.validated_data.get("quantity", 1)

        product = Product.objects.get(pk=product_id)
        line, created = CartLine.objects.select_for_update().get_or_create(
            cart=cart, product=product, defaults={"quantity": qty}
        )
        if not created:
            line.quantity += qty
            line.save(update_fields=["quantity"])

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartLineView(APIView):
    @transaction.atomic
    def patch(self, request, line_id: int):
        cart = _get_or_create_cart(request)
        try:
            line = cart.lines.select_for_update().get(pk=line_id)
        except CartLine.DoesNotExist:
            return Response({"detail": "Line not found"}, status=404)

        qty = int(request.data.get("quantity", 1))
        if qty < 1:
            line.delete()
        else:
            line.quantity = qty
            line.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data)

    @transaction.atomic
    def delete(self, request, line_id: int):
        cart = _get_or_create_cart(request)
        deleted, _ = cart.lines.filter(pk=line_id).delete()
        if not deleted:
            return Response({"detail": "Line not found"}, status=404)
        return Response(CartSerializer(cart).data)


class CartPage(TemplateView):
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if not self.request.session.session_key:
            self.request.session.save()
        cart, _ = Cart.objects.get_or_create(
            session_key=self.request.session.session_key
        )
        ctx["cart"] = cart
        return ctx
