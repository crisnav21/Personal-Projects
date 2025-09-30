from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session_key"],
                name="uniq_cart_session",
                condition=~models.Q(session_key=None),
            )
        ]

    def __str__(self):
        who = self.user or self.session_key or "anon"
        return f"Cart({who})"


class CartLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="lines")

    from apps.catalog.models import Product

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField(default=1)

    class Meta:
        unique_together = [("cart", "product")]

    def __str__(self):
        return f"{self.product} x {self.quantity}"
