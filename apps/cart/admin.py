from django.contrib import admin
from apps.cart.models import Cart, CartLine


class CartLineInLine(admin.TabularInline):
    model = CartLine
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "session_key", "created_at")
    inlines = [CartLineInLine]
